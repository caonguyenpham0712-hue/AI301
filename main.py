import os
import pandas as pd
from engine.data_loader import DataLoader
from engine.audit_engine import AuditEngine
from engine.health_scorer import HealthScorer
from engine.recommendation_engine import RecommendationEngine
from engine.workflow_tracker import WorkflowTracker
from engine.excel_exporter import ExcelExporter
from engine.html_dashboard import HTMLDashboardGenerator
from engine.presentation_generator import PresentationGenerator

def main():
    print("=" * 80)
    print(" HỆ THỐNG AI AGENT ĐIỀU PHỐI & THẨM ĐỊNH GIA HẠN HỢP ĐỒNG - CÔNG TY AN TÍN")
    print("=" * 80)

    # 1. Khởi tạo & Tải dữ liệu
    benchmark_date_str = "2026-11-15"
    loader = DataLoader(data_dir="data", benchmark_date=benchmark_date_str)
    unified_df = loader.load_all()
    print(f"\n[1/6] Đã tải và đối soát thành công {len(unified_df)} hợp đồng theo ngày đối chiếu: {benchmark_date_str}")

    # 2. Khởi tạo các Agent chuyên trách
    audit_engine = AuditEngine(loader.service_packages, loader.discount_policies)
    health_scorer = HealthScorer()
    rec_engine = RecommendationEngine(loader.service_packages, loader.discount_policies)
    workflow_tracker = WorkflowTracker(benchmark_date=benchmark_date_str)

    # 3. Chạy quy trình phân tích và thẩm định trên từng hợp đồng
    print("[2/6] Đang chạy kiểm toán 4 sai phạm, chấm điểm sức khỏe và lập căn cứ đề xuất...")
    
    enriched_rows = []
    all_tasks = []
    audit_results_list = []

    err_count_upsell_with_ticket = 0
    err_count_seats_misalignment = 0
    err_count_missed_outreach = 0
    err_count_invalid_discount = 0

    for idx, row in unified_df.iterrows():
        # Bước 1: Rà soát 4 lỗi nghiệp vụ
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

        # Bước 2: Chấm điểm Sức khỏe & Dự báo Rủi ro
        health_info = health_scorer.compute_score(row)

        # Bước 3: Sinh đề xuất gói & ưu đãi hợp chuẩn
        rec_info = rec_engine.generate_recommendation(row, health_info, audit_res)

        # Bước 4: Điều phối theo 4 làn bơi BPMN & Tạo Task theo dõi
        wf_info = workflow_tracker.process_workflow(row, health_info, audit_res, rec_info)
        all_tasks.extend(wf_info["tasks"])

        # Tổng hợp dữ liệu chi tiết
        merged_row = {**row.to_dict(), **health_info, **rec_info, **wf_info}
        enriched_rows.append(merged_row)

    enriched_df = pd.DataFrame(enriched_rows)

    # 4. Tính toán số liệu thống kê tổng hợp (KPIs)
    total_current_arr = enriched_df["annual_contract_value"].sum()
    total_proposed_arr = enriched_df["net_proposed_arr"].sum()
    arr_growth_pct = ((total_proposed_arr - total_current_arr) / total_current_arr) * 100
    total_audited_violations = sum(1 for res in audit_results_list if res["violations_count"] > 0)
    total_at_risk = (enriched_df["churn_risk"].str.contains("Cao", na=False)).sum()

    # Thống kê phân bổ sức khỏe
    green_count = (enriched_df["health_tier"].str.contains("Xanh")).sum()
    yellow_count = (enriched_df["health_tier"].str.contains("Vàng")).sum()
    red_count = (enriched_df["health_tier"].str.contains("Đỏ")).sum()

    health_summary_rows = [
        ("Xanh (Healthy / Growth)", "Health Score >= 75, Active Users cao, không có sự cố", green_count, f"{green_count/120*100:.1f}%", f"{enriched_df[enriched_df['health_tier'].str.contains('Xanh')]['annual_contract_value'].sum():,.0f} VND", "Đề xuất mở rộng / Nâng gói Professional & Enterprise"),
        ("Vàng (Stable / Attention)", "Health Score 50-74, sử dụng ổn định, cần theo dõi", yellow_count, f"{yellow_count/120*100:.1f}%", f"{enriched_df[enriched_df['health_tier'].str.contains('Vàng')]['annual_contract_value'].sum():,.0f} VND", "Duy trì gói hiện tại, tặng ưu đãi gia hạn sớm hoặc cam kết nhiều năm"),
        ("Đỏ (At-Risk / Critical)", "Health Score < 50 hoặc có sự cố P1/P2 chưa đóng", red_count, f"{red_count/120*100:.1f}%", f"{enriched_df[enriched_df['health_tier'].str.contains('Đỏ')]['annual_contract_value'].sum():,.0f} VND", "Chặn tăng gói, tập trung xử lý dứt điểm ticket trong 24h & hỗ trợ thiện chí")
    ]

    summary_data = {
        "benchmark_date": benchmark_date_str,
        "total_contracts": len(enriched_df),
        "total_current_arr": total_current_arr,
        "total_proposed_arr": total_proposed_arr,
        "arr_growth_pct": arr_growth_pct,
        "total_audited_violations": total_audited_violations,
        "total_at_risk": total_at_risk,
        "err_upsell_with_ticket": err_count_upsell_with_ticket,
        "err_seats_misalignment": err_count_seats_misalignment,
        "err_missed_outreach": err_count_missed_outreach,
        "err_invalid_discount": err_count_invalid_discount,
        "health_summary_rows": health_summary_rows
    }

    # 5. Xuất báo cáo Excel
    print("[3/6] Đang xuất báo cáo chi tiết ra file Excel (5 Sheets định dạng chuẩn)...")
    excel_exporter = ExcelExporter(output_path="output/Bao_Cao_Gia_Han_Hop_Dong_An_Tin.xlsx")
    excel_exporter.export(
        summary_data,
        enriched_df,
        all_tasks,
        audit_results_list,
        loader.service_packages,
        loader.discount_policies
    )

    # 6. Xuất giao diện Dashboard tương tác
    print("[4/6] Đang xây dựng giao diện Dashboard HTML tương tác cao cấp...")
    html_gen = HTMLDashboardGenerator(output_path="output/Dashboard_Gia_Han_An_Tin.html")
    html_gen.generate(summary_data, enriched_df, all_tasks, audit_results_list)

    # 7. In tóm tắt báo cáo ra màn hình
    print("\n" + "=" * 80)
    print(" KẾT QUẢ VẬN HÀNH AI AGENT - CÔNG TY AN TÍN")
    print("=" * 80)
    print(f"• Tổng số hợp đồng rà soát kỳ này:           {len(enriched_df)} hợp đồng")
    print(f"• Tổng giá trị hợp đồng hiện tại (ARR cũ):   {total_current_arr:,.0f} VND")
    print(f"• Dự báo doanh thu gia hạn (Proposed ARR):   {total_proposed_arr:,.0f} VND ({arr_growth_pct:+.2f}%)")
    print(f"• Số hồ sơ rủi ro cao (At-Risk / Cảnh báo đỏ): {total_at_risk} khách hàng")
    print("-" * 80)
    print(" KẾT QUẢ PHÁT HIỆN & KHẮC PHỤC 4 SAI PHẠM CỐT TỬ CỦA NHÂN VIÊN:")
    print(f"  [1] Chặn Đề xuất Tăng gói khi còn sự cố P1/P2: {err_count_upsell_with_ticket} ca vi phạm -> Đã chặn và chuyển sang bảo vệ khách")
    print(f"  [2] Khắc phục Ảo tưởng số User (Active thấp):  {err_count_seats_misalignment} ca nhầm lẫn -> Đã đối soát đúng tỷ lệ sử dụng")
    print(f"  [3] Phát hiện Quá hạn bắt đầu liên hệ (30 ngày): {err_count_missed_outreach} ca chậm trễ -> Đã kích hoạt báo động đỏ liên hệ ngay")
    print(f"  [4] Hủy bỏ & Chuẩn hóa Ưu đãi sai quy chế:      {err_count_invalid_discount} ca sai phạm -> Đã tính lại chiết khấu hợp chuẩn")
    print("-" * 80)
    print(f"• Tổng số nhiệm vụ (Action Tasks) đã giao:    {len(all_tasks)} đầu việc (CSKH, Sales, Tech Support, Trưởng phòng)")
    print(f"• File Excel báo cáo: output/Bao_Cao_Gia_Han_Hop_Dong_An_Tin.xlsx")
    print(f"• Dashboard tương tác: output/Dashboard_Gia_Han_An_Tin.html")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()

