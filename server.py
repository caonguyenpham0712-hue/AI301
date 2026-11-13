import http.server
import socketserver
import json
import urllib.parse
import os
import sys
import datetime
import traceback
from engine.data_loader import DataLoader
from engine.audit_engine import AuditEngine
from engine.health_scorer import HealthScorer
from engine.recommendation_engine import RecommendationEngine
from engine.workflow_tracker import WorkflowTracker
from engine.doc_generator import DocumentGenerator
from engine.llm_client import GeminiLLMClient

PORT = 8000
BENCHMARK_DATE_STR = "2026-11-15"

# Global state
GLOBAL_DATA = {}
DOC_GEN = DocumentGenerator(output_dir="output")
LLM_CLIENT = GeminiLLMClient()

def init_agent_system():
    global GLOBAL_DATA
    loader = DataLoader(data_dir="data", benchmark_date=BENCHMARK_DATE_STR)
    unified_df = loader.load_all()

    audit_engine = AuditEngine(loader.service_packages, loader.discount_policies)
    health_scorer = HealthScorer()
    rec_engine = RecommendationEngine(loader.service_packages, loader.discount_policies)
    workflow_tracker = WorkflowTracker(benchmark_date=BENCHMARK_DATE_STR)

    enriched_rows = []
    all_tasks = []
    audit_results_list = []

    err_count_upsell_with_ticket = 0
    err_count_seats_misalignment = 0
    err_count_missed_outreach = 0
    err_count_invalid_discount = 0

    for idx, row in unified_df.iterrows():
        audit_res = audit_engine.audit_row(row)
        audit_results_list.append(audit_res)

        for v in audit_res["violations"]:
            if v["error_code"] == "ERR_01_UPSELL_BLOCKED_UNRESOLVED_TICKET":
                err_count_upsell_with_ticket += 1
            elif "ERR_02" in v["error_code"]:
                err_count_seats_misalignment += 1
            elif v["error_code"] == "ERR_03_OVERDUE_CONTACT_TIMELINE":
                err_count_missed_outreach += 1
            elif v["error_code"] == "ERR_04_INVALID_DISCOUNT_POLICY":
                err_count_invalid_discount += 1

        health_info = health_scorer.compute_score(row)
        rec_info = rec_engine.generate_recommendation(row, health_info, audit_res)
        wf_info = workflow_tracker.process_workflow(row, health_info, audit_res, rec_info)
        all_tasks.extend(wf_info["tasks"])

        row_dict = row.to_dict()
        # Format dates for JSON
        row_dict["contract_start_date"] = row_dict["contract_start_date"].strftime("%d/%m/%Y")
        row_dict["contract_end_date"] = row_dict["contract_end_date"].strftime("%d/%m/%Y")
        row_dict["target_contact_date"] = row_dict["target_contact_date"].strftime("%d/%m/%Y")
        row_dict["last_active_date"] = row_dict["last_active_date"].strftime("%d/%m/%Y") if hasattr(row_dict["last_active_date"], "strftime") else str(row_dict["last_active_date"])

        merged_row = {**row_dict, **health_info, **rec_info, **wf_info}
        enriched_rows.append(merged_row)

    total_current_arr = sum(r["annual_contract_value"] for r in enriched_rows)
    total_proposed_arr = sum(r["net_proposed_arr"] for r in enriched_rows)
    arr_growth_pct = ((total_proposed_arr - total_current_arr) / total_current_arr) * 100
    total_audited_violations = sum(1 for res in audit_results_list if res["violations_count"] > 0)
    total_at_risk = sum(1 for r in enriched_rows if "Cao" in r.get("churn_risk", ""))

    green_count = sum(1 for r in enriched_rows if "Xanh" in r.get("health_tier", ""))
    yellow_count = sum(1 for r in enriched_rows if "Vàng" in r.get("health_tier", ""))
    red_count = sum(1 for r in enriched_rows if "Đỏ" in r.get("health_tier", ""))

    violations_map = {item["customer_id"]: item["violations"] for item in audit_results_list}

    GLOBAL_DATA = {
        "benchmark_date": BENCHMARK_DATE_STR,
        "contracts": enriched_rows,
        "tasks": all_tasks,
        "violations": violations_map,
        "stats": {
            "total_contracts": len(enriched_rows),
            "total_current_arr": total_current_arr,
            "total_proposed_arr": total_proposed_arr,
            "arr_growth_pct": round(arr_growth_pct, 2),
            "total_at_risk": total_at_risk,
            "total_audited_violations": total_audited_violations,
            "err_upsell_with_ticket": err_count_upsell_with_ticket,
            "err_seats_misalignment": err_count_seats_misalignment,
            "err_missed_outreach": err_count_missed_outreach,
            "err_invalid_discount": err_count_invalid_discount,
            "green_count": green_count,
            "yellow_count": yellow_count,
            "red_count": red_count,
            "total_tasks": len(all_tasks)
        },
        "chat_history": []
    }
    print(f"Agent Engine initialized with {len(enriched_rows)} contracts and {len(all_tasks)} action tasks.")

