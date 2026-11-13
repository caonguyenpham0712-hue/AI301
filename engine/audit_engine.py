import pandas as pd

class AuditEngine:
    """
    Rà soát và phát hiện 4 sai phạm kinh điển trong quy trình gia hạn của Công ty An Tín:
    1. Đề xuất tăng gói khi còn sự cố P1/P2 chưa xử lý.
    2. Nhầm số tài khoản đăng ký với số người thực sự sử dụng (Active Users).
    3. Nhầm ngày hết hạn với ngày cần bắt đầu liên hệ (chậm trễ tiến độ tiếp cận).
    4. Áp dụng chính sách ưu đãi không đúng điều kiện quy chế.
    """
    def __init__(self, service_packages, discount_policies):
        self.service_packages = service_packages
        self.discount_policies = discount_policies
        self.audit_logs = []

    def audit_row(self, row):
        violations = []
        corrections = []
        is_compliant = True

        pkg_tier_map = {"Standard": 1, "Professional": 2, "Enterprise": 3}
        current_tier = pkg_tier_map.get(row["current_package"], 1)
        staff_proposed_tier = pkg_tier_map.get(row.get("staff_raw_proposed_package", row["current_package"]), current_tier)
        is_upsell_proposed = staff_proposed_tier > current_tier

        # =====================================================================
        # LỖI 1: TĂNG GÓI TRONG KHI CÒN SỰ CỐ CHƯA XỬ LÝ
        # =====================================================================
        if is_upsell_proposed and row["has_unresolved_critical_incident"]:
            is_compliant = False
            violations.append({
                "error_code": "ERR_01_UPSELL_BLOCKED_UNRESOLVED_TICKET",
                "severity": "CRITICAL",
                "title": "Đề xuất tăng gói trong khi còn sự cố kỹ thuật nghiêm trọng chưa xử lý",
                "detail": f"Khách hàng có {row['p1_p2_open_tickets']} ticket P1/P2 đang xử lý (CSAT hiện tại: {row['avg_csat']:.1f}/5). "
                          f"Nhân viên đề xuất nâng từ {row['current_package']} lên {row.get('staff_raw_proposed_package')}. "
                          f"Hành động này gây bức xúc cho khách và nguy cơ mất khách (Churn).",
                "corrective_action": "Chặn tăng gói (Block Upsell). Chuyển sang kịch bản: Hỗ trợ khẩn cấp đóng sự cố + CSKH xin lỗi cam kết SLA + Đề xuất duy trì gói hiện tại kèm ưu đãi thiện chí."
            })
            corrections.append("BLOCK_UPSELL_MAINTAIN_CURRENT")

        # =====================================================================
        # LỖI 2: ẢO TƯỞNG SỐ USER (XEM SỐ ĐĂNG KÝ LÀ SỐ THỰC SỰ SỬ DỤNG)
        # =====================================================================
        utilization_rate = row["utilization_rate_pct"]
        if utilization_rate < 50.0:
            is_compliant = False
            violations.append({
                "error_code": "ERR_02_SEATS_MISALIGNMENT_LOW_ACTIVE",
                "severity": "WARNING",
                "title": "Tỷ lệ sử dụng thực tế quá thấp so với số tài khoản đăng ký",
                "detail": f"Số tài khoản mua: {row['registered_seats']}, nhưng chỉ có {row['active_users_30d']} người active (Đạt {utilization_rate}%). "
                          f"Nhân viên không nhận diện nguy cơ khách cảm thấy lãng phí ngân sách và không gia hạn.",
                "corrective_action": "Đánh giá lại nhu cầu thực tế: Nếu khách muốn tiết giảm chi phí -> Đề xuất gói tinh gọn (Right-Sizing); "
                                     "Nếu khách duy trì gói -> Kích hoạt ngay chương trình CSKH đào tạo & hỗ trợ kích hoạt user."
            })
            corrections.append("FLAG_LOW_UTILIZATION")
        elif is_upsell_proposed and utilization_rate < 75.0:
            is_compliant = False
            violations.append({
                "error_code": "ERR_02_PREMATURE_UPSELL_LOW_USAGE",
                "severity": "WARNING",
                "title": "Đề xuất nâng gói thiếu căn cứ sử dụng",
                "detail": f"Tỷ lệ sử dụng hiện tại chỉ đạt {utilization_rate}%, chưa chạm ngưỡng mở rộng (cần >= 85%).",
                "corrective_action": "Khuyên nghị duy trì gói hiện tại và tập trung khai thác hết tính năng trước khi upsell."
            })
            corrections.append("REVERT_UPSELL_TO_MAINTAIN")

        # =====================================================================
        # LỖI 3: NHẦM NGÀY HẾT HẠN VỚI NGÀY CẦN BẮT ĐẦU LIÊN HỆ
        # =====================================================================
        days_until_contact = row["days_until_contact_due"]
        days_until_expiry = row["days_until_expiry"]
        
        if days_until_contact < 0:
            is_compliant = False
            violations.append({
                "error_code": "ERR_03_OVERDUE_CONTACT_TIMELINE",
                "severity": "CRITICAL" if days_until_expiry <= 10 else "WARNING",
                "title": "Quá hạn bắt đầu liên hệ gia hạn theo quy định",
                "detail": f"Ngày hết hạn hợp đồng là {row['contract_end_date'].strftime('%d/%m/%Y')} (còn {days_until_expiry} ngày). "
                          f"Quy chuẩn yêu cầu bắt đầu liên hệ trước {row['required_lead_days']} ngày. "
                          f"Hiện đã quá hạn bắt đầu liên hệ {abs(days_until_contact)} ngày mà chưa hoàn tất thỏa thuận.",
                "corrective_action": "Đưa vào danh sách 'Khẩn cấp / Báo động đỏ'. Phân công Sales & CSKH liên hệ trực tiếp trong vòng 24 giờ."
            })
            corrections.append("ESCALATE_URGENT_OUTREACH")

        # =====================================================================
        # LỖI 4: ÁP DỤNG ƯU ĐÃI KHÔNG ĐÚNG ĐIỀU KIỆN
        # =====================================================================
        staff_discount_code = str(row.get("staff_raw_discount_code", "NONE")).strip()
        staff_discount_pct = float(row.get("staff_raw_discount_pct", 0))

        if staff_discount_code != "NONE" and staff_discount_pct > 0:
            policy_info = self.discount_policies.get(staff_discount_code)
            discount_valid = True
            invalid_reasons = []

            if not policy_info:
                discount_valid = False
                invalid_reasons.append(f"Mã ưu đãi '{staff_discount_code}' không tồn tại trong danh mục quy chế.")
            else:
                # Check Early Bird
                if staff_discount_code == "EARLY_BIRD":
                    if days_until_expiry < policy_info.get("min_days_before_expiry", 25):
                        discount_valid = False
                        invalid_reasons.append(f"Chỉ còn {days_until_expiry} ngày là hết hạn (Yêu cầu Early Bird phải >= 25 ngày).")

                # Check Loyalty Tier 1
                elif staff_discount_code == "LOYALTY_TIER_1":
                    if row["tenure_years"] < policy_info.get("min_tenure_years", 2):
                        discount_valid = False
                        invalid_reasons.append(f"Thâm niên khách hàng mới {row['tenure_years']} năm (Yêu cầu >= 2 năm).")

                # Check Loyalty Tier 2
                elif staff_discount_code == "LOYALTY_TIER_2":
                    if row["tenure_years"] < policy_info.get("min_tenure_years", 4):
                        discount_valid = False
                        invalid_reasons.append(f"Thâm niên khách hàng mới {row['tenure_years']} năm (Yêu cầu >= 4 năm).")

                # Check discount cap
                allowed_pct = policy_info.get("discount_pct", 0)
                if staff_discount_pct > allowed_pct:
                    discount_valid = False
                    invalid_reasons.append(f"Mức giảm giá đề xuất {staff_discount_pct}% vượt quá định mức quy định ({allowed_pct}%).")

            if not discount_valid:
                is_compliant = False
                violations.append({
                    "error_code": "ERR_04_INVALID_DISCOUNT_POLICY",
                    "severity": "HIGH",
                    "title": "Áp dụng chính sách ưu đãi không đúng điều kiện",
                    "detail": " ; ".join(invalid_reasons),
                    "corrective_action": "Hủy bỏ chiết khấu sai quy định. AI Agent tự động tính toán lại mức ưu đãi hợp chuẩn dựa trên hồ sơ khách."
                })
                corrections.append("RESET_AND_RECALCULATE_DISCOUNT")

        return {
            "customer_id": row["customer_id"],
            "contract_id": row["contract_id"],
            "is_compliant": is_compliant,
            "violations_count": len(violations),
            "violations": violations,
            "corrections": corrections
        }

    def audit_all(self, df):
        """Run audit across all customer rows."""
        results = []
        for _, row in df.iterrows():
            res = self.audit_row(row)
            results.append(res)
            self.audit_logs.append(res)
        return results

