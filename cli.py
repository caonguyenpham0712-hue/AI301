import argparse
import sys
import os
import json
import pandas as pd
from engine.data_loader import DataLoader
from engine.audit_engine import AuditEngine
from engine.health_scorer import HealthScorer
from engine.recommendation_engine import RecommendationEngine
from engine.workflow_tracker import WorkflowTracker
from engine.doc_generator import DocumentGenerator

def load_system():
    loader = DataLoader(data_dir="data", benchmark_date="2026-11-15")
    unified_df = loader.load_all()
    audit_engine = AuditEngine(loader.service_packages, loader.discount_policies)
    health_scorer = HealthScorer()
    rec_engine = RecommendationEngine(loader.service_packages, loader.discount_policies)
    workflow_tracker = WorkflowTracker(benchmark_date="2026-11-15")

    enriched = []
    tasks = []
    violations = {}

    for _, row in unified_df.iterrows():
        audit_res = audit_engine.audit_row(row)
        violations[row["customer_id"]] = audit_res["violations"]
        health = health_scorer.compute_score(row)
        rec = rec_engine.generate_recommendation(row, health, audit_res)
        wf = workflow_tracker.process_workflow(row, health, audit_res, rec)
        tasks.extend(wf["tasks"])
        enriched.append({**row.to_dict(), **health, **rec, **wf})

    return pd.DataFrame(enriched), tasks, violations

def cmd_summary(args):
    df, tasks, violations = load_system()
    total_arr_old = df["annual_contract_value"].sum()
    total_arr_new = df["net_proposed_arr"].sum()
    growth = ((total_arr_new - total_arr_old) / total_arr_old) * 100

    print("=" * 75)
    print(" BÁO CÁO TỔNG QUAN HỆ THỐNG GIA HẠN HỢP ĐỒNG - AN TÍN")
    print("=" * 75)
    print(f"• Tổng số hợp đồng:                 {len(df)} hồ sơ")
    print(f"• Tổng doanh thu ARR hiện tại:       {total_arr_old:,.0f} VND")
    print(f"• Dự báo doanh thu gia hạn (ARR mới): {total_arr_new:,.0f} VND ({growth:+.2f}%)")
    print(f"• Số khách hàng có nguy cơ Churn cao: {sum(1 for _, r in df.iterrows() if 'Cao' in r['churn_risk'])} khách hàng")
    print(f"• Tổng số nhiệm vụ đã giao:          {len(tasks)} đầu việc")
    print("-" * 75)
    print("KẾT QUẢ RÀ SOÁT 4 SAI PHẠM KINH ĐIỂN:")
    v_flat = [v for v_list in violations.values() for v in v_list]
    err1 = sum(1 for v in v_flat if v["error_code"] == "ERR_01_UPSELL_BLOCKED_UNRESOLVED_TICKET")
    err2 = sum(1 for v in v_flat if "ERR_02" in v["error_code"])
    err3 = sum(1 for v in v_flat if v["error_code"] == "ERR_03_OVERDUE_CONTACT_TIMELINE")
    err4 = sum(1 for v in v_flat if v["error_code"] == "ERR_04_INVALID_DISCOUNT_POLICY")

    print(f"  [Lỗi 1] Chặn Đề xuất Tăng gói khi còn sự cố P1/P2: {err1} ca")
    print(f"  [Lỗi 2] Khắc phục Ảo tưởng số User (Active thấp):  {err2} ca")
    print(f"  [Lỗi 3] Báo động đỏ Quá hạn liên hệ (30 ngày):    {err3} ca")
    print(f"  [Lỗi 4] Chuẩn hóa Ưu đãi sai quy chế:              {err4} ca")
    print("=" * 75)

