import math

class RecommendationEngine:
    """
    Sinh đề xuất gói gia hạn có căn cứ định lượng, tính toán ưu đãi hợp lệ
    và lập giải trình chi tiết phục vụ Trưởng phòng và BGĐ duyệt.
    """
    def __init__(self, service_packages, discount_policies):
        self.service_packages = service_packages
        self.discount_policies = discount_policies

    def generate_recommendation(self, row, health_info, audit_result):
        curr_pkg = row["current_package"]
        reg_seats = int(row["registered_seats"])
        active_users = int(row["active_users_30d"])
        util_pct = float(row["utilization_rate_pct"])
        days_to_expiry = int(row["days_until_expiry"])
        tenure = int(row["tenure_years"])
        has_critical_ticket = bool(row["has_unresolved_critical_incident"])
        open_tickets = int(row["open_tickets"])
        p1_p2_open = int(row["p1_p2_open_tickets"])
        avg_csat = float(row["avg_csat"])
        curr_arr = float(row["annual_contract_value"])

        # =====================================================================
        # 1. XÁC ĐỊNH CHIẾN LƯỢC GIA HẠN (STRATEGY)
        # =====================================================================
        if has_critical_ticket:
            strategy = "RESCUE_AND_HOLD"
            proposed_package = curr_pkg
            proposed_seats = reg_seats
            strategy_name = "Giữ chân & Khắc phục sự cố khẩn cấp (Chặn tăng gói)"
        elif util_pct < 40.0:
            strategy = "DOWNSELL_OR_RETENTION"
            proposed_package = curr_pkg
            # Nếu user active quá thấp (< 35%), đề xuất tối ưu hóa (right-sizing) hoặc kèm đào tạo
            if util_pct < 30.0 and reg_seats > 25:
                # Gợi ý tối ưu lại số ghế = active_users * 1.3 (dư 30% đệm phát triển)
                proposed_seats = max(10, int(math.ceil(active_users * 1.35)))
                strategy_name = f"Tối ưu hóa số tài khoản (Right-Sizing từ {reg_seats} xuống {proposed_seats} seats)"
            else:
                proposed_seats = reg_seats
                strategy_name = "Duy trì số lượng & Kích hoạt gói đào tạo CSKH cứu vãn adoption"
        elif util_pct >= 85.0 and avg_csat >= 4.0 and open_tickets == 0:
            # Đủ điều kiện tăng trưởng
            if curr_pkg == "Standard":
                strategy = "UPSELL_TIER"
                proposed_package = "Professional"
                proposed_seats = max(35, reg_seats)
                strategy_name = "Nâng cấp lên gói Professional (Do nhu cầu mở rộng tính năng & user cao)"
            elif curr_pkg == "Professional":
                strategy = "UPSELL_TIER"
                proposed_package = "Enterprise"
                proposed_seats = max(105, reg_seats)
                strategy_name = "Nâng cấp lên gói Enterprise (Do tiệm cận ngưỡng tài nguyên và cần SLA cao cấp)"
            else:
                strategy = "UPSELL_SEATS"
                proposed_package = "Enterprise"
                proposed_seats = int(reg_seats * 1.25)
                strategy_name = f"Mở rộng số tài khoản Enterprise (+25%, lên {proposed_seats} seats)"
        else:
            strategy = "MAINTAIN_CURRENT"
            proposed_package = curr_pkg
            proposed_seats = reg_seats
            strategy_name = "Gia hạn giữ nguyên gói & số lượng tài khoản"

        # =====================================================================
        # 2. XÁC ĐỊNH CHÍNH SÁCH ƯU ĐÃI HỢP CHUẨN (VALIDATED DISCOUNTS)
        # =====================================================================
        applied_promos = []
        total_discount_pct = 0

        # Kiểm tra Early Bird: Phải còn >= 25 ngày
        if days_to_expiry >= 25:
            applied_promos.append({
                "code": "EARLY_BIRD",
                "name": "Gia hạn sớm (>= 25 ngày)",
                "pct": 10
            })
            total_discount_pct += 10

        # Kiểm tra Thâm niên (Loyalty)
        if tenure >= 4:
            applied_promos.append({
                "code": "LOYALTY_TIER_2",
                "name": "Khách hàng Thân thiết Bền vững (>= 4 năm)",
                "pct": 8
            })
            total_discount_pct += 8
        elif tenure >= 2:
            applied_promos.append({
                "code": "LOYALTY_TIER_1",
                "name": "Khách hàng Thân thiết (2-3 năm)",
                "pct": 5
            })
            total_discount_pct += 5

        # Nếu đang có sự cố hoặc vừa khắc phục sự cố nghiêm trọng -> Ưu đãi thiện chí
        if has_critical_ticket:
            applied_promos.append({
                "code": "INCIDENT_RECOVERY",
                "name": "Cam kết Bù đắp Thiện chí Sự cố",
                "pct": 10
            })
            total_discount_pct += 10

        # Áp trần tối đa quy chế (Max cap 25%)
        gov_cap = self.discount_policies.get("GOVERNANCE_RULES", {}).get("max_stackable_discount_pct", 25)
        if total_discount_pct > gov_cap:
            total_discount_pct = gov_cap

        # Kiểm tra thẩm quyền phê duyệt
        requires_bod = total_discount_pct > 20 or proposed_package == "Enterprise" or strategy == "RESCUE_AND_HOLD"

        # =====================================================================
        # 3. TÍNH TOÁN TÀI CHÍNH DỰ BÁO
        # =====================================================================
        pkg_spec = self.service_packages[proposed_package]
        seat_price_year = pkg_spec["price_per_seat_year"]
        
        gross_arr = proposed_seats * seat_price_year
        discount_amount = gross_arr * (total_discount_pct / 100.0)
        net_proposed_arr = gross_arr - discount_amount
        arr_variance = net_proposed_arr - curr_arr

        # =====================================================================
        # 4. SINH CĂN CỨ ĐỀ XUẤT (JUSTIFICATION / RATIONALE)
        # =====================================================================
        rationale_parts = []

        # Căn cứ sử dụng
        rationale_parts.append(
            f"• Căn cứ Sử dụng: {active_users}/{reg_seats} tài khoản hoạt động trong 30 ngày qua (Tỷ lệ hoạt động: {util_pct}%). "
            f"Dung lượng lưu trữ: {row['storage_used_gb']}/{row['storage_limit_gb']}GB ({row['storage_utilization_pct']}%). "
            f"Xu hướng: {row['usage_trend_3m']}."
        )

        # Căn cứ hỗ trợ & sự cố
        if has_critical_ticket:
            rationale_parts.append(
                f"• CẢNH BÁO SỰ CỐ: Hiện có {p1_p2_open} sự cố P1/P2 chưa đóng. CSAT bình quân: {avg_csat:.1f}/5. "
                f"AI Agent tự động CHẶN TĂNG GÓI, đề xuất giữ nguyên gói và kích hoạt bảo trợ kỹ thuật cấp tốc."
            )
        else:
            rationale_parts.append(
                f"• Căn cứ Hỗ trợ: Không có sự cố nghiêm trọng tồn đọng ({open_tickets} ticket đang xử lý). "
                f"Chỉ số hài lòng CSAT đạt {avg_csat:.1f}/5."
            )

        # Căn cứ thời hạn & liên hệ
        lead_time = row["required_lead_days"]
        days_to_contact = row["days_until_contact_due"]
        if days_to_contact < 0:
            rationale_parts.append(
                f"• TIẾN ĐỘ LIÊN HỆ: Quá hạn chuẩn {abs(days_to_contact)} ngày (Hạn HĐ: {row['contract_end_date'].strftime('%d/%m/%Y')}, còn {days_to_expiry} ngày). Cần tiếp cận khẩn cấp."
            )
        else:
            rationale_parts.append(
                f"• Tiến độ liên hệ: Còn {days_to_contact} ngày đến hạn kích hoạt liên hệ chuẩn ({lead_time} ngày trước hết hạn)."
            )

        # Căn cứ ưu đãi
        if applied_promos:
            promo_desc = " + ".join([f"{p['name']} ({p['pct']}%)" for p in applied_promos])
            rationale_parts.append(
                f"• Căn cứ Ưu đãi: Đủ điều kiện hưởng tổng chiết khấu {total_discount_pct}% gồm [{promo_desc}]. Tuân thủ 100% quy chế tài chính."
            )
        else:
            rationale_parts.append("• Căn cứ Ưu đãi: Không áp dụng chiết khấu do chưa thỏa mãn điều kiện gia hạn sớm hoặc thâm niên.")

        # Căn cứ quyết định điều chỉnh lỗi của nhân viên nếu có
        if audit_result["violations_count"] > 0:
            error_titles = [v["title"] for v in audit_result["violations"]]
            rationale_parts.append(
                f"• ĐIỀU CHỈNH SAI SÓT CỦA NHÂN VIÊN: AI Agent đã rà soát và khắc phục {len(error_titles)} lỗi ({'; '.join(error_titles)})."
            )

        full_rationale = "\n".join(rationale_parts)

        return {
            "strategy": strategy,
            "strategy_name": strategy_name,
            "proposed_package": proposed_package,
            "proposed_seats": proposed_seats,
            "gross_arr": gross_arr,
            "total_discount_pct": total_discount_pct,
            "discount_amount": discount_amount,
            "net_proposed_arr": net_proposed_arr,
            "arr_variance": arr_variance,
            "applied_promos": applied_promos,
            "applied_promos_str": " + ".join([p["code"] for p in applied_promos]) if applied_promos else "NONE",
            "requires_bod_approval": requires_bod,
            "full_rationale": full_rationale
        }

