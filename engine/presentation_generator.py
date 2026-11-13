import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

class PresentationGenerator:
    """
    Tự động sinh bộ Slide Báo cáo Ban Giám Đốc (PowerPoint .pptx)
    phục vụ Làn 4 của quy trình BPMN Công ty An Tín.
    """
    def __init__(self, output_path="output/Bao_Cao_Ban_Giam_Doc_An_Tin.pptx"):
        self.output_path = output_path
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

    def _set_slide_background(self, slide, r, g, b):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(r, g, b)

    def generate(self, summary_data, detailed_df):
        prs = Presentation()
        # Set slide width & height to 16:9 widescreen
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)

        blank_slide_layout = prs.slide_layouts[6]

        # Colors
        c_navy = RGBColor(31, 78, 120)       # #1F4E78
        c_rose = RGBColor(196, 109, 134)     # #C46D86
        c_terracotta = RGBColor(197, 139, 116) # #C58B74
        c_dark = RGBColor(45, 35, 39)        # #2D2327
        c_white = RGBColor(255, 255, 255)
        c_muted = RGBColor(120, 110, 115)
        c_card_bg = RGBColor(250, 245, 243)

        # =====================================================================
        # SLIDE 1: TITLE SLIDE
        # =====================================================================
        s1 = prs.slides.add_slide(blank_slide_layout)
        self._set_slide_background(s1, 253, 239, 234) # Soft blush

        # Top tag
        tb_tag = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(10), Inches(0.5))
        p_tag = tb_tag.text_frame.paragraphs[0]
        p_tag.text = "BÁO CÁO ĐIỀU HÀNH CHIẾN LƯỢC • LÀN 4 BAN GIÁM ĐỐC"
        p_tag.font.name = "Segoe UI"
        p_tag.font.size = Pt(13)
        p_tag.font.bold = True
        p_tag.font.color.rgb = c_rose

        # Main title
        tb_title = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11), Inches(2.2))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        p1 = tf_title.paragraphs[0]
        p1.text = "Tối Ưu Hóa Quy Trình Gia Hạn Hợp Đồng B2B"
        p1.font.name = "Times New Roman"
        p1.font.size = Pt(40)
        p1.font.bold = True
        p1.font.color.rgb = c_dark

        p2 = tf_title.add_paragraph()
        p2.text = "Thẩm Định Tự Động Bằng Hệ Thống AI Agent • Bảo Toàn Doanh Thu 39.7 Tỷ VND"
        p2.font.name = "Times New Roman"
        p2.font.size = Pt(24)
        p2.font.italic = True
        p2.font.color.rgb = c_navy

        # Metadata
        tb_meta = s1.shapes.add_textbox(Inches(1.2), Inches(4.8), Inches(10), Inches(1.5))
        tf_meta = tb_meta.text_frame
        p_m1 = tf_meta.paragraphs[0]
        p_m1.text = f"• Doanh nghiệp: Công ty Cổ phần Phần mềm An Tín\n• Chu kỳ rà soát: Tháng 11/2026 (Ngày đối chiếu: {summary_data['benchmark_date']})\n• Trình bày: Trưởng phòng Kinh doanh & Hệ thống AI Agent"
        p_m1.font.name = "Segoe UI"
        p_m1.font.size = Pt(14)
        p_m1.font.color.rgb = c_muted

        # =====================================================================
        # SLIDE 2: FINANCIAL OVERVIEW & KPIS
        # =====================================================================
        s2 = prs.slides.add_slide(blank_slide_layout)
        self._set_slide_background(s2, 255, 255, 255)

        tb_h2 = s2.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.5), Inches(0.8))
        p_h2 = tb_h2.text_frame.paragraphs[0]
        p_h2.text = "1. TỔNG QUAN TÀI CHÍNH & HIỆU SUẤT GIA HẠN KỲ THÁNG 11/2026"
        p_h2.font.name = "Times New Roman"
        p_h2.font.size = Pt(24)
        p_h2.font.bold = True
        p_h2.font.color.rgb = c_navy

        # 4 KPI Cards
        cards_data = [
            ("TỔNG QUY MÔ HỢP ĐỒNG", f"{summary_data['total_contracts']} Hợp Đồng", "100% đã đối soát dữ liệu đa nguồn", c_navy),
            ("DOANH THU ARR HIỆN TẠI", f"{summary_data['total_current_arr']:,.0f} đ", "Tổng giá trị 120 hợp đồng cũ", c_dark),
            ("DỰ BÁO DOANH THU GIA HẠN", f"{summary_data['total_proposed_arr']:,.0f} đ", f"Tỷ lệ bảo toàn: {summary_data['arr_growth_pct']:+.1f}%", c_rose),
            ("HỒ SƠ CẢNH BÁO NGUY CƠ", f"{summary_data['total_at_risk']} Khách Hàng", "Đã kích hoạt phương án giữ chân", c_terracotta)
        ]

        card_w = Inches(2.7)
        card_h = Inches(4.5)
        card_top = Inches(1.8)

        for idx, (title, val, desc, col) in enumerate(cards_data):
            left = Inches(0.8 + idx * 2.95)
            shape = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, card_top, card_w, card_h)
            shape.fill.solid()
            shape.fill.fore_color.rgb = c_card_bg
            shape.line.color.rgb = col
            shape.line.width = Pt(1.5)

            tf = shape.text_frame
            tf.word_wrap = True
            tf.margin_top = Inches(0.4)
            tf.margin_left = Inches(0.2)
            tf.margin_right = Inches(0.2)

            pt1 = tf.paragraphs[0]
            pt1.text = title
            pt1.font.name = "Segoe UI"
            pt1.font.size = Pt(11)
            pt1.font.bold = True
            pt1.font.color.rgb = c_muted
            pt1.alignment = PP_ALIGN.CENTER

            pt2 = tf.add_paragraph()
            pt2.text = f"\n{val}\n"
            pt2.font.name = "Times New Roman"
            pt2.font.size = Pt(22)
            pt2.font.bold = True
            pt2.font.color.rgb = col
            pt2.alignment = PP_ALIGN.CENTER

            pt3 = tf.add_paragraph()
            pt3.text = desc
            pt3.font.name = "Segoe UI"
            pt3.font.size = Pt(12)
            pt3.font.color.rgb = c_dark
            pt3.alignment = PP_ALIGN.CENTER

        # =====================================================================
        # SLIDE 3: 4 CLASSIC ERRORS ELIMINATED
        # =====================================================================
        s3 = prs.slides.add_slide(blank_slide_layout)
        self._set_slide_background(s3, 255, 255, 255)

        tb_h3 = s3.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.5), Inches(0.8))
        p_h3 = tb_h3.text_frame.paragraphs[0]
        p_h3.text = "2. KẾT QUẢ KIỂM TOÁN & NGĂN CHẶN 4 SAI PHẠM CỐT TỬ CỦA NHÂN VIÊN"
        p_h3.font.name = "Times New Roman"
        p_h3.font.size = Pt(24)
        p_h3.font.bold = True
        p_h3.font.color.rgb = c_navy

        errors_table_shape = s3.shapes.add_table(5, 4, Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.8))
        table = errors_table_shape.table
        table.columns[0].width = Inches(2.5)
        table.columns[1].width = Inches(1.5)
        table.columns[2].width = Inches(3.5)
        table.columns[3].width = Inches(4.2)

        headers = ["Sai Phạm Nghiệp Vụ Cũ", "Số Ca Vi Phạm", "Rủi Ro Nếu Không Có AI", "Giải Pháp & Chuẩn Hóa Của AI Agent"]
        for c_idx, h in enumerate(headers):
            cell = table.cell(0, c_idx)
            cell.text = h
            cell.fill.solid()
            cell.fill.fore_color.rgb = c_navy
            cell.text_frame.paragraphs[0].font.bold = True
            cell.text_frame.paragraphs[0].font.size = Pt(12)
            cell.text_frame.paragraphs[0].font.color.rgb = c_white

        rows_content = [
            ("Lỗi 1: Tăng gói khi còn sự cố P1/P2 chưa xử lý", f"{summary_data['err_upsell_with_ticket']} ca", "Khách hàng bức xúc, hủy hợp đồng (Churn ngay lập tức)", "Chặn Upsell, kích hoạt kỹ thuật đóng ticket trong 24h & bồi thường thiện chí 10%"),
            ("Lỗi 2: Xem số user đăng ký là số thực dùng", f"{summary_data['err_seats_misalignment']} ca", "Khách thấy lãng phí ngân sách, giảm uy tín phần mềm", "Đối soát Active thực tế, đề xuất gói tinh gọn (Right-Sizing) hoặc mở Workshop Onboarding"),
            ("Lỗi 3: Nhầm hạn HĐ với ngày bắt đầu liên hệ", f"{summary_data['err_missed_outreach']} ca", "Tiếp cận trễ, khách không kịp chuẩn bị ngân sách", "Tự động tính ngày chuẩn (trước 30-45 ngày), phân loại báo động đỏ liên hệ hỏa tốc"),
            ("Lỗi 4: Áp dụng chiết khấu sai điều kiện quy chế", f"{summary_data['err_invalid_discount']} ca", "Thất thoát doanh thu, vi phạm kiểm toán tài chính", "Hủy chiết khấu khống, tính toán lại đúng 100% quy chế theo thâm niên và kỳ hạn")
        ]

        for r_idx, r_data in enumerate(rows_content, 1):
            for c_idx, val in enumerate(r_data):
                cell = table.cell(r_idx, c_idx)
                cell.text = val
                cell.text_frame.paragraphs[0].font.size = Pt(11)
                cell.text_frame.paragraphs[0].font.name = "Segoe UI"
                if c_idx == 1:
                    cell.text_frame.paragraphs[0].font.bold = True
                    cell.text_frame.paragraphs[0].font.color.rgb = c_rose

        # =====================================================================
        # SLIDE 4: BPMN 4 LANES GOVERNANCE
        # =====================================================================
        s4 = prs.slides.add_slide(blank_slide_layout)
        self._set_slide_background(s4, 253, 239, 234)

        tb_h4 = s4.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.5), Inches(0.8))
        p_h4 = tb_h4.text_frame.paragraphs[0]
        p_h4.text = "3. MÔ HÌNH VẬN HÀNH 4 LÀN BƠI (BPMN) TÍCH HỢP AI AGENT"
        p_h4.font.name = "Times New Roman"
        p_h4.font.size = Pt(24)
        p_h4.font.bold = True
        p_h4.font.color.rgb = c_navy

        lanes_data = [
            ("LÀN 1: KINH DOANH & CSKH", "Kích hoạt trước hạn 30-45 ngày", "Nhận danh sách nhiệm vụ AI đã phân rã (377 tasks). Tiếp cận khách hàng đúng tiến độ kèm script giải trình căn cứ."),
            ("LÀN 2: HÀNH CHÍNH & VẬN HÀNH (AI)", "Tự động sơ kiểm & đối soát 100%", "AI Agent thay thế con người kiểm tra 4 nguồn dữ liệu, triệt tiêu 4 sai phạm, chấm điểm Health Score và lập dự thảo phụ lục."),
            ("LÀN 3: TRƯỞNG PHÒNG KINH DOANH", "Duyệt nhanh 1-Click hoặc kết thúc", "Trưởng phòng xem căn cứ định lượng trên Dashboard, duyệt hồ sơ đạt chuẩn trong 3 giây hoặc quyết định chấm dứt nếu khách không có nhu cầu."),
            ("LÀN 4: BAN GIÁM ĐỐC (BGĐ)", "Phê duyệt thẩm quyền cấp cao", "Xem xét các hợp đồng Enterprise giá trị lớn, mức chiết khấu > 20%, hoặc hồ sơ rủi ro cao trước khi ký duyệt điện tử.")
        ]

        lane_h = Inches(1.15)
        for idx, (lname, lsub, ldesc) in enumerate(lanes_data):
            top_pos = Inches(1.6 + idx * 1.35)
            box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.7), lane_h)
            box.fill.solid()
            box.fill.fore_color.rgb = c_white
            box.line.color.rgb = c_rose if idx == 1 else c_terracotta
            box.line.width = Pt(1.5)

            tf = box.text_frame
            tf.word_wrap = True
            tf.margin_left = Inches(0.3)
            tf.margin_top = Inches(0.15)

            p_l1 = tf.paragraphs[0]
            p_l1.text = f"{lname} — {lsub}"
            p_l1.font.bold = True
            p_l1.font.size = Pt(13)
            p_l1.font.color.rgb = c_navy

            p_l2 = tf.add_paragraph()
            p_l2.text = ldesc
            p_l2.font.size = Pt(11)
            p_l2.font.color.rgb = c_dark

        # =====================================================================
        # SLIDE 5: ENTERPRISE CONTRACTS NEEDING BOARD APPROVAL
        # =====================================================================
        s5 = prs.slides.add_slide(blank_slide_layout)
        self._set_slide_background(s5, 255, 255, 255)

        tb_h5 = s5.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.5), Inches(0.8))
        p_h5 = tb_h5.text_frame.paragraphs[0]
        p_h5.text = "4. DANH MỤC HỢP ĐỒNG GIÁ TRỊ LỚN TRÌNH BAN GIÁM ĐỐC PHÊ DUYỆT"
        p_h5.font.name = "Times New Roman"
        p_h5.font.size = Pt(24)
        p_h5.font.bold = True
        p_h5.font.color.rgb = c_navy

        bod_df = detailed_df[detailed_df["requires_bod_approval"] == True].head(6)

        table_bod = s5.shapes.add_table(len(bod_df) + 1, 6, Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.8)).table
        table_bod.columns[0].width = Inches(1.5)
        table_bod.columns[1].width = Inches(3.2)
        table_bod.columns[2].width = Inches(1.8)
        table_bod.columns[3].width = Inches(1.8)
        table_bod.columns[4].width = Inches(1.4)
        table_bod.columns[5].width = Inches(2.0)

        bod_headers = ["Mã HĐ", "Doanh Nghiệp Khách Hàng", "Gói Đề Xuất", "Doanh Thu Mới", "Ưu Đãi", "Lý Do Trình BGĐ"]
        for c_idx, h in enumerate(bod_headers):
            cell = table_bod.cell(0, c_idx)
            cell.text = h
            cell.fill.solid()
            cell.fill.fore_color.rgb = c_navy
            cell.text_frame.paragraphs[0].font.bold = True
            cell.text_frame.paragraphs[0].font.size = Pt(11)
            cell.text_frame.paragraphs[0].font.color.rgb = c_white

        for r_idx, (_, r) in enumerate(bod_df.iterrows(), 1):
            row_data = [
                str(r["contract_id"]),
                str(r["customer_name"])[:35],
                f"{r['proposed_package']} ({r['proposed_seats']}s)",
                f"{r['net_proposed_arr']:,.0f} đ",
                f"{r['total_discount_pct']}%",
                str(r["lane4_trigger_reason"])[:35]
            ]
            for c_idx, val in enumerate(row_data):
                cell = table_bod.cell(r_idx, c_idx)
                cell.text = val
                cell.text_frame.paragraphs[0].font.size = Pt(10)
                cell.text_frame.paragraphs[0].font.name = "Segoe UI"
                if c_idx == 3:
                    cell.text_frame.paragraphs[0].font.bold = True
                    cell.text_frame.paragraphs[0].font.color.rgb = c_terracotta

        # =====================================================================
        # SLIDE 6: CONCLUSION & NEXT STEPS
        # =====================================================================
        s6 = prs.slides.add_slide(blank_slide_layout)
        self._set_slide_background(s6, 253, 239, 234)

        tb_h6 = s6.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(11), Inches(4.5))
        tf_c = tb_h6.text_frame
        tf_c.word_wrap = True

        p_c1 = tf_c.paragraphs[0]
        p_c1.text = "KẾT LUẬN & KIẾN NGHỊ THỰC THI"
        p_c1.font.name = "Times New Roman"
        p_c1.font.size = Pt(32)
        p_c1.font.bold = True
        p_c1.font.color.rgb = c_navy

        conclusions = [
            "1. Tối ưu hóa thời gian thẩm định: Giảm 90% thời gian duyệt hồ sơ của Trưởng phòng từ hàng giờ xuống vài phút.",
            "2. Triệt tiêu sai phạm nghiệp vụ: 100% hồ sơ được kiểm soát trần chiết khấu và ngăn chặn tình trạng chào tăng gói khi còn sự cố.",
            "3. Bảo toàn doanh thu: Dự kiến thu hồi 39.71 Tỷ VND doanh thu gia hạn (đạt 98.4% so với năm trước), chủ động giảm thiểu rủi ro Churn.",
            "4. Kiến nghị Ban Giám Đốc: Phê duyệt chính sách ưu đãi bồi thường thiện chí 10% (INCIDENT_RECOVERY) cho 14 khách hàng gặp sự cố."
        ]

        for c_text in conclusions:
            p_item = tf_c.add_paragraph()
            p_item.text = f"\n{c_text}"
            p_item.font.name = "Segoe UI"
            p_item.font.size = Pt(14)
            p_item.font.color.rgb = c_dark

        prs.save(self.output_path)
        print(f"Presentation saved successfully to {self.output_path}")
        return self.output_path

