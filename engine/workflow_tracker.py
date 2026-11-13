from datetime import datetime, timedelta

class WorkflowTracker:
    """
    Quản lý luồng vận hành theo đúng Sơ đồ quy trình BPMN của Công ty An Tín:
    - Làn 1: Nhân viên Kinh doanh / CSKH
    - Làn 2: Phòng Hành chính - Vận hành (Sơ bộ hồ sơ)
    - Làn 3: Trưởng bộ phận (Đánh giá & Duyệt đề xuất)
    - Làn 4: Ban Giám Đốc (Ký duyệt Hợp đồng / Phụ lục)
    Sinh danh sách công việc (Action Tasks) theo dõi chi tiết cho từng khách hàng.
    """
    def __init__(self, benchmark_date="2026-11-15"):
        self.benchmark_date = datetime.strptime(benchmark_date, "%Y-%m-%d")

    def process_workflow(self, row, health_info, audit_result, rec_info):
        cid = row["customer_id"]
        cname = row["customer_name"]
        sales_rep = row["account_manager"]
        csm_rep = row["csm_in_charge"]
        days_to_expiry = row["days_until_expiry"]
        days_to_contact = row["days_until_contact_due"]
        strategy = rec_info["strategy"]
        has_critical = row["has_unresolved_critical_incident"]

        # =====================================================================
        # 1. LÀN 2: ĐÁNH GIÁ SƠ BỘ (PHÒNG HÀNH CHÍNH - VẬN HÀNH / AI ENGINE)
        # =====================================================================
        if audit_result["violations_count"] == 0 and not has_critical:
            lane2_prescreen_status = "ĐẠT - HỒ SƠ HỢP LỆ"
            lane2_note = "Hồ sơ đầy đủ, số liệu sử dụng khớp thực tế, chính sách ưu đãi đúng quy chế."
        elif audit_result["violations_count"] > 0 and not has_critical:
            lane2_prescreen_status = "ĐẠT SAU ĐIỀU CHỈNH (AI REVISED)"
            lane2_note = f"Đã tự động chuẩn hóa {audit_result['violations_count']} sai sót của nhân viên. Hồ sơ đã sẵn sàng trình duyệt."
        else:
            lane2_prescreen_status = "CẢNH BÁO NGUY CƠ - CẦN XỬ LÝ SỰ CỐ"
            lane2_note = "Phát hiện sự cố P1/P2 chưa đóng. Yêu cầu ưu tiên xử lý dứt điểm trước khi chốt hợp đồng."

        # =====================================================================
        # 2. LÀN 3: TRƯỞNG BỘ PHẬN ĐÁNH GIÁ & DUYỆT ĐỀ XUẤT
        # =====================================================================
        # Nếu khách hàng có tỷ lệ active < 20% và không có thiện chí duy trì -> Cân nhắc Chấm dứt HĐ
        if health_info["health_score"] < 25 and row["utilization_rate_pct"] < 20:
            lane3_manager_decision = "CÂN NHẮC CHẤM DỨT HỢP ĐỒNG (OFFBOARDING)"
            lane3_action = "Lập thủ tục thanh lý và bàn giao dữ liệu nếu khách hàng không còn nhu cầu sử dụng."
            lane3_status = "Pending_Manager_Review"
        elif has_critical:
            lane3_manager_decision = "TẠM HOÃN DUYỆT TĂNG GÓI - DUYỆT PHƯƠNG ÁN BẢO VỆ KHÁCH HÀNG"
            lane3_action = "Chỉ đạo Kỹ thuật đóng dứt điểm ticket; CSKH trực tiếp gặp mặt xin lỗi và trình bày chính sách cam kết SLA mới."
            lane3_status = "Escalated_To_Manager"
        else:
            lane3_manager_decision = "ĐỒNG Ý ĐỀ XUẤT - CHUYỂN DỰ THẢO HỢP ĐỒNG MỚI"
            lane3_action = "Phê duyệt căn cứ đề xuất của AI Agent. Yêu cầu Kinh doanh & CSKH gửi dự thảo cho khách hàng."
            lane3_status = "Approved_By_Manager"

        # =====================================================================
        # 3. LÀN 4: BAN GIÁM ĐỐC (BGĐ) XEM XÉT & DUYỆT
        # =====================================================================
        if rec_info["requires_bod_approval"]:
            lane4_bod_required = True
            if rec_info["total_discount_pct"] > 20:
                lane4_trigger_reason = f"Mức chiết khấu {rec_info['total_discount_pct']}% vượt thẩm quyền Trưởng phòng (>20%)"
            elif rec_info["proposed_package"] == "Enterprise":
                lane4_trigger_reason = "Hợp đồng cấp Enterprise giá trị lớn (ARR cao)"
            else:
                lane4_trigger_reason = "Hồ sơ rủi ro cao cần chính sách giữ chân đặc biệt từ BGĐ"
            lane4_status = "Chờ BGĐ Phê Duyệt"
        else:
            lane4_bod_required = False
            lane4_trigger_reason = "Hồ sơ tiêu chuẩn trong hạn mức phân quyền của Trưởng phòng"
            lane4_status = "Trưởng phòng Ủy quyền Ký duyệt"

        # =====================================================================
        # 4. TẠO DANH SÁCH NHIỆM VỤ THEO DÕI TỪNG KHÁCH (ACTION TASKS)
        # =====================================================================
        tasks = []

        # Task 1: Đối với Kỹ thuật / Hỗ trợ nếu có sự cố
        if has_critical:
            tasks.append({
                "customer_id": cid,
                "customer_name": cname,
                "role": "Hỗ trợ Kỹ thuật (Support)",
                "assignee": "Lê Kỹ Thuật (Tech Lead)",
                "task_title": "Xử lý dứt điểm sự cố P1/P2 và ký biên bản nghiệm thu",
                "urgency": "HỎA TỐC (Trong 24h)",
                "due_date": (self.benchmark_date + timedelta(days=1)).strftime("%d/%m/%Y"),
                "workflow_stage": "Tiền đàm phán gia hạn",
                "instructions": "Khắc phục triệt để lỗi đồng bộ hóa đơn/hệ thống, test trực tiếp với IT khách hàng và lấy xác nhận đóng ticket."
            })

        # Task 2: Đối với CSKH (Customer Success)
        if strategy == "RESCUE_AND_HOLD":
            tasks.append({
                "customer_id": cid,
                "customer_name": cname,
                "role": "Chăm sóc khách hàng (CSKH)",
                "assignee": csm_rep,
                "task_title": "Thực hiện cuộc gọi thăm hỏi & cam kết chất lượng dịch vụ",
                "urgency": "Khẩn cấp (Trong 48h)",
                "due_date": (self.benchmark_date + timedelta(days=2)).strftime("%d/%m/%Y"),
                "workflow_stage": "Đánh giá & Thỏa thuận",
                "instructions": "Chia sẻ phương án bồi hoàn thiện chí (Gói INCIDENT_RECOVERY 10%), lắng nghe phản hồi của người dùng cuối."
            })
        elif strategy == "DOWNSELL_OR_RETENTION":
            tasks.append({
                "customer_id": cid,
                "customer_name": cname,
                "role": "Chăm sóc khách hàng (CSKH)",
                "assignee": csm_rep,
                "task_title": "Họp rà soát hiệu quả sử dụng & Đào tạo kích hoạt user (Adoption Workshop)",
                "urgency": "Quan trọng (Trước ngày liên hệ)",
                "due_date": (self.benchmark_date + timedelta(days=5)).strftime("%d/%m/%Y"),
                "workflow_stage": "Đánh giá sơ bộ",
                "instructions": f"Khách chỉ active {row['active_users_30d']}/{row['registered_seats']} tài khoản. Tìm hiểu nguyên nhân bộ phận nào chưa dùng để hướng dẫn."
            })
        else:
            tasks.append({
                "customer_id": cid,
                "customer_name": cname,
                "role": "Chăm sóc khách hàng (CSKH)",
                "assignee": csm_rep,
                "task_title": "Lập Báo cáo tổng kết giá trị sử dụng năm (Annual Business Review)",
                "urgency": "Tiêu chuẩn",
                "due_date": (row["target_contact_date"]).strftime("%d/%m/%Y"),
                "workflow_stage": "Báo cáo kết quả công việc",
                "instructions": "Tổng hợp số liệu thời gian vận hành 99.9%, số giờ tiết kiệm được và tính năng mới đã cập nhật."
            })

        # Task 3: Đối với Nhân viên Kinh doanh (Sales / AM)
        if days_to_contact <= 0:
            sales_urgency = "HỎA TỐC - ĐÃ QUÁ HẠN LIÊN HỆ"
            sales_due = (self.benchmark_date + timedelta(days=1)).strftime("%d/%m/%Y")
        elif days_to_contact <= 7:
            sales_urgency = "Gấp (Trong tuần này)"
            sales_due = (self.benchmark_date + timedelta(days=days_to_contact)).strftime("%d/%m/%Y")
        else:
            sales_urgency = "Tiêu chuẩn"
            sales_due = (row["target_contact_date"]).strftime("%d/%m/%Y")

        tasks.append({
            "customer_id": cid,
            "customer_name": cname,
            "role": "Nhân viên Kinh doanh (Sales)",
            "assignee": sales_rep,
            "task_title": f"Gửi Dự thảo Đề xuất Gia hạn ({rec_info['strategy_name']})",
            "urgency": sales_urgency,
            "due_date": sales_due,
            "workflow_stage": "Thỏa thuận & Dự thảo hợp đồng mới",
            "instructions": f"Gửi báo giá gói {rec_info['proposed_package']} ({rec_info['proposed_seats']} seats), tổng tiền sau ưu đãi {rec_info['net_proposed_arr']:,.0f} VND. "
                            f"Kèm giải trình căn cứ số liệu đã được AI và Trưởng phòng thẩm định."
        })

        # Task 4: Đối với Trưởng phòng và Hành chính
        tasks.append({
            "customer_id": cid,
            "customer_name": cname,
            "role": "Trưởng phòng Kinh doanh",
            "assignee": "Trần Trưởng Phòng (Sales Head)",
            "task_title": f"Duyệt đề xuất hồ sơ {cid}",
            "urgency": "Tiêu chuẩn",
            "due_date": (self.benchmark_date + timedelta(days=3)).strftime("%d/%m/%Y"),
            "workflow_stage": "Xem xét & Duyệt đề xuất",
            "instructions": f"Quyết định: {lane3_manager_decision}. Đánh giá phê duyệt mức chiết khấu {rec_info['total_discount_pct']}%."
        })

        return {
            "customer_id": cid,
            "lane1_submitter": f"{sales_rep} & {csm_rep}",
            "lane2_prescreen_status": lane2_prescreen_status,
            "lane2_prescreen_notes": lane2_note,
            "lane3_manager_decision": lane3_manager_decision,
            "lane3_manager_action": lane3_action,
            "lane3_manager_status": lane3_status,
            "lane4_bod_required": lane4_bod_required,
            "lane4_trigger_reason": lane4_trigger_reason,
            "lane4_status": lane4_status,
            "tasks": tasks
        }