def cmd_inspect(args):
    df, tasks, violations = load_system()
    cid = args.customer_id.upper()
    row = df[(df["customer_id"] == cid) | (df["contract_id"] == cid)]
    if row.empty:
        print(f"Không tìm thấy khách hàng với mã: {cid}")
        return

    r = row.iloc[0]
    cust_id = r["customer_id"]
    cust_violations = violations.get(cust_id, [])

    print("=" * 75)
    print(f" HỒ SƠ 360 ĐỘ KHÁCH HÀNG: {r['customer_name']} ({cust_id})")
    print("=" * 75)
    print(f"• Mã HĐ:            {r['contract_id']} (Ký: {r['contract_start_date'].strftime('%d/%m/%Y')} -> Hết hạn: {r['contract_end_date'].strftime('%d/%m/%Y')})")
    print(f"• Còn lại:          {r['days_until_expiry']} ngày | Tiến độ liên hệ: {'QUÁ HẠN' if r['days_until_contact_due'] < 0 else f'Còn {r["days_until_contact_due"]} ngày'}")
    print(f"• Nhân sự phụ trách: Sales: {r['account_manager']} | CSM: {r['csm_in_charge']}")
    print(f"• Gói hiện tại:     {r['current_package']} ({r['registered_seats']} seats mua, {r['active_users_30d']} active -> {r['utilization_rate_pct']}%)")
    print(f"• Tài nguyên dùng:  {r['storage_used_gb']}/{r['storage_limit_gb']} GB ({r['storage_utilization_pct']}%) | Đăng nhập/tuần: {r['avg_login_frequency_per_week']}")
    print(f"• Tình hình hỗ trợ: {r['p1_p2_open_tickets']} ticket P1/P2 đang mở (Tổng: {r['total_tickets']} tickets) | CSAT: {r['avg_csat']:.1f}/5")
    print(f"• Điểm sức khỏe:    {r['health_score']}/100 ({r['health_tier']}) | Rủi ro Churn: {r['churn_risk']}")
    print("-" * 75)
    print("PHƯƠNG ÁN GIA HẠN ĐỀ XUẤT CỦA AI AGENT:")
    print(f"• Chiến lược:       {r['strategy_name']}")
    print(f"• Gói đề xuất:      {r['proposed_package']} ({r['proposed_seats']} seats)")
    print(f"• Ưu đãi hợp chuẩn: {r['applied_promos_str']} ({r['total_discount_pct']}%) -> Giảm: {r['discount_amount']:,.0f} VND")
    print(f"• Doanh thu mới:    {r['net_proposed_arr']:,.0f} VND (Chênh lệch: {r['arr_variance']:+,.0f} VND)")
    print(f"• Cấp thẩm quyền:   {'Cần Ban Giám Đốc Phê Duyệt' if r['requires_bod_approval'] else 'Trưởng phòng đủ thẩm quyền ký'}")
    print("-" * 75)
    print("CĂN CỨ ĐỀ XUẤT ĐỊNH LƯỢNG:")
    print(r["full_rationale"])
    if cust_violations:
        print("-" * 75)
        print("SAI SÓT NHÂN VIÊN ĐÃ ĐƯỢC AI AGENT ĐIỀU CHỈNH:")
        for idx, v in enumerate(cust_violations, 1):
            print(f"  {idx}. [{v['error_code']}] {v['title']}")
            print(f"     Chi tiết: {v['detail']}")
            print(f"     Khắc phục: {v['corrective_action']}")
    print("=" * 75)

def cmd_export_docx(args):
    df, _, _ = load_system()
    cid = args.customer_id.upper()
    row = df[(df["customer_id"] == cid) | (df["contract_id"] == cid)]
    if row.empty:
        print(f"Không tìm thấy khách hàng với mã: {cid}")
        return

    r = row.iloc[0].to_dict()
    doc_gen = DocumentGenerator(output_dir="output")
    out_file = doc_gen.generate_contract_addendum(r)
    print(f"Đã xuất Phụ lục Hợp đồng Word (.docx) thành công tại:")
    print(f"-> {os.path.abspath(out_file)}")

def cmd_tasks(args):
    df, tasks, _ = load_system()
    role_filter = args.role.lower() if args.role else None

    filtered_tasks = tasks
    if role_filter:
        filtered_tasks = [t for t in tasks if role_filter in t["role"].lower()]

    print("=" * 85)
    print(f" DANH SÁCH NHIỆM VỤ THEO DÕI KHÁCH HÀNG ({len(filtered_tasks)}/{len(tasks)} tasks)")
    print("=" * 85)
    for idx, t in enumerate(filtered_tasks[:args.limit], 1):
        print(f"[{idx:03d}] {t['customer_id']} - {t['customer_name'][:30]}")
        print(f"      Bộ phận: {t['role']} | Người phụ trách: {t['assignee']}")
        print(f"      Nhiệm vụ: {t['task_title']} | Hạn chót: {t['due_date']} | Mức độ: {t['urgency']}")
        print(f"      Chi tiết: {t['instructions'][:80]}...")
        print("-" * 85)

def main():
    parser = argparse.ArgumentParser(description="CLI Quản Trị Hệ Thống AI Agent Gia Hạn Hợp Đồng - Công Ty An Tín")
    subparsers = parser.add_subparsers(dest="command", help="Lệnh chức năng")

    # Command: summary
    p_summary = subparsers.add_parser("summary", help="Xem báo cáo tổng quan và KPIs")

    # Command: inspect
    p_inspect = subparsers.add_parser("inspect", help="Tra cứu hồ sơ 360 độ của khách hàng")
    p_inspect.add_argument("customer_id", help="Mã khách hàng (KH-xxxx) hoặc mã HĐ (HD-xxxx)")

    # Command: export-docx
    p_docx = subparsers.add_parser("export-docx", help="Tự động sinh Phụ lục Hợp đồng gia hạn dạng Word (.docx)")
    p_docx.add_argument("customer_id", help="Mã khách hàng (KH-xxxx) hoặc mã HĐ (HD-xxxx)")

    # Command: tasks
    p_tasks = subparsers.add_parser("tasks", help="Xem danh sách nhiệm vụ hành động")
    p_tasks.add_argument("--role", help="Lọc theo bộ phận: cskh, sales, support")
    p_tasks.add_argument("--limit", type=int, default=15, help="Số lượng nhiệm vụ hiển thị (mặc định 15)")

    args = parser.parse_args()

    if args.command == "summary":
        cmd_summary(args)
    elif args.command == "inspect":
        cmd_inspect(args)
    elif args.command == "export-docx":
        cmd_export_docx(args)
    elif args.command == "tasks":
        cmd_tasks(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