def handle_ai_chat_query(user_msg):
    """
    Xử lý ngôn ngữ tự nhiên từ người dùng (Trưởng phòng, CSKH, Sales)
    truy vấn cơ sở tri thức Agent và thực hiện hành động.
    """
    msg_lower = user_msg.lower().strip()
    contracts = GLOBAL_DATA["contracts"]
    stats = GLOBAL_DATA["stats"]

    # 1. Tra cứu khách hàng theo mã (KH-xxxx hoặc HD-xxxx)
    import re
    kh_match = re.search(r"kh-\d+", msg_lower)
    hd_match = re.search(r"hd-2025-\d+", msg_lower)

    target_cust = None
    if kh_match:
        target_id = kh_match.group(0).upper()
        target_cust = next((c for c in contracts if c["customer_id"] == target_id), None)
    elif hd_match:
        target_id = hd_match.group(0).upper()
        target_cust = next((c for c in contracts if c["contract_id"] == target_id), None)
    else:
        # Thử tìm theo tên công ty
        for c in contracts:
            if c["customer_name"].lower() in msg_lower or any(word in msg_lower for word in c["customer_name"].lower().split() if len(word) > 4):
                target_cust = c
                break

    if target_cust:
        cid = target_cust["customer_id"]
        violations = GLOBAL_DATA["violations"].get(cid, [])
        doc_btn = f"<button class='btn btn-sm btn-primary mt-2' onclick='downloadDocx(\"{cid}\")'><i class='fa-solid fa-file-word me-1'></i>Tải Phụ Lục HĐ Word ({cid})</button>"
        approve_btn = f"<button class='btn btn-sm btn-success mt-2 ms-2' onclick='approveContract(\"{cid}\")'><i class='fa-solid fa-check me-1'></i>Duyệt Hồ Sơ Nhanh</button>"

        reply = f"""
<strong>[HỒ SƠ 360° - {target_cust['customer_name']}] ({target_cust['customer_id']} - {target_cust['contract_id']})</strong><br>
• <strong>Gói hiện tại:</strong> {target_cust['current_package']} ({target_cust['registered_seats']} seats đăng ký) | <strong>Active 30d:</strong> {target_cust['active_users_30d']} seats ({target_cust['utilization_rate_pct']}%)<br>
• <strong>Hạn hợp đồng:</strong> {target_cust['contract_end_date']} (Còn {target_cust['days_until_expiry']} ngày) | <strong>Ngày cần liên hệ:</strong> {target_cust['target_contact_date']} ({'ĐÃ QUÁ HẠN' if target_cust['days_until_contact_due'] < 0 else f'Còn {target_cust["days_until_contact_due"]} ngày'})<br>
• <strong>Sức khỏe tài khoản:</strong> <span class='badge bg-{'success' if target_cust['health_score']>=75 else ('warning text-dark' if target_cust['health_score']>=50 else 'danger')}'>{target_cust['health_score']}/100</span> - {target_cust['churn_risk']}<br>
• <strong>Sự cố P1/P2 tồn đọng:</strong> {target_cust['p1_p2_open_tickets']} ticket (CSAT: {target_cust['avg_csat']:.1f}/5)<br>
<hr class='my-2'>
• <strong>Chiến lược AI Đề xuất:</strong> <strong>{target_cust['strategy_name']}</strong><br>
• <strong>Gói đề xuất:</strong> {target_cust['proposed_package']} ({target_cust['proposed_seats']} seats) | <strong>Ưu đãi:</strong> {target_cust['applied_promos_str']} ({target_cust['total_discount_pct']}%)<br>
• <strong>Doanh thu đề xuất:</strong> <span class='text-success fw-bold'>{target_cust['net_proposed_arr']:,.0f} VND</span> (Chênh lệch: {target_cust['arr_variance']:+,.0f} VND)<br>
• <strong>Tiến độ BPMN:</strong> Làn 2: <em>{target_cust['lane2_prescreen_status']}</em> | Làn 3: <em>{target_cust['lane3_manager_decision']}</em> | Làn 4: <em>{target_cust['lane4_status']}</em><br>
{f"<div class='alert alert-warning p-2 mt-2 mb-1 small'><strong>AI đã ngăn chặn sai sót:</strong> " + '; '.join([v['title'] for v in violations]) + "</div>" if violations else "<div class='text-success small mt-1'>✓ Hồ sơ chuẩn chỉnh, không có vi phạm quy chế.</div>"}
<div class='mt-2'>{doc_btn} {approve_btn}</div>
"""
        return reply

    # 2. Truy vấn danh sách cảnh báo đỏ / rủi ro
    if any(k in msg_lower for k in ["rủi ro", "cảnh báo đỏ", "churn", "nguy cơ", "at-risk", "sự cố"]):
        red_list = [c for c in contracts if "Đỏ" in c.get("health_tier", "") or c.get("p1_p2_open_tickets", 0) > 0][:8]
        items_html = "".join([
            f"<li><strong>{c['customer_id']}</strong> - {c['customer_name']} (Health: <span class='text-danger fw-bold'>{c['health_score']}/100</span> | Sự cố: {c['p1_p2_open_tickets']} P1/P2 | Gói đề xuất: {c['proposed_package']} - {c['strategy_name']})</li>"
            for c in red_list
        ])
        return f"""
<strong>DANH SÁCH KHÁCH HÀNG CẢNH BÁO ĐỎ & NGUY CƠ RỜI BỎ ({stats['total_at_risk']} hồ sơ):</strong><br>
<small class='text-muted'>AI Agent đã kích hoạt phương án bảo vệ khách hàng (chặn tăng gói, bồi thường thiện chí, cử CSKH & Kỹ thuật xử lý trong 24h):</small>
<ul class='mt-2 mb-2 ps-3'>{items_html}</ul>
<em>Gõ <code>KH-xxxx</code> để xem chi tiết từng khách hàng.</em>
"""

    # 3. Truy vấn về 4 lỗi kinh điển
    if any(k in msg_lower for k in ["lỗi", "sai phạm", "sai sót", "vi phạm", "audit"]):
        return f"""
<strong>BÁO CÁO KIỂM TOÁN 4 SAI PHẠM KINH ĐIỂN TỪ NHÂN VIÊN:</strong><br>
1. <strong>Chặn Đề xuất Tăng gói khi còn sự cố P1/P2:</strong> Đã phát hiện và ngăn chặn <strong class='text-danger'>{stats['err_upsell_with_ticket']} ca</strong>. AI Agent tự động chuyển thành bảo vệ khách hàng và bồi thường thiện chí.<br>
2. <strong>Khắc phục Ảo tưởng số User (Active thấp):</strong> Đã điều chỉnh <strong class='text-warning'>{stats['err_seats_misalignment']} ca</strong> khách hàng active < 50%, chuyển sang đề xuất gói tinh gọn (Right-Sizing) hoặc đào tạo Onboarding.<br>
3. <strong>Phát hiện Quá hạn bắt đầu liên hệ (30 ngày):</strong> Đã báo động đỏ <strong class='text-danger'>{stats['err_missed_outreach']} ca</strong> nhân viên nhầm ngày hết hạn với ngày cần liên hệ.<br>
4. <strong>Hủy bỏ Ưu đãi sai quy chế:</strong> Đã chuẩn hóa <strong class='text-info'>{stats['err_invalid_discount']} ca</strong> chiết khấu sai thâm niên hoặc chưa đủ điều kiện Early Bird.
"""

    # 4. Thống kê doanh thu / KPIs
    if any(k in msg_lower for k in ["doanh thu", "arr", "kpi", "tổng quan", "tiền"]):
        return f"""
<strong>TỔNG QUAN TÀI CHÍNH & DỰ BÁO DOANH THU GIA HẠN:</strong><br>
• <strong>Tổng số hợp đồng:</strong> {stats['total_contracts']} hợp đồng<br>
• <strong>Doanh thu hiện tại (ARR cũ):</strong> {stats['total_current_arr']:,.0f} VND<br>
• <strong>Dự báo doanh thu mới (Proposed ARR):</strong> <strong class='text-success'>{stats['total_proposed_arr']:,.0f} VND</strong> ({stats['arr_growth_pct']:+.2f}%)<br>
• <strong>Khách hàng Khỏe mạnh (Xanh):</strong> {stats['green_count']} ({stats['green_count']/120*100:.1f}%)<br>
• <strong>Khách hàng Cần theo dõi (Vàng):</strong> {stats['yellow_count']} ({stats['yellow_count']/120*100:.1f}%)<br>
• <strong>Khách hàng Nguy cơ cao (Đỏ):</strong> {stats['red_count']} ({stats['red_count']/120*100:.1f}%)
"""

    # 5. Duyệt hợp đồng
    if any(k in msg_lower for k in ["duyệt", "approve", "phê duyệt"]):
        return "Để duyệt hợp đồng, vui lòng gõ kèm mã khách hàng (ví dụ: <code>duyệt KH-1001</code>) hoặc bấm nút <strong>Duyệt Đề Xuất Nhanh</strong> trong bảng danh sách."

    # 6. Sử dụng Google Gemini 3.8 Flash sinh phản hồi thông minh nếu có câu hỏi mở
    if LLM_CLIENT.is_configured and len(user_msg.strip()) > 5:
        sys_prompt = (
            "Bạn là Antigravity AI Agent - Chuyên gia tư vấn cấp cao về Gia hạn hợp đồng phần mềm B2B cho Công ty An Tín. "
            f"Bối cảnh hiện tại: Công ty có 120 hợp đồng sắp đến hạn, tổng ARR 40.3 tỷ VND, có 52 khách rủi ro cao, 14 ca bị chặn tăng gói do có sự cố P1/P2. "
            "Hãy trả lời ngắn gọn, chuyên nghiệp, súc tích bằng tiếng Việt, định dạng HTML đơn giản (dùng <strong>, <br>, <ul>, <li>)."
        )
        gemini_reply = LLM_CLIENT.call_gemini(sys_prompt, user_msg)
        if gemini_reply:
            return f"<div class='gemini-ai-tag text-primary small mb-1'><i class='fa-solid fa-sparkles me-1 text-warning'></i><strong>Phân tích bởi Gemini 3.8 Flash:</strong></div>" + gemini_reply.replace("\n", "<br>")

    # Mặc định: Hướng dẫn
    return f"""
Xin chào! Tôi là <strong>AI Agent Gia Hạn Hợp Đồng An Tín</strong>.<br>
Bạn có thể hỏi tôi bằng ngôn ngữ tự nhiên:
• <em>"Kiểm tra khách hàng KH-1001"</em> hoặc <em>"Xem hợp đồng HD-2025-005"</em>
• <em>"Liệt kê các khách hàng có nguy cơ rời bỏ cao nhất"</em>
• <em>"Báo cáo 4 sai phạm nghiệp vụ đã ngăn chặn"</em>
• <em>"Dự báo tổng doanh thu ARR gia hạn kỳ này"</em>
• <em>"Tạo phụ lục hợp đồng Word cho KH-1002"</em>
"""

class AgentHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open("output/Dashboard_Gia_Han_An_Tin.html", "rb") as f:
                self.wfile.write(f.read())
            return

        elif path == "/api/stats":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(GLOBAL_DATA["stats"], ensure_ascii=False).encode("utf-8"))
            return

        elif path == "/api/contracts":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(GLOBAL_DATA["contracts"], ensure_ascii=False).encode("utf-8"))
            return

        elif path.startswith("/api/contract/"):
            cid = path.split("/")[-1].upper()
            cust = next((c for c in GLOBAL_DATA["contracts"] if c["customer_id"] == cid or c["contract_id"] == cid), None)
            if cust:
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(cust, ensure_ascii=False).encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
            return

        elif path == "/api/tasks":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(GLOBAL_DATA["tasks"], ensure_ascii=False).encode("utf-8"))
            return

        elif path.startswith("/download/"):
            # Serve generated Word .docx file
            filename = urllib.parse.unquote(path.replace("/download/", ""))
            file_path = os.path.join("output", filename)
            if os.path.exists(file_path):
                self.send_response(200)
                self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                self.send_header("Content-Disposition", f"attachment; filename=\"{filename}\"")
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_response(404)
                self.end_headers()
                return

        # Fallback to default handler for static files
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len).decode('utf-8')
        try:
            data = json.loads(post_body) if post_body else {}
        except Exception:
            data = {}

        if path == "/api/chat":
            user_msg = data.get("message", "")
            bot_reply = handle_ai_chat_query(user_msg)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"reply": bot_reply}, ensure_ascii=False).encode("utf-8"))
            return

        elif path == "/api/approve":
            cid = data.get("customer_id", "").upper()
            cust = next((c for c in GLOBAL_DATA["contracts"] if c["customer_id"] == cid or c["contract_id"] == cid), None)
            if cust:
                cust["lane3_manager_status"] = "ĐÃ PHÊ DUYỆT BỞI TRƯỞNG PHÒNG (1-CLICK)"
                cust["lane3_manager_decision"] = "ĐÃ ĐỒNG Ý GIA HẠN"
                cust["lane2_prescreen_status"] = "ĐÃ DUYỆT HOÀN TẤT"
                if not cust["requires_bod_approval"]:
                    cust["lane4_status"] = "Đã Ban Hành Hợp Đồng"
                else:
                    cust["lane4_status"] = "Đã Trình BGĐ Ký Số"

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "message": f"Đã phê duyệt thành công đề xuất gia hạn cho {cust['customer_name']} ({cust['customer_id']})!",
                    "customer": cust
                }, ensure_ascii=False).encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
            return

        elif path == "/api/generate-docx":
            cid = data.get("customer_id", "").upper()
            cust = next((c for c in GLOBAL_DATA["contracts"] if c["customer_id"] == cid or c["contract_id"] == cid), None)
            if cust:
                file_name = f"Phu_Luc_Gia_Han_{cust['customer_id']}.docx"
                file_path = DOC_GEN.generate_contract_addendum(cust, file_name=file_name)
                download_url = f"/download/{file_name}"

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "file_name": file_name,
                    "download_url": download_url
                }, ensure_ascii=False).encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
            return

        self.send_response(404)
        self.end_headers()

def run_server(port=PORT):
    init_agent_system()
    server_address = ('127.0.0.1', port)
    
    # Enable address reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(server_address, AgentHTTPRequestHandler) as httpd:
        print("=" * 80)
        print(f" AI AGENT SERVER ĐANG CHẠY TẠI: http://localhost:{port}")
        print(f" • Dashboard & Trợ Lý Co-Pilot: http://localhost:{port}/index.html")
        print(f" • REST API Hợp Đồng:          http://localhost:{port}/api/contracts")
        print(f" • REST API Thống Kê:          http://localhost:{port}/api/stats")
        print("=" * 80)
        sys.stdout.flush()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nĐã dừng máy chủ AI Agent.")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run_server(port)
