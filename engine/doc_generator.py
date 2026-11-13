import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

class DocumentGenerator:
    """
    Tự động soạn thảo Phụ lục Hợp đồng gia hạn dịch vụ phần mềm (Word .docx)
    dựa trên đề xuất có căn cứ của AI Agent theo đúng Làn 3 của quy trình BPMN.
    """
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _set_cell_background(self, cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), fill_hex)
        tcPr.append(shd)

    def generate_contract_addendum(self, customer_record, file_name=None):
        doc = docx.Document()

        # Page margins
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(0.8)
            section.bottom_margin = Inches(0.8)
            section.left_margin = Inches(0.9)
            section.right_margin = Inches(0.9)

        # Header Title
        p_header = doc.add_paragraph()
        p_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_nation = p_header.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\nĐộc lập - Tự do - Hạnh phúc\n------------------------\n")
        run_nation.font.name = "Times New Roman"
        run_nation.font.size = Pt(12)
        run_nation.font.bold = True

        p_title = doc.add_paragraph()
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_title = p_title.add_run("PHỤ LỤC GIA HẠN HỢP ĐỒNG DỊCH VỤ PHẦN MỀM\n")
        run_title.font.name = "Times New Roman"
        run_title.font.size = Pt(15)
        run_title.font.bold = True
        run_title.font.color.rgb = RGBColor(31, 78, 120)

        run_sub = p_title.add_run(f"Số: PL-{customer_record['contract_id']}/AT-2026\n(Đính kèm theo Hợp đồng số: {customer_record['contract_id']})")
        run_sub.font.name = "Times New Roman"
        run_sub.font.size = Pt(11)
        run_sub.font.italic = True

        doc.add_paragraph()

        # Date & Introduction
        p_intro = doc.add_paragraph()
        p_intro.paragraph_format.line_spacing = 1.2
        r_intro = p_intro.add_run(
            "Hôm nay, ngày đối chiếu và thỏa thuận gia hạn tại trụ sở Công ty Cổ phần Phần mềm An Tín, chúng tôi gồm có:\n"
        )
        r_intro.font.name = "Times New Roman"
        r_intro.font.size = Pt(11)

        # Party A: An Tin
        p_party_a = doc.add_paragraph()
        p_party_a.paragraph_format.line_spacing = 1.2
        r_a_title = p_party_a.add_run("BÊN CUNG CẤP DỊCH VỤ (BÊN A): CÔNG TY CỔ PHẦN PHẦN MỀM AN TÍN\n")
        r_a_title.font.name = "Times New Roman"
        r_a_title.font.size = Pt(11)
        r_a_title.font.bold = True

        r_a_detail = p_party_a.add_run(
            "• Đại diện: Ông/Bà Trần Trưởng Phòng - Chức vụ: Trưởng phòng Kinh doanh (Ủy quyền BGĐ)\n"
            f"• Chuyên viên quản lý tài khoản (AM): {customer_record['account_manager']}\n"
            f"• Chuyên viên Chăm sóc khách hàng (CSM): {customer_record['csm_in_charge']}\n"
            "• Địa chỉ: Tầng 8, Tòa nhà Công nghệ An Tín, Hà Nội | Hotline: 1900 6868\n"
        )
        r_a_detail.font.name = "Times New Roman"
        r_a_detail.font.size = Pt(11)

        # Party B: Customer
        p_party_b = doc.add_paragraph()
        p_party_b.paragraph_format.line_spacing = 1.2
        r_b_title = p_party_b.add_run(f"BÊN KHÁCH HÀNG (BÊN B): {customer_record['customer_name'].upper()}\n")
        r_b_title.font.name = "Times New Roman"
        r_b_title.font.size = Pt(11)
        r_b_title.font.bold = True

        r_b_detail = p_party_b.add_run(
            f"• Mã khách hàng: {customer_record['customer_id']}\n"
            f"• Lĩnh vực hoạt động: {customer_record['industry']}\n"
            f"• Thâm niên đồng hành cùng An Tín: {customer_record['tenure_years']} năm liên tục\n"
        )
        r_b_detail.font.name = "Times New Roman"
        r_b_detail.font.size = Pt(11)

        # Terms Agreement
        p_terms_head = doc.add_paragraph()
        r_terms_head = p_terms_head.add_run("Hai bên cùng thỏa thuận và thống nhất ký kết Phụ lục hợp đồng gia hạn với các điều khoản sau:")
        r_terms_head.font.name = "Times New Roman"
        r_terms_head.font.size = Pt(11)
        r_terms_head.font.italic = True

        # Table of Terms
        table = doc.add_table(rows=7, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        headers = [
            ("Gói dịch vụ phần mềm gia hạn", f"{customer_record['proposed_package']} (Gói đề xuất tối ưu)"),
            ("Số lượng tài khoản (Seats) được cấp phép", f"{customer_record['proposed_seats']} tài khoản người dùng hoạt động"),
            ("Thời hạn hợp đồng gia hạn", "01 năm (12 tháng tiếp theo kể từ ngày hết hạn hợp đồng cũ)"),
            ("Đơn giá gốc niêm yết (Gross ARR)", f"{customer_record['gross_arr']:,.0f} VND / năm"),
            ("Chính sách ưu đãi hợp chuẩn áp dụng", f"{customer_record['applied_promos_str']} (Chiết khấu {customer_record['total_discount_pct']}%)"),
            ("Số tiền chiết khấu giảm trừ", f"-{customer_record['discount_amount']:,.0f} VND"),
            ("TỔNG GIÁ TRỊ GIA HẠN THANH TOÁN (NET ARR)", f"{customer_record['net_proposed_arr']:,.0f} VND (Chưa gồm VAT)")
        ]

        for i, (k, v) in enumerate(headers):
            row = table.rows[i]
            cell_k = row.cells[0]
            cell_v = row.cells[1]
            cell_k.width = Inches(2.6)
            cell_v.width = Inches(4.2)
            cell_k.text = k
            cell_v.text = v

            # Formatting
            for cell in [cell_k, cell_v]:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.name = "Times New Roman"
                        run.font.size = Pt(10.5)

            if i == 6:
                # Highlight last row
                self._set_cell_background(cell_k, "D9E1F2")
                self._set_cell_background(cell_v, "D9E1F2")
                cell_k.paragraphs[0].runs[0].font.bold = True
                cell_v.paragraphs[0].runs[0].font.bold = True
                cell_v.paragraphs[0].runs[0].font.color.rgb = RGBColor(31, 78, 120)

        doc.add_paragraph()

        # Section: AI Data-Driven Justification
        p_just = doc.add_paragraph()
        r_just_title = p_just.add_run("ĐIỀU KHOẢN CAM KẾT & CĂN CỨ ĐÁNH GIÁ CHẤT LƯỢNG:\n")
        r_just_title.font.name = "Times New Roman"
        r_just_title.font.size = Pt(11)
        r_just_title.font.bold = True

        r_just_body = p_just.add_run(
            f"1. Căn cứ hiệu quả khai thác: Khách hàng ghi nhận {customer_record['active_users_30d']}/{customer_record['registered_seats']} tài khoản "
            f"hoạt động ổn định ({customer_record['utilization_rate_pct']}%), dung lượng đạt {customer_record['storage_used_gb']} GB.\n"
            f"2. Cam kết chất lượng dịch vụ (SLA): An Tín cam kết thời gian hoạt động hệ thống đạt tối thiểu 99.5% và hỗ trợ kỹ thuật 24/7.\n"
            f"3. Phê duyệt thẩm quyền: Hồ sơ đã được Trưởng phòng Kinh doanh kiểm tra theo đúng Quy trình BPMN, "
            f"{'đã trình Ban Giám Đốc ký duyệt đặc cách.' if customer_record['requires_bod_approval'] else 'đủ thẩm quyền ban hành.'}\n"
        )
        r_just_body.font.name = "Times New Roman"
        r_just_body.font.size = Pt(10.5)

        # Signature blocks
        p_sig = doc.add_paragraph()
        p_sig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        table_sig = doc.add_table(rows=3, cols=2)
        table_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        c_sig_a = table_sig.rows[0].cells[0]
        c_sig_b = table_sig.rows[0].cells[1]
        c_sig_a.width = Inches(3.4)
        c_sig_b.width = Inches(3.4)

        c_sig_a.text = "ĐẠI DIỆN BÊN A\nCÔNG TY CỔ PHẦN PHẦN MỀM AN TÍN\n(Ký tên & đóng dấu)"
        c_sig_b.text = f"ĐẠI DIỆN BÊN B\n{customer_record['customer_name'].upper()}\n(Ký tên & đóng dấu)"

        c_sig_a.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        c_sig_b.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

        for row in table_sig.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for r in p.runs:
                        r.font.name = "Times New Roman"
                        r.font.size = Pt(11)
                        r.font.bold = True

        # Signer space
        table_sig.rows[1].cells[0].text = "\n\n\n"
        table_sig.rows[1].cells[1].text = "\n\n\n"

        table_sig.rows[2].cells[0].text = "TRẦN TRƯỞNG PHÒNG\n(Đã ký duyệt điện tử)"
        table_sig.rows[2].cells[1].text = "GIÁM ĐỐC ĐẠI DIỆN"
        table_sig.rows[2].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        table_sig.rows[2].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

        if not file_name:
            file_name = f"Phu_Luc_Gia_Han_{customer_record['customer_id']}.docx"
        out_file_path = os.path.join(self.output_dir, file_name)
        doc.save(out_file_path)
        return out_file_path

