import time
import sys

def print_agent_msg(agent_name, role_color, msg, delay=0.4):
    print(f"\n[{agent_name}]:")
    print(f"  {msg}")
    time.sleep(delay)

def simulate_case_1():
    print("\n" + "=" * 80)
    print(" KỊCH BẢN MÔ PHỎNG 1: XỬ LÝ KHÁCH HÀNG CÓ SỰ CỐ TỒN ĐỌNG (ERR_01)")
    print(" Khách hàng: KH-1007 (Hợp đồng HD-2025-007) - Gói Professional (50 seats)")
    print("=" * 80)

    print_agent_msg("🤖 DataIntegrationAgent", "CYAN", 
        "Đã đối chiếu dữ liệu đến ngày 15/11/2026: Hợp đồng HD-2025-007 còn 8 ngày là hết hạn. "
        "Số tài khoản mua: 50 seats, Active: 40 users. Nhưng phát hiện Ticket TK-1015 (P1 - Critical): "
        "'Lỗi đồng bộ dữ liệu hóa đơn điện tử' đang ở trạng thái In_Progress từ 5 ngày trước!")

    print_agent_msg("💼 SalesAgent (Nhân viên Kinh doanh)", "BLUE", 
        "Khách hàng này dùng 40/50 tài khoản, dung lượng đạt 85%. Tôi đề xuất nâng cấp họ lên gói Enterprise (105 seats) "
        "với doanh thu dự kiến 882 triệu VND để hoàn thành chỉ tiêu doanh số quý này!")

    print_agent_msg("🛡️ AuditComplianceAgent (Agent Kiểm Toán)", "RED", 
        "DỪNG LẠI! CẢNH BÁO VI PHẠM NGUYÊN TẮC KINH DOANH SỐ 1! "
        "Khách hàng đang có ticket P1 nghiêm trọng chưa giải quyết xong, điểm CSAT giảm xuống còn 2.0/5. "
        "Nếu chào gói cao cấp lúc này, khách sẽ phản ứng tiêu cực và hủy hợp đồng ngay lập tức. "
        "Tôi kích hoạt LỆNH CHẶN TĂNG GÓI (Block Upsell)!")

    print_agent_msg("🔧 SupportLeadAgent (Agent Kỹ Thuật)", "YELLOW", 
        "Chúng tôi nhận trách nhiệm. Tôi đã chỉ đạo kỹ sư Senior fix lỗi đồng bộ API trong vòng 6 giờ tới, "
        "và sẽ cùng CSKH kiểm tra trực tiếp với bộ phận kế toán của khách để đóng ticket dứt điểm.")

    print_agent_msg("🤝 CSMAgent (Chăm Sóc Khách Hàng)", "MAGENTA", 
        "Đồng ý. Tôi đã liên hệ Giám đốc Vận hành của khách để xin lỗi chân thành, thông báo tiến độ fix lỗi, "
        "và xin áp dụng chính sách 'INCIDENT_RECOVERY' (Chiết khấu thiện chí 10%) để tri ân sự kiên nhẫn của họ.")

    print_agent_msg("👔 SalesManagerAgent (Trưởng Phòng Kinh Doanh - Làn 3)", "GREEN", 
        "QUYẾT ĐỊNH CỦA TRƯỞNG PHÒNG: Phê duyệt phương án của Audit và CSKH! "
        "Tạm hoãn đề xuất Enterprise, giữ nguyên gói Professional (50 seats) có chiết khấu bồi thường 10%. "
        "Ký cam kết chất lượng dịch vụ SLA 99.9%. Chuyển dự thảo phụ lục lên Ban Giám Đốc.")

