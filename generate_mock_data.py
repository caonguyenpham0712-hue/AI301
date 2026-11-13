import json
import csv
import random
from datetime import datetime, timedelta

# Fix seed for reproducible, high quality realistic dataset
random.seed(42)

BENCHMARK_DATE = datetime(2026, 11, 15)

def generate_pricing_and_policies():
    packages = {
        "Standard": {
            "name": "Standard",
            "tier": 1,
            "min_seats": 10,
            "max_seats": 30,
            "price_per_seat_month": 250000,
            "price_per_seat_year": 3000000,
            "storage_gb": 50,
            "features": ["Core CRM", "Quản lý liên hệ", "Báo cáo cơ bản", "Hỗ trợ qua Email"],
            "sla": "99.0%"
        },
        "Professional": {
            "name": "Professional",
            "tier": 2,
            "min_seats": 31,
            "max_seats": 100,
            "price_per_seat_month": 450000,
            "price_per_seat_year": 5400000,
            "storage_gb": 200,
            "features": ["Toàn bộ Standard", "Tự động hóa quy trình", "Phân tích dự báo", "Tích hợp Zalo/Tổng đài", "Hỗ trợ Hotline & Email 8/5"],
            "sla": "99.5%"
        },
        "Enterprise": {
            "name": "Enterprise",
            "tier": 3,
            "min_seats": 101,
            "max_seats": 1000,
            "price_per_seat_month": 700000,
            "price_per_seat_year": 8400000,
            "storage_gb": 1000,
            "features": ["Toàn bộ Professional", "Tùy biến API/Webhook riêng", "Bảo mật nâng cao & SSO", "Dedicated CSM 24/7", "Đào tạo tại chỗ"],
            "sla": "99.9%"
        }
    }

    policies = {
        "EARLY_BIRD": {
            "code": "EARLY_BIRD",
            "name": "Ưu đãi Gia hạn Sớm",
            "discount_pct": 10,
            "condition_description": "Khách hàng chốt gia hạn trước ngày hết hạn >= 25 ngày",
            "min_days_before_expiry": 25,
            "max_discount_cap": 10
        },
        "MULTI_YEAR_2": {
            "code": "MULTI_YEAR_2",
            "name": "Ưu đãi Cam kết 2 năm",
            "discount_pct": 15,
            "condition_description": "Khách hàng đồng ý ký hợp đồng gia hạn thời hạn 2 năm trả trước",
            "min_commitment_years": 2,
            "max_discount_cap": 15
        },
        "MULTI_YEAR_3": {
            "code": "MULTI_YEAR_3",
            "name": "Ưu đãi Cam kết 3 năm",
            "discount_pct": 20,
            "condition_description": "Khách hàng đồng ý ký hợp đồng gia hạn thời hạn 3 năm trả trước",
            "min_commitment_years": 3,
            "max_discount_cap": 20
        },
        "LOYALTY_TIER_1": {
            "code": "LOYALTY_TIER_1",
            "name": "Khách hàng Thân thiết (2-3 năm)",
            "discount_pct": 5,
            "condition_description": "Khách hàng có thâm niên hợp tác liên tục từ 2 đến dưới 4 năm",
            "min_tenure_years": 2,
            "max_tenure_years": 3
        },
        "LOYALTY_TIER_2": {
            "code": "LOYALTY_TIER_2",
            "name": "Khách hàng Đồng hành Vàng (>= 4 năm)",
            "discount_pct": 8,
            "condition_description": "Khách hàng có thâm niên hợp tác liên tục từ 4 năm trở lên",
            "min_tenure_years": 4,
            "max_tenure_years": 99
        },
        "INCIDENT_RECOVERY": {
            "code": "INCIDENT_RECOVERY",
            "name": "Hỗ trợ Thiện chí do Sự cố",
            "discount_pct": 10,
            "condition_description": "Dành cho khách hàng gặp sự cố P1/P2 trong kỳ trước (đã khắc phục xong và cam kết SLA mới)",
            "applicable_only_if_past_incident_resolved": True
        },
        "GOVERNANCE_RULES": {
            "max_stackable_discount_pct": 25,
            "requires_bod_approval_above_pct": 20,
            "lead_time_contact_days": 30,
            "enterprise_lead_time_contact_days": 45,
            "overdue_threshold_days": 0
        }
    }

    with open("data/service_packages.json", "w", encoding="utf-8") as f:
        json.dump(packages, f, ensure_ascii=False, indent=2)

    with open("data/discount_policies.json", "w", encoding="utf-8") as f:
        json.dump(policies, f, ensure_ascii=False, indent=2)

    print("Created data/service_packages.json and data/discount_policies.json")

