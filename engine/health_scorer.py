class HealthScorer:
    """
    Tính toán chỉ số Sức khỏe khách hàng (Account Health Score: 0 - 100)
    và Dự báo mức độ rủi ro rời bỏ (Churn Risk).
    """
    def __init__(self):
        pass

    def compute_score(self, row):
        # 1. Trụ cột Sử dụng (Usage - Tối đa 40 điểm)
        util_pct = row["utilization_rate_pct"]
        if util_pct >= 85:
            usage_score = 36
        elif util_pct >= 70:
            usage_score = 30
        elif util_pct >= 50:
            usage_score = 22
        elif util_pct >= 30:
            usage_score = 12
        else:
            usage_score = 5

        # Điều chỉnh theo xu hướng và tính năng
        trend = str(row.get("usage_trend_3m", "Stable"))
        if trend == "Increasing":
            usage_score += 4
        elif trend == "Declining":
            usage_score -= 6

        features = row.get("key_features_adopted_count", 5)
        if features >= 7:
            usage_score += 3
        elif features <= 3:
            usage_score -= 2

        usage_score = max(0, min(40, usage_score))

        # 2. Trụ cột Hỗ trợ & CSAT (Support - Tối đa 30 điểm)
        csat = row.get("avg_csat", 5.0)
        if csat >= 4.5:
            support_score = 30
        elif csat >= 4.0:
            support_score = 25
        elif csat >= 3.0:
            support_score = 16
        else:
            support_score = 6

        # Phạt nặng nếu còn sự cố P1/P2 chưa đóng
        p1_p2_open = row.get("p1_p2_open_tickets", 0)
        if p1_p2_open > 0:
            support_score -= (p1_p2_open * 15)

        open_tickets = row.get("open_tickets", 0)
        if open_tickets > 2:
            support_score -= 5

        support_score = max(0, min(30, support_score))

        # 3. Trụ cột Thâm niên & Gắn kết (Tenure - Tối đa 15 điểm)
        tenure = row.get("tenure_years", 1)
        if tenure >= 4:
            tenure_score = 15
        elif tenure >= 2:
            tenure_score = 12
        else:
            tenure_score = 8

        # 4. Trụ cột Thanh toán & Tài chính (Payment - Tối đa 15 điểm)
        payment_status = row.get("payment_status", "Paid")
        if payment_status == "Paid":
            payment_score = 15
        else:
            payment_score = 5

        # Tổng điểm
        total_health_score = int(usage_score + support_score + tenure_score + payment_score)
        total_health_score = max(0, min(100, total_health_score))

        # Phân loại Sức khỏe & Rủi ro
        if row.get("has_unresolved_critical_incident", False):
            churn_risk = "Cao (High Risk - Critical Ticket)"
            health_tier = "Cảnh báo Đỏ (At-Risk)"
        elif total_health_score < 50 or util_pct < 35:
            churn_risk = "Cao (High Risk - Inactive/Low CSAT)"
            health_tier = "Cảnh báo Đỏ (At-Risk)"
        elif total_health_score < 75:
            churn_risk = "Trung bình (Medium Risk)"
            health_tier = "Cảnh báo Vàng (Stable / Needs Attention)"
        else:
            churn_risk = "Thấp (Low Risk)"
            health_tier = "Xanh (Healthy / Growth Potential)"

        return {
            "health_score": total_health_score,
            "usage_subscore": usage_score,
            "support_subscore": support_score,
            "tenure_subscore": tenure_score,
            "payment_subscore": payment_score,
            "health_tier": health_tier,
            "churn_risk": churn_risk
        }