def simulate_case_2():
    print("\n" + "=" * 80)
    print(" KỊCH BẢN MÔ PHỎNG 2: XỬ LÝ ẢO TƯỞNG SỐ USER & TỐI ƯU HÓA LICENSE (ERR_02)")
    print(" Khách hàng: KH-1015 (Hợp đồng HD-2025-015) - Gói Professional (70 seats)")
    print("=" * 80)

    print_agent_msg("🤖 DataIntegrationAgent", "CYAN", 
        "Hợp đồng KH-1015 đăng ký mua 70 tài khoản. Nhưng qua nhật ký 30 ngày qua, chỉ có 14 người đăng nhập (Đạt 20.0%). "
        "Xu hướng sử dụng: Suy giảm liên tục trong 3 tháng.")

    print_agent_msg("💼 SalesAgent (Nhân viên Kinh doanh)", "BLUE", 
        "Nhân viên cũ báo cáo khách hàng có 70 user nên tôi đang chuẩn bị báo giá gia hạn giữ nguyên 70 seats (378 triệu VND).")

    print_agent_msg("📊 UsageAnalysisAgent (Agent Phân Tích Hành Vi)", "YELLOW", 
        "CẢNH BÁO ẢO TƯỞNG TÀI NGUYÊN (Ghost Licenses): Khách hàng đang lãng phí 80% chi phí phần mềm! "
        "Nếu gửi báo giá 378 triệu, CFO của họ chắc chắn sẽ từ chối phê duyệt ngân sách và cắt hợp đồng.")

    print_agent_msg("🤝 CSMAgent (Chăm Sóc Khách Hàng)", "MAGENTA", 
        "Tôi đã tìm hiểu: Khách hàng chỉ mới triển khai cho khối Kinh doanh, khối Kho vận và Kế toán chưa được đào tạo. "
        "Tôi đề xuất 2 phương án: "
        "PA1: Tinh gọn xuống 25 seats (Right-Sizing) phù hợp quy mô thực tế. "
        "PA2: Duy trì 70 seats nhưng An Tín tặng kèm gói Onboarding Workshop đào tạo tận nơi 2 tuần.")

    print_agent_msg("👔 SalesManagerAgent (Trưởng Phòng Kinh Doanh - Làn 3)", "GREEN", 
        "QUYẾT ĐỊNH CỦA TRƯỞNG PHÒNG: Đồng ý với PA2 kèm điều kiện linh hoạt. "
        "Gửi khách thư đề xuất gia hạn nhấn mạnh cam kết đồng hành đào tạo, bảo vệ toàn vẹn tài khoản doanh nghiệp. "
        "Giao CSM Thảo hoàn thành workshop trước ngày 25/11.")

def simulate_case_3():
    print("\n" + "=" * 80)
    print(" KỊCH BẢN MÔ PHỎNG 3: KHÁCH HÀNG TĂNG TRƯỞNG MẠNH MẼ - NÂNG CẤP ENTERPRISE (HEALTHY)")
    print(" Khách hàng: KH-1025 (Hợp đồng HD-2025-025) - Gói Professional (80 seats)")
    print("=" * 80)

    print_agent_msg("🤖 DataIntegrationAgent", "CYAN", 
        "Khách hàng thâm niên 3 năm. Đăng ký 80 seats, Active 78/80 users (97.5%). "
        "Dung lượng lưu trữ đạt 92% hạn mức (184/200 GB). Không có sự cố nào trong 90 ngày qua. CSAT đạt 5.0/5 tuyệt đối!")

    print_agent_msg("🛡️ AuditComplianceAgent (Agent Kiểm Toán)", "GREEN", 
        "Hồ sơ VÀNG! Đạt chuẩn 100% các tiêu chí tăng trưởng: "
        "Health Score 96/100, đủ điều kiện hưởng Early Bird 10% (còn 28 ngày hết hạn) + Loyalty Tier 1 (5%). "
        "Tổng chiết khấu 15% hoàn toàn hợp lệ trong thẩm quyền.")

    print_agent_msg("💼 SalesAgent (Nhân viên Kinh doanh)", "BLUE", 
        "Tuyệt vời! Tôi đề xuất nâng cấp lên gói Enterprise (120 seats), mở rộng dung lượng lên 1,000 GB "
        "và tích hợp hệ thống tổng đài tự động. Doanh thu tăng từ 432 triệu lên 856 triệu VND sau ưu đãi!")

    print_agent_msg("👔 SalesManagerAgent (Trưởng Phòng Kinh Doanh - Làn 3)", "GREEN", 
        "DUYỆT NHANH 1-CLICK! Đây là khách hàng mẫu mực (Champion). "
        "Chuyển ngay hồ sơ sang Làn 4 để Ban Giám Đốc ký quyết định ưu đãi đặc cách cấp Enterprise!")

def main():
    print("=" * 80)
    print(" MÔ PHỎNG HỘI THOẠI ĐIỀU PHỐI MULTI-AGENT - CÔNG TY AN TÍN")
    print("=" * 80)
    simulate_case_1()
    simulate_case_2()
    simulate_case_3()
    print("\n" + "=" * 80)
    print(" KẾT THÚC MÔ PHỎNG - CÁC AGENT ĐÃ THỐNG NHẤT 100% CĂN CỨ VÀ HÀNH ĐỘNG!")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()

