import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

class ExcelExporter:
    """
    Xuất báo cáo thẩm định gia hạn và kế hoạch công việc ra file Excel chuyên nghiệp.
    """
    def __init__(self, output_path="output/Bao_Cao_Gia_Han_Hop_Dong_An_Tin.xlsx"):
        self.output_path = output_path

    def export(self, summary_data, detailed_df, tasks_list, audit_violations_list, packages_dict, policies_dict):
        wb = openpyxl.Workbook()
        # Remove default sheet
        wb.remove(wb.active)

        # Style definitions
        header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
        header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
        sub_header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
        sub_header_font = Font(name="Segoe UI", size=11, bold=True, color="1F4E78")
        title_font = Font(name="Segoe UI", size=16, bold=True, color="1F4E78")
        section_font = Font(name="Segoe UI", size=13, bold=True, color="203764")
        bold_font = Font(name="Segoe UI", size=10, bold=True)
        regular_font = Font(name="Segoe UI", size=10)
        center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
        left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
        right_align = Alignment(horizontal="right", vertical="center")
        thin_border = Border(
            left=Side(style='thin', color='D9D9D9'),
            right=Side(style='thin', color='D9D9D9'),
            top=Side(style='thin', color='D9D9D9'),
            bottom=Side(style='thin', color='D9D9D9')
        )

        # =====================================================================
        # SHEET 1: TỔNG QUAN DASHBOARD
        # =====================================================================
        ws1 = wb.create_sheet(title="Tong_Quan_Dashboard")
        ws1.views.sheetView[0].showGridLines = True
        
        # Title
        ws1.merge_cells("A1:G1")
        ws1["A1"] = "BÁO CÁO TỔNG QUAN QUY TRÌNH GIA HẠN HỢP ĐỒNG - CÔNG TY AN TÍN"
        ws1["A1"].font = title_font
        ws1["A1"].alignment = Alignment(horizontal="left", vertical="center")
        ws1.row_dimensions[1].height = 35

        ws1.merge_cells("A2:G2")
        ws1["A2"] = f"Hệ thống AI Agent thẩm định tự động | Ngày đối chiếu chuẩn: {summary_data['benchmark_date']} | Tổng số hợp đồng: {summary_data['total_contracts']}"
        ws1["A2"].font = Font(name="Segoe UI", size=10, italic=True, color="595959")
        ws1.row_dimensions[2].height = 20

        # KPI Cards (Rows 4-7)
        kpi_metrics = [
            ("A4:B5", "A4", "TỔNG GIÁ TRỊ HỢP ĐỒNG CŨ (ARR CŨ)", f"{summary_data['total_current_arr']:,.0f} VND", "D9E1F2", "1F4E78"),
            ("C4:D5", "C4", "DOANH THU DỰ KIẾN (PROPOSED ARR)", f"{summary_data['total_proposed_arr']:,.0f} VND", "E2EFDA", "375623"),
            ("E4:E5", "E4", "TỶ LỆ TĂNG TRƯỞNG / BẢO TOÀN", f"{summary_data['arr_growth_pct']:+.1f}%", "FCE4D6", "C65911"),
            ("F4:G5", "F4", "SỐ HỒ SƠ PHÁT HIỆN SAI SÓT", f"{summary_data['total_audited_violations']} / {summary_data['total_contracts']} HĐ", "FFF2CC", "7F6000")
        ]

        for merge_range, top_left, label, val, bg_col, txt_col in kpi_metrics:
            ws1.merge_cells(merge_range)
            cell = ws1[top_left]
            cell.value = f"{label}\n{val}"
            cell.font = Font(name="Segoe UI", size=12, bold=True, color=txt_col)
            cell.fill = PatternFill(start_color=bg_col, end_color=bg_col, fill_type="solid")
            cell.alignment = center_align

        ws1.row_dimensions[4].height = 25
        ws1.row_dimensions[5].height = 25

        # Section: Báo cáo kết quả xử lý 4 sai sót nghiệp vụ cốt tử
        ws1.cell(row=8, column=1, value="1. KẾT QUẢ RÀ SOÁT & NGĂN CHẶN 4 LỖI NGHIỆP VỤ KINH ĐIỂN TỪ NHÂN VIÊN").font = section_font
        ws1.row_dimensions[8].height = 25

        audit_headers = ["Mã Lỗi", "Tên Sai Phạm Nghiệp Vụ Cần Xử Lý", "Số Ca Phát Hiện", "Tác Động Nghiêm Trọng", "Cơ Chế Khắc Phục Của AI Agent"]
        for col_idx, h_text in enumerate(audit_headers, 1):
            c = ws1.cell(row=9, column=col_idx, value=h_text)
            c.font = header_font
            c.fill = header_fill
            c.alignment = center_align
            c.border = thin_border
        ws1.row_dimensions[9].height = 28

        audit_rows_data = [
            ("LỖI 01", "Đề xuất tăng gói (Upsell) khi còn sự cố P1/P2 chưa giải quyết", summary_data["err_upsell_with_ticket"], "Khách bức xúc, hủy hợp đồng (Churn ngay lập tức)", "Tự động CHẶN TĂNG GÓI, ưu tiên kỹ thuật đóng ticket trong 24h & áp dụng chính sách bồi hoàn thiện chí."),
            ("LỖI 02", "Ảo tưởng số user: Xem số đăng ký là số thực dùng (Active Users)", summary_data["err_seats_misalignment"], "Khách thấy lãng phí ngân sách, giảm uy tín phần mềm", "Đối soát log sử dụng thực tế. Đề xuất gói tinh gọn (Right-Sizing) hoặc kích hoạt workshop đào tạo Onboarding."),
            ("LỖI 03", "Nhầm ngày hết hạn hợp đồng với ngày cần bắt đầu liên hệ", summary_data["err_missed_outreach"], "Liên hệ trễ, không kịp làm thủ tục, đối thủ nhảy vào", "Tự động tính ngày liên hệ chuẩn (trước 30-45 ngày), phân loại báo động đỏ quá hạn để tiếp cận khẩn cấp."),
            ("LỖI 04", "Áp dụng chính sách ưu đãi không đúng điều kiện quy chế", summary_data["err_invalid_discount"], "Thất thoát doanh thu, vi phạm kiểm toán tài chính", "Hủy bỏ chiết khấu sai, tự động tính lại chiết khấu hợp lệ chuẩn xác theo thâm niên, cam kết và kỳ hạn.")
        ]

        for r_idx, r_data in enumerate(audit_rows_data, 10):
            for c_idx, val in enumerate(r_data, 1):
                c = ws1.cell(row=r_idx, column=c_idx, value=val)
                c.font = regular_font
                c.alignment = center_align if c_idx in [1, 3] else left_align
                c.border = thin_border
            ws1.row_dimensions[r_idx].height = 24

        # Section: Phân loại sức khỏe & Rủi ro rời bỏ
        ws1.cell(row=16, column=1, value="2. PHÂN BỔ SỨC KHỎE KHÁCH HÀNG & RỦI RO RỜI BỎ (HEALTH SCORE & CHURN RISK)").font = section_font
        ws1.row_dimensions[16].height = 25

        health_headers = ["Phân Loại Sức Khỏe", "Mô Tả Tiêu Chí", "Số Khách Hàng", "Tỷ Lệ %", "Tổng ARR Hiện Tại", "Hành Động Trọng Tâm"]
        for col_idx, h_text in enumerate(health_headers, 1):
            c = ws1.cell(row=17, column=col_idx, value=h_text)
            c.font = header_font
            c.fill = header_fill
            c.alignment = center_align
            c.border = thin_border
        ws1.row_dimensions[17].height = 28

        for r_idx, r_data in enumerate(summary_data["health_summary_rows"], 18):
            for c_idx, val in enumerate(r_data, 1):
                c = ws1.cell(row=r_idx, column=c_idx, value=val)
                c.font = regular_font
                c.alignment = center_align if c_idx in [1, 3, 4] else (right_align if c_idx == 5 else left_align)
                c.border = thin_border
            ws1.row_dimensions[r_idx].height = 24

        # =====================================================================
        # SHEET 2: DANH SÁCH GIA HẠN CHI TIẾT (120 HỢP ĐỒNG)
        # =====================================================================
        ws2 = wb.create_sheet(title="Danh_Sach_Gia_Han_Chi_Tiet")
        ws2.views.sheetView[0].showGridLines = True

        detail_headers = [
            "Mã HĐ", "Mã KH", "Tên Doanh Nghiệp Khách Hàng", "Ngành Nghề", "Gói Hiện Tại", "Hạn Hợp Đồng", "Còn (Ngày)", 
            "Ngày Cần Liên Hệ", "Tiến Độ Liên Hệ", "Tài Khoản Mua", "Active 30d", "Tỷ Lệ Dùng %", "Sự Cố P1/P2 Mở", 
            "Điểm CSAT", "Điểm Sức Khỏe", "Phân Loại Rủi Ro", "Chiến Lược Đề Xuất", "Gói Đề Xuất", "Số Ghế Đề Xuất", 
            "Ưu Đãi Hợp Lệ", "Chiết Khấu %", "Doanh Thu Đề Xuất (VND)", "Chênh Lệch ARR", "Thẩm Quyền BGĐ", 
            "Làn 2: Hành Chính Sơ Bộ", "Làn 3: Trưởng Phòng Duyệt", "Làn 4: BGĐ Phê Duyệt", "Căn Cứ Đề Xuất Chi Tiết"
        ]

        for col_idx, h_text in enumerate(detail_headers, 1):
            c = ws2.cell(row=1, column=col_idx, value=h_text)
            c.font = header_font
            c.fill = header_fill
            c.alignment = center_align
            c.border = thin_border
        ws2.row_dimensions[1].height = 32

        for r_idx, row in detailed_df.iterrows():
            row_num = r_idx + 2
            values = [
                row["contract_id"], row["customer_id"], row["customer_name"], row["industry"], row["current_package"],
                row["contract_end_date"].strftime("%d/%m/%Y"), row["days_until_expiry"],
                row["target_contact_date"].strftime("%d/%m/%Y"), 
                "QUÁ HẠN" if row["days_until_contact_due"] < 0 else f"Còn {row['days_until_contact_due']} ngày",
                row["registered_seats"], row["active_users_30d"], f"{row['utilization_rate_pct']:.1f}%",
                row["p1_p2_open_tickets"], f"{row['avg_csat']:.1f}", row["health_score"], row["churn_risk"],
                row["strategy_name"], row["proposed_package"], row["proposed_seats"],
                row["applied_promos_str"], f"{row['total_discount_pct']}%",
                f"{row['net_proposed_arr']:,.0f}", f"{row['arr_variance']:+,.0f}",
                "Cần BGĐ Duyệt" if row["requires_bod_approval"] else "Trưởng Phòng Đủ Quyền",
                row["lane2_prescreen_status"], row["lane3_manager_decision"], row["lane4_status"],
                row["full_rationale"]
            ]
            for col_idx, val in enumerate(values, 1):
                c = ws2.cell(row=row_num, column=col_idx, value=val)
                c.font = regular_font
                c.border = thin_border
                if col_idx in [1, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 21, 24, 25, 26, 27]:
                    c.alignment = center_align
                elif col_idx in [22, 23]:
                    c.alignment = right_align
                else:
                    c.alignment = left_align

                # Conditional color formatting
                if col_idx == 9 and "QUÁ HẠN" in str(val):
                    c.fill = PatternFill(start_color="FCE4D6", fill_type="solid")
                    c.font = Font(name="Segoe UI", size=10, bold=True, color="C00000")
                elif col_idx == 13 and int(row["p1_p2_open_tickets"]) > 0:
                    c.fill = PatternFill(start_color="FFC7CE", fill_type="solid")
                    c.font = Font(name="Segoe UI", size=10, bold=True, color="9C0006")
                elif col_idx == 15:
                    score = int(row["health_score"])
                    if score >= 75:
                        c.fill = PatternFill(start_color="C6EFCE", fill_type="solid")
                    elif score >= 50:
                        c.fill = PatternFill(start_color="FFEB9C", fill_type="solid")
                    else:
                        c.fill = PatternFill(start_color="FFC7CE", fill_type="solid")
            ws2.row_dimensions[row_num].height = 22

        # =====================================================================
        # SHEET 3: KẾ HOẠCH THEO DÕI TỪNG KHÁCH (ACTION TASKS)
        # =====================================================================
        ws3 = wb.create_sheet(title="Ke_Hoach_Theo_Doi_Tung_Khach")
        ws3.views.sheetView[0].showGridLines = True

        task_headers = [
            "STT", "Mã KH", "Tên Khách Hàng", "Bộ Phận Đảm Nhận", "Nhân Viên Chịu Trách Nhiệm",
            "Tên Nhiệm Vụ Cụ Thể", "Mức Độ Khẩn Cấp", "Hạn Chót (Deadline)", "Giai Đoạn Quy Trình", "Hướng Dẫn Thực Hiện Chi Tiết"
        ]

        for col_idx, h_text in enumerate(task_headers, 1):
            c = ws3.cell(row=1, column=col_idx, value=h_text)
            c.font = header_font
            c.fill = header_fill
            c.alignment = center_align
            c.border = thin_border
        ws3.row_dimensions[1].height = 32

        for t_idx, task in enumerate(tasks_list, 1):
            row_num = t_idx + 1
            t_values = [
                t_idx, task["customer_id"], task["customer_name"], task["role"], task["assignee"],
                task["task_title"], task["urgency"], task["due_date"], task["workflow_stage"], task["instructions"]
            ]
            for col_idx, val in enumerate(t_values, 1):
                c = ws3.cell(row=row_num, column=col_idx, value=val)
                c.font = regular_font
                c.border = thin_border
                if col_idx in [1, 2, 4, 7, 8, 9]:
                    c.alignment = center_align
                else:
                    c.alignment = left_align

                if "HỎA TỐC" in str(task["urgency"]):
                    c.fill = PatternFill(start_color="FCE4D6", fill_type="solid")
                    c.font = Font(name="Segoe UI", size=10, bold=True, color="C00000")
            ws3.row_dimensions[row_num].height = 24

        # =====================================================================
        # SHEET 4: NHẬT KÝ KIỂM TRA LỖI AI (AUDIT LOGS)
        # =====================================================================
        ws4 = wb.create_sheet(title="Nhat_Ky_Kiem_Tra_Loi_AI")
        ws4.views.sheetView[0].showGridLines = True

        audit_log_headers = [
            "STT", "Mã HĐ", "Mã KH", "Mã Lỗi", "Mức Độ", "Tiêu Đề Sai Sót", "Chi Tiết Phát Hiện", "Biện Pháp AI Đã Khắc Phục"
        ]

        for col_idx, h_text in enumerate(audit_log_headers, 1):
            c = ws4.cell(row=1, column=col_idx, value=h_text)
            c.font = header_font
            c.fill = header_fill
            c.alignment = center_align
            c.border = thin_border
        ws4.row_dimensions[1].height = 32

        stt = 1
        for item in audit_violations_list:
            for v in item["violations"]:
                row_num = stt + 1
                v_vals = [
                    stt, item["contract_id"], item["customer_id"], v["error_code"], v["severity"],
                    v["title"], v["detail"], v["corrective_action"]
                ]
                for col_idx, val in enumerate(v_vals, 1):
                    c = ws4.cell(row=row_num, column=col_idx, value=val)
                    c.font = regular_font
                    c.border = thin_border
                    if col_idx in [1, 2, 3, 4, 5]:
                        c.alignment = center_align
                    else:
                        c.alignment = left_align
                    if v["severity"] == "CRITICAL":
                        c.fill = PatternFill(start_color="FFC7CE", fill_type="solid")
                ws4.row_dimensions[row_num].height = 24
                stt += 1

        # =====================================================================
        # SHEET 5: BẢNG GIÁ & CHÍNH SÁCH QUY CHUẨN
        # =====================================================================
        ws5 = wb.create_sheet(title="Bang_Gia_Chinh_Sach_Chuan")
        ws5.views.sheetView[0].showGridLines = True

        ws5.merge_cells("A1:E1")
        ws5["A1"] = "DANH MỤC GÓI PHẦN MỀM & QUY CHẾ ƯU ĐÃI CHUẨN - CÔNG TY AN TÍN"
        ws5["A1"].font = title_font
        ws5["A1"].alignment = left_align

        ws5.cell(row=3, column=1, value="1. BẢNG GIÁ DỊCH VỤ PHẦN MỀM HIỆN HÀNH").font = section_font
        pkg_headers = ["Tên Gói", "Định Mức Seats", "Đơn Giá / Seat / Tháng", "Đơn Giá / Seat / Năm", "Dung Lượng", "Cam Kết SLA"]
        for col_idx, h_text in enumerate(pkg_headers, 1):
            c = ws5.cell(row=4, column=col_idx, value=h_text)
            c.font = header_font
            c.fill = header_fill
            c.alignment = center_align
            c.border = thin_border

        pkg_rows = [
            ("Standard", "10 - 30 seats", "250,000 VND", "3,000,000 VND", "50 GB", "99.0%"),
            ("Professional", "31 - 100 seats", "450,000 VND", "5,400,000 VND", "200 GB", "99.5%"),
            ("Enterprise", "101+ seats", "700,000 VND", "8,400,000 VND", "1,000 GB+", "99.9% (Dedicated Support)")
        ]
        for r_idx, r_data in enumerate(pkg_rows, 5):
            for c_idx, val in enumerate(r_data, 1):
                c = ws5.cell(row=r_idx, column=c_idx, value=val)
                c.font = regular_font
                c.alignment = center_align if c_idx in [1, 2, 5, 6] else right_align
                c.border = thin_border

        ws5.cell(row=9, column=1, value="2. CHÍNH SÁCH CHIẾT KHẤU & ĐIỀU KIỆN ÁP DỤNG").font = section_font
        pol_headers = ["Mã Ưu Đãi", "Tên Chính Sách", "Mức Giảm %", "Điều Kiện Áp Dụng Bắt Buộc", "Thẩm Quyền Phê Duyệt"]
        for col_idx, h_text in enumerate(pol_headers, 1):
            c = ws5.cell(row=10, column=col_idx, value=h_text)
            c.font = header_font
            c.fill = header_fill
            c.alignment = center_align
            c.border = thin_border

        pol_rows = [
            ("EARLY_BIRD", "Gia hạn sớm", "10%", "Ký gia hạn trước hạn hợp đồng >= 25 ngày", "Trưởng phòng duyệt"),
            ("MULTI_YEAR_2", "Cam kết 2 năm", "15%", "Ký hợp đồng trả trước 2 năm liên tục", "Trưởng phòng duyệt"),
            ("MULTI_YEAR_3", "Cam kết 3 năm", "20%", "Ký hợp đồng trả trước 3 năm liên tục", "Trưởng phòng duyệt"),
            ("LOYALTY_TIER_1", "Thân thiết (2-3 năm)", "5%", "Khách hàng hợp tác liên tục 2 đến dưới 4 năm", "Trưởng phòng duyệt"),
            ("LOYALTY_TIER_2", "Đồng hành Vàng (>= 4 năm)", "8%", "Khách hàng hợp tác liên tục từ 4 năm trở lên", "Trưởng phòng duyệt"),
            ("INCIDENT_RECOVERY", "Hỗ trợ Thiện chí Sự cố", "10%", "Có sự cố P1/P2 trong kỳ trước (đã khắc phục xong và ký cam kết SLA mới)", "Trưởng phòng & BGĐ"),
            ("GOVERNANCE", "Hạn mức tối đa", "Tối đa 25%", "Tổng cộng gộp không quá 25%. Mọi mức chiết khấu > 20% bắt buộc phải có phê duyệt của Ban Giám Đốc", "Ban Giám Đốc (BGĐ)")
        ]
        for r_idx, r_data in enumerate(pol_rows, 11):
            for c_idx, val in enumerate(r_data, 1):
                c = ws5.cell(row=r_idx, column=c_idx, value=val)
                c.font = regular_font
                c.alignment = center_align if c_idx in [1, 3] else left_align
                c.border = thin_border

        # Auto-adjust column widths for all sheets
        for sheet in wb.worksheets:
            for col in sheet.columns:
                max_len = 0
                col_letter = get_column_letter(col[0].column)
                for cell in col:
                    if cell.value:
                        val_str = str(cell.value)
                        # Check first line if multiline
                        first_line = val_str.split("\n")[0]
                        max_len = max(max_len, len(first_line))
                sheet.column_dimensions[col_letter].width = min(50, max(12, max_len + 3))

        wb.save(self.output_path)
        print(f"Excel report saved successfully to {self.output_path}")