def generate_datasets():
    companies_pool = [
        ("Công ty Cổ phần Bất động sản Hoàng Gia", "Bất động sản"),
        ("Tập đoàn Dược phẩm Thiên Nam", "Dược phẩm"),
        ("Công ty TNHH Vận tải & Logistics Biển Đông", "Logistics"),
        ("Công ty CP Công nghệ & Truyền thông Sài Gòn", "Truyền thông"),
        ("Chuỗi Siêu thị Thực phẩm Sạch GreenMart", "Bán lẻ"),
        ("Công ty CP May mặc Xuất khẩu Thái Bình Dương", "Sản xuất"),
        ("Công ty TNHH Tư vấn Tài chính An Khang", "Tài chính"),
        ("Tập đoàn Khách sạn & Du lịch Hải Đăng", "Khách sạn"),
        ("Học viện Anh ngữ Quốc tế SmartEdu", "Giáo dục"),
        ("Công ty CP Xây dựng & Hạ tầng Toàn Cầu", "Xây dựng"),
        ("Công ty TNHH Thiết bị Y tế Minh Đức", "Y tế"),
        ("Công ty CP Chế biến Thủy hải sản Nam Việt", "Nông nghiệp"),
        ("Công ty CP Phân phối Hàng tiêu dùng Phúc Thịnh", "Bán lẻ"),
        ("Tập đoàn Cơ khí & Chế tạo Máy Tân Tiến", "Cơ khí"),
        ("Công ty Luật TNHH Hợp danh Minh Quang", "Dịch vụ pháp lý"),
        ("Công ty TNHH Thương mại Quốc tế Vĩnh Phát", "Xuất nhập khẩu"),
        ("Chuỗi Cửa hàng Trà sữa & F&B Trà Việt", "F&B"),
        ("Công ty CP Dịch vụ Bảo vệ & An ninh Thăng Long", "Dịch vụ"),
        ("Công ty CP Năng lượng & Môi trường Xanh", "Năng lượng"),
        ("Tập đoàn Đầu tư & Phát triển Đô thị Đại Việt", "Bất động sản")
    ]

    sales_team = ["Nguyễn Văn Dũng (Sales 1)", "Trần Thị Mai (Sales 2)", "Lê Hoàng Long (Sales 3)", "Vũ Thị Hương (Sales 4)"]
    csm_team = ["Phạm Quốc Bảo (CSKH 1)", "Đặng Thị Thảo (CSKH 2)", "Ngô Gia Huy (CSKH 3)", "Bùi Thu Hà (CSKH 4)"]

    contracts = []
    usage_logs = []
    tickets = []

    ticket_id_counter = 1001

    for i in range(1, 121):
        cid = f"KH-{1000 + i}"
        contract_code = f"HD-2025-{i:03d}"
        
        # Pick company name & industry
        base_name, industry = companies_pool[(i - 1) % len(companies_pool)]
        cust_name = f"{base_name} - Chi nhánh {i}" if i > len(companies_pool) else base_name
        
        # Determine tenure (1 to 5 years)
        tenure = random.choices([1, 2, 3, 4, 5], weights=[0.45, 0.25, 0.15, 0.10, 0.05])[0]
        
        # Determine package distribution: 50% Standard, 35% Professional, 15% Enterprise
        pkg_choice = random.choices(["Standard", "Professional", "Enterprise"], weights=[0.50, 0.35, 0.15])[0]
        
        if pkg_choice == "Standard":
            reg_seats = random.randint(15, 30)
            seat_price = 3000000
        elif pkg_choice == "Professional":
            reg_seats = random.randint(35, 80)
            seat_price = 5400000
        else:
            reg_seats = random.randint(110, 250)
            seat_price = 8400000
            
        contract_val = reg_seats * seat_price
        
        # Expiry date distributed from 5 days to 45 days after benchmark date
        # Benchmark: 2026-11-15
        # days_offset between 1 and 45
        days_offset = (i % 45) + 1  # 1 to 45 days from Nov 15
        end_date = BENCHMARK_DATE + timedelta(days=days_offset)
        start_date = end_date - timedelta(days=365)
        
        sales_rep = sales_team[i % len(sales_team)]
        csm_rep = csm_team[i % len(csm_team)]
        
        # Simulating the 4 classic operational issues deliberately on a realistic subset:
        # Scenario archetypes:
        # 1. Has Unresolved P1/P2 Ticket, but sales rep mistakenly proposed Upsell!
        # 2. Low active users (e.g. 15% - 40%), but sales rep mistakenly looked at registered seats and proposed Upsell!
        # 3. Staff mistakenly applied 20-30% discount without meeting conditions (e.g. claiming early bird when it's late, or claiming multi-year without customer consent).
        # 4. Missed contact date (expiration in < 10 days, lead time was 30 days, staff confused expiry with outreach date).
        # 5. Healthy candidate for upsell (Usage > 90%, active users high, CSAT 5, tickets all resolved).
        # 6. Normal renewal (Usage 60-80%, no issues, standard renewal).
        # 7. High churn risk (Low usage, declining, bad CSAT, complaints).

        archetype = (i % 7)
        has_unresolved_ticket = False
        num_tickets = 0
        active_ratio = 0.75
        trend = "Stable"
        csat_avg = 4.5
        
        # Raw human inputs that might contain mistakes:
        raw_proposed_pkg = pkg_choice
        raw_discount_code = "NONE"
        raw_discount_pct = 0
        
        if archetype == 0:
            # ISSUE 1: Unresolved P1/P2 ticket, but naive sales rep proposed UPGRADE!
            has_unresolved_ticket = True
            num_tickets = random.randint(2, 4)
            active_ratio = random.uniform(0.65, 0.85)
            trend = "Stable"
            csat_avg = 2.0
            # Misjudgment: sales proposed UPGRADE anyway
            raw_proposed_pkg = "Enterprise" if pkg_choice == "Professional" else "Professional"
            raw_discount_code = "LOYALTY_TIER_1"
            raw_discount_pct = 5
        elif archetype == 1:
            # ISSUE 2: Ghost account / Low real usage! Registered 50, but active only 8!
            # Staff looked at 50 and proposed to increase to 70!
            active_ratio = random.uniform(0.15, 0.35)
            trend = "Declining"
            num_tickets = 1
            csat_avg = 3.2
            raw_proposed_pkg = "Enterprise" if pkg_choice == "Professional" else pkg_choice
            raw_discount_code = "NONE"
            raw_discount_pct = 0
        elif archetype == 2:
            # ISSUE 3: Illegal discount applied by staff! (Claimed Early bird even though expiry is in 8 days)
            active_ratio = random.uniform(0.70, 0.85)
            trend = "Stable"
            num_tickets = 1
            csat_avg = 4.0
            raw_proposed_pkg = pkg_choice
            raw_discount_code = "EARLY_BIRD"
            raw_discount_pct = 15  # Policy says 10%, staff entered 15% and expiry is < 25 days!
        elif archetype == 3:
            # ISSUE 4: Expiry date confused with contact date.
            # Contract expires in 3-7 days! Contact should have started 30 days ago!
            end_date = BENCHMARK_DATE + timedelta(days=random.randint(2, 6))
            start_date = end_date - timedelta(days=365)
            active_ratio = random.uniform(0.60, 0.80)
            trend = "Stable"
            num_tickets = 0
            csat_avg = 4.2
            raw_proposed_pkg = pkg_choice
            raw_discount_code = "NONE"
            raw_discount_pct = 0
        elif archetype == 4:
            # HEALTHY UPSELL CANDIDATE: 95% utilization, growing, high CSAT
            active_ratio = random.uniform(0.90, 0.98)
            trend = "Increasing"
            num_tickets = 1
            csat_avg = 5.0
            raw_proposed_pkg = "Enterprise" if pkg_choice == "Professional" else ("Professional" if pkg_choice == "Standard" else "Enterprise")
            raw_discount_code = "EARLY_BIRD" if (end_date - BENCHMARK_DATE).days >= 25 else "NONE"
            raw_discount_pct = 10 if raw_discount_code == "EARLY_BIRD" else 0
        elif archetype == 5:
            # NORMAL STABLE RENEWAL
            active_ratio = random.uniform(0.65, 0.80)
            trend = "Stable"
            num_tickets = random.choice([0, 1, 2])
            csat_avg = 4.0
            raw_proposed_pkg = pkg_choice
            raw_discount_code = "NONE"
            raw_discount_pct = 0
        else:
            # HIGH CHURN RISK / COMPLAINTS
            active_ratio = random.uniform(0.30, 0.50)
            trend = "Declining"
            num_tickets = random.randint(2, 5)
            csat_avg = 2.4
            raw_proposed_pkg = pkg_choice
            raw_discount_code = "NONE"
            raw_discount_pct = 0

        # Compute active users
        active_users = max(1, int(reg_seats * active_ratio))
        storage_limit = 50 if pkg_choice == "Standard" else (200 if pkg_choice == "Professional" else 1000)
        storage_used = round(storage_limit * random.uniform(0.2, 0.92), 1)
        login_freq = round(random.uniform(2.5, 9.8), 1)
        adopted_features = random.randint(3, 10)
        last_active = BENCHMARK_DATE - timedelta(days=random.randint(0, 12))

        # Append contract
        contracts.append({
            "contract_id": contract_code,
            "customer_id": cid,
            "customer_name": cust_name,
            "industry": industry,
            "current_package": pkg_choice,
            "contract_start_date": start_date.strftime("%Y-%m-%d"),
            "contract_end_date": end_date.strftime("%Y-%m-%d"),
            "registered_seats": reg_seats,
            "annual_contract_value": contract_val,
            "tenure_years": tenure,
            "account_manager": sales_rep,
            "csm_in_charge": csm_rep,
            "payment_status": "Paid" if random.random() > 0.08 else "Late_Payment_Risk",
            "staff_raw_proposed_package": raw_proposed_pkg,
            "staff_raw_discount_code": raw_discount_code,
            "staff_raw_discount_pct": raw_discount_pct,
            "staff_raw_notes": "Nhân viên rà soát thủ công sơ bộ"
        })

        # Append usage log
        usage_logs.append({
            "customer_id": cid,
            "registered_seats": reg_seats,
            "active_users_30d": active_users,
            "utilization_rate_pct": round((active_users / reg_seats) * 100, 1),
            "storage_used_gb": storage_used,
            "storage_limit_gb": storage_limit,
            "storage_utilization_pct": round((storage_used / storage_limit) * 100, 1),
            "avg_login_frequency_per_week": login_freq,
            "key_features_adopted_count": adopted_features,
            "last_active_date": last_active.strftime("%Y-%m-%d"),
            "usage_trend_3m": trend
        })

        # Generate support tickets for this customer
        # If has_unresolved_ticket is True, generate at least one Open/In-progress P1/P2 ticket
        if has_unresolved_ticket:
            tickets.append({
                "ticket_id": f"TK-{ticket_id_counter}",
                "customer_id": cid,
                "created_at": (BENCHMARK_DATE - timedelta(days=random.randint(2, 10))).strftime("%Y-%m-%d"),
                "severity": random.choice(["P1 - Critical", "P2 - Major"]),
                "issue_type": "Lỗi đồng bộ dữ liệu hóa đơn điện tử & treo phiên làm việc",
                "status": random.choice(["Open", "In_Progress"]),
                "resolved_at": "",
                "csat_score": "",
                "assigned_support_engineer": "Lê Kỹ Thuật (Tech Lead)"
            })
            ticket_id_counter += 1

        # Additional historical tickets
        for t_idx in range(num_tickets):
            t_created = BENCHMARK_DATE - timedelta(days=random.randint(15, 80))
            is_resolved = True if not has_unresolved_ticket else (t_idx > 0)
            t_status = "Closed" if is_resolved else "In_Progress"
            t_score = int(csat_avg) if is_resolved else ""
            t_resolved = (t_created + timedelta(days=random.randint(1, 4))).strftime("%Y-%m-%d") if is_resolved else ""

            tickets.append({
                "ticket_id": f"TK-{ticket_id_counter}",
                "customer_id": cid,
                "created_at": t_created.strftime("%Y-%m-%d"),
                "severity": random.choice(["P2 - Major", "P3 - Minor", "P3 - Minor"]),
                "issue_type": random.choice([
                    "Hỏi cách cấu hình phân quyền người dùng mới",
                    "Chậm tốc độ tải báo cáo doanh thu tháng",
                    "Cần hướng dẫn xuất file Excel tùy chỉnh",
                    "Đổi thông tin đăng ký nhân viên phụ trách"
                ]),
                "status": t_status,
                "resolved_at": t_resolved,
                "csat_score": t_score,
                "assigned_support_engineer": "Nguyễn Hỗ Trợ (Helpdesk)"
            })
            ticket_id_counter += 1

    # Write contracts.csv
    with open("data/contracts.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(contracts[0].keys()))
        writer.writeheader()
        writer.writerows(contracts)

    # Write usage_logs.csv
    with open("data/usage_logs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(usage_logs[0].keys()))
        writer.writeheader()
        writer.writerows(usage_logs)

    # Write support_tickets.csv
    with open("data/support_tickets.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(tickets[0].keys()))
        writer.writeheader()
        writer.writerows(tickets)

    print(f"Generated {len(contracts)} contracts, {len(usage_logs)} usage records, and {len(tickets)} support tickets.")

if __name__ == "__main__":
    generate_pricing_and_policies()
    generate_datasets()

