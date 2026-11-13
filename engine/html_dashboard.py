import json

class HTMLDashboardGenerator:
    """
    Sinh giao diện Dashboard HTML tương tác trực quan cao cấp,
    đồng bộ 100% theo phong cách thiết kế mẫu (Pastel Blush Pink & Cream,
    Frosted Glassmorphism, Luxury Serif Typography, Smooth Micro-animations),
    tích hợp Toast Notifications cao cấp, 3 thẻ tiện ích đáy trang (Smart Docs, CSAT, Outreach),
    Trợ lý AI Co-Pilot Chatbot và kết nối REST API localhost:8000.
    """
    def __init__(self, output_path="output/Dashboard_Gia_Han_An_Tin.html"):
        self.output_path = output_path

    def generate(self, summary_data, detailed_df, tasks_list, audit_violations_list):
        records = detailed_df.to_dict(orient="records")
        for r in records:
            r["contract_start_date"] = r["contract_start_date"].strftime("%d/%m/%Y")
            r["contract_end_date"] = r["contract_end_date"].strftime("%d/%m/%Y")
            r["target_contact_date"] = r["target_contact_date"].strftime("%d/%m/%Y")
            r["last_active_date"] = r["last_active_date"].strftime("%d/%m/%Y") if hasattr(r["last_active_date"], "strftime") else str(r["last_active_date"])

        records_json = json.dumps(records, ensure_ascii=False)
        tasks_json = json.dumps(tasks_list, ensure_ascii=False)
        violations_map = {item["customer_id"]: item["violations"] for item in audit_violations_list}
        violations_json = json.dumps(violations_map, ensure_ascii=False)

        html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>An Tín Software | Hệ Thống AI Agent Gia Hạn Hợp Đồng Chuẩn Xác</title>
    <!-- Google Fonts: Playfair Display (Serif cao cấp) & Plus Jakarta Sans (Giao diện hiện đại) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --bg-gradient: linear-gradient(135deg, #FDEFEA 0%, #F8E2DC 35%, #F4D3CC 70%, #F9ECE8 100%);
            --rose-primary: #C46D86;
            --rose-dark: #A34863;
            --rose-light: #F7D6DE;
            --rose-soft: #FDF2F4;
            --terracotta: #C58B74;
            --terracotta-dark: #AC715A;
            --cream-bg: #FFF9F7;
            --card-glass: rgba(255, 255, 255, 0.78);
            --card-border: rgba(255, 255, 255, 0.9);
            --text-heading: #2D2327;
            --text-body: #5A4B51;
            --text-muted: #8E7B82;
            --shadow-soft: 0 15px 35px rgba(196, 109, 134, 0.09);
            --shadow-hover: 0 20px 45px rgba(196, 109, 134, 0.16);
            --radius-lg: 24px;
            --radius-md: 18px;
            --radius-pill: 9999px;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            background: var(--bg-gradient);
            background-attachment: fixed;
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: var(--text-body);
            line-height: 1.6;
            overflow-x: hidden;
        }}

        h1, h2, h3, h4, .serif-font {{
            font-family: 'Playfair Display', Georgia, serif;
            color: var(--text-heading);
            letter-spacing: -0.02em;
        }}

        /* Glassmorphism Card Utility */
        .glass-card {{
            background: var(--card-glass);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--card-border);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-soft);
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .glass-card:hover {{
            box-shadow: var(--shadow-hover);
            transform: translateY(-4px);
        }}

        /* Top Pill Navigation Bar (Matching Sample Image Header) */
        .pill-navbar-container {{
            max-width: 1140px;
            margin: 24px auto 35px auto;
            padding: 0 16px;
        }}

        .pill-navbar {{
            background: rgba(255, 255, 255, 0.72);
            backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.95);
            border-radius: var(--radius-pill);
            padding: 10px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 10px 30px rgba(196, 109, 134, 0.08);
        }}

        .pill-nav-links a {{
            color: var(--text-body);
            text-decoration: none;
            font-size: 13.5px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin: 0 14px;
            transition: color 0.2s ease;
        }}

        .pill-nav-links a:hover, .pill-nav-links a.active {{
            color: var(--rose-primary);
        }}

        .pill-search-box {{
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(230, 205, 210, 0.8);
            border-radius: var(--radius-pill);
            padding: 7px 18px;
            display: flex;
            align-items: center;
            width: 320px;
            transition: all 0.3s ease;
        }}

        .pill-search-box:focus-within {{
            border-color: var(--rose-primary);
            box-shadow: 0 0 0 3px rgba(196, 109, 134, 0.15);
            background: #fff;
        }}

        .pill-search-box input {{
            border: none;
            outline: none;
            background: transparent;
            font-size: 13.5px;
            width: 100%;
            color: var(--text-heading);
        }}

        .pill-search-box input::placeholder {{
            color: var(--text-muted);
            font-style: italic;
        }}

        /* Buttons */
        .btn-luxury {{
            background: linear-gradient(135deg, var(--terracotta) 0%, var(--terracotta-dark) 100%);
            color: #ffffff;
            border: none;
            border-radius: var(--radius-pill);
            padding: 12px 30px;
            font-weight: 600;
            font-size: 14px;
            letter-spacing: 0.04em;
            box-shadow: 0 8px 20px rgba(197, 139, 116, 0.28);
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }}

        .btn-luxury:hover {{
            color: #fff;
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 12px 25px rgba(197, 139, 116, 0.38);
        }}

        .btn-luxury-outline {{
            background: transparent;
            color: var(--terracotta-dark);
            border: 1.5px solid var(--terracotta);
            border-radius: var(--radius-pill);
            padding: 10px 24px;
            font-weight: 600;
            font-size: 13.5px;
            transition: all 0.3s ease;
        }}

        .btn-luxury-outline:hover {{
            background: var(--terracotta);
            color: white;
            transform: translateY(-2px);
        }}

        /* Hero Section */
        .hero-section {{
            max-width: 1140px;
            margin: 0 auto 50px auto;
            padding: 20px 16px;
        }}

        .hero-title {{
            font-size: 52px;
            line-height: 1.15;
            font-weight: 700;
            margin-bottom: 20px;
            color: var(--text-heading);
        }}

        .hero-title span {{
            font-style: italic;
            color: var(--rose-primary);
        }}

        .hero-badge {{
            display: inline-block;
            background: rgba(196, 109, 134, 0.12);
            color: var(--rose-primary);
            padding: 6px 16px;
            border-radius: var(--radius-pill);
            font-size: 12.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 16px;
        }}

        .hero-stat-pill {{
            background: rgba(255, 255, 255, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            padding: 16px 20px;
            box-shadow: 0 10px 25px rgba(196, 109, 134, 0.06);
            display: flex;
            align-items: center;
            margin-bottom: 14px;
        }}

        .hero-stat-icon {{
            width: 48px;
            height: 48px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            margin-right: 16px;
            background: var(--rose-soft);
            color: var(--rose-primary);
        }}

        /* Section Cards & Showcase */
        .section-header {{
            text-align: center;
            margin-bottom: 40px;
        }}

        .section-subtitle {{
            text-transform: uppercase;
            font-size: 12.5px;
            letter-spacing: 0.15em;
            color: var(--rose-primary);
            font-weight: 700;
            margin-bottom: 8px;
        }}

        .section-title {{
            font-size: 34px;
            font-weight: 700;
            color: var(--text-heading);
        }}

        /* Service Tier Cards (Matching 3 product cards in image) */
        .tier-card {{
            border-radius: var(--radius-lg);
            padding: 28px 24px;
            background: #ffffff;
            border: 1px solid rgba(240, 220, 225, 0.8);
            box-shadow: 0 12px 30px rgba(196, 109, 134, 0.06);
            transition: all 0.3s ease;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
        }}

        .tier-card:hover {{
            transform: translateY(-6px);
            box-shadow: var(--shadow-hover);
            border-color: var(--rose-light);
        }}

        .tier-card.featured {{
            background: linear-gradient(180deg, #FFFFFF 0%, #FFF5F7 100%);
            border: 1.5px solid var(--rose-light);
        }}

        .tier-price {{
            font-family: 'Playfair Display', serif;
            font-size: 28px;
            font-weight: 700;
            color: var(--text-heading);
            margin: 12px 0 6px 0;
        }}

        .tier-badge {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: var(--rose-soft);
            color: var(--rose-primary);
            padding: 4px 12px;
            border-radius: var(--radius-pill);
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }}

        /* Seasonal Specials Banner Card (Matching right card in image) */
        .promo-highlight-card {{
            background: linear-gradient(135deg, #F8E2DC 0%, #F5D3CC 100%);
            border-radius: var(--radius-lg);
            padding: 32px 26px;
            border: 1px solid rgba(255, 255, 255, 0.9);
            box-shadow: var(--shadow-soft);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            height: 100%;
        }}

        .promo-highlight-badge {{
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.12em;
            color: var(--rose-dark);
            text-transform: uppercase;
            margin-bottom: 10px;
        }}

        .promo-discount-number {{
            font-family: 'Playfair Display', serif;
            font-size: 46px;
            font-weight: 700;
            color: var(--text-heading);
            line-height: 1;
            margin-bottom: 14px;
        }}

        /* Split Promo Section (Matching Section 3 in image) */
        .split-promo-section {{
            max-width: 1140px;
            margin: 0 auto 50px auto;
            padding: 0 16px;
        }}

        .split-promo-card {{
            background: linear-gradient(135deg, #FBECE8 0%, #F7DCD5 100%);
            border-radius: var(--radius-lg);
            overflow: hidden;
            box-shadow: var(--shadow-soft);
            border: 1px solid rgba(255, 255, 255, 0.8);
        }}

        .promo-left-panel {{
            padding: 45px 40px;
        }}

        .error-card-pill {{
            background: rgba(255, 255, 255, 0.92);
            border-radius: var(--radius-md);
            padding: 16px 20px;
            margin-bottom: 12px;
            border-left: 4px solid var(--rose-primary);
            box-shadow: 0 6px 16px rgba(196, 109, 134, 0.05);
            transition: transform 0.2s ease;
        }}

        .error-card-pill:hover {{
            transform: translateX(4px);
        }}

        /* Carousel Navigation Controls (Matching Bottom Arrows in Image) */
        .carousel-nav-btn {{
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.95);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: var(--text-heading);
            font-size: 15px;
            box-shadow: 0 8px 18px rgba(196, 109, 134, 0.12);
            cursor: pointer;
            transition: all 0.25s ease;
        }}

        .carousel-nav-btn:hover {{
            background: var(--terracotta);
            color: white;
            transform: scale(1.08);
        }}

        .carousel-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: rgba(196, 109, 134, 0.25);
            display: inline-block;
            margin: 0 5px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .carousel-dot.active {{
            width: 24px;
            border-radius: 10px;
            background: var(--terracotta);
        }}

        /* Contracts Table Luxury Styling */
        .luxury-table-container {{
            max-width: 1140px;
            margin: 0 auto 50px auto;
            padding: 0 16px;
        }}

        .table-glass {{
            background: rgba(255, 255, 255, 0.92);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-soft);
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.95);
            padding: 28px;
        }}

        .custom-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0 10px;
        }}

        .custom-table thead th {{
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            border-bottom: 2px solid #F4E4E0;
            padding: 12px 14px;
        }}

        .custom-table tbody tr {{
            background: #ffffff;
            box-shadow: 0 4px 12px rgba(196, 109, 134, 0.03);
            border-radius: 14px;
            transition: all 0.25s ease;
        }}

        .custom-table tbody tr:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(196, 109, 134, 0.09);
            background: #FFFAF9;
        }}

        .custom-table tbody td {{
            padding: 14px;
            vertical-align: middle;
            border-top: none;
            font-size: 13.5px;
        }}

        .custom-table tbody tr td:first-child {{
            border-top-left-radius: 14px;
            border-bottom-left-radius: 14px;
        }}

        .custom-table tbody tr td:last-child {{
            border-top-right-radius: 14px;
            border-bottom-right-radius: 14px;
        }}

        /* Luxury Status Pills */
        .pill-tag {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: var(--radius-pill);
            font-size: 11.5px;
            font-weight: 700;
            letter-spacing: 0.02em;
        }}

        .pill-tag-green {{ background: #EAF5ED; color: #2D7A47; }}
        .pill-tag-yellow {{ background: #FEF7E6; color: #9A6B1A; }}
        .pill-tag-red {{ background: #FCECEE; color: #B3394E; }}
        .pill-tag-neutral {{ background: #F3ECEE; color: #725D64; }}

        /* 3 Bottom Feature Cards (Matching the 3 icons under carousel in sample image) */
        .bottom-features-section {{
            max-width: 1140px;
            margin: 0 auto 60px auto;
            padding: 0 16px;
        }}

        .bottom-feature-card {{
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.95);
            border-radius: var(--radius-lg);
            padding: 24px;
            box-shadow: var(--shadow-soft);
            transition: all 0.3s ease;
            text-align: center;
            height: 100%;
        }}

        .bottom-feature-card:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-hover);
        }}

        .bottom-feature-icon {{
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--rose-soft) 0%, #F5D3CC 100%);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            color: var(--terracotta-dark);
            margin-bottom: 16px;
            box-shadow: 0 6px 16px rgba(196, 109, 134, 0.12);
        }}

        /* Floating AI Chat Co-Pilot (Pastel Blush Re-themed) */
        #aiChatWidget {{
            position: fixed;
            bottom: 25px;
            right: 25px;
            width: 390px;
            height: 540px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(25px);
            border-radius: var(--radius-lg);
            box-shadow: 0 20px 50px rgba(196, 109, 134, 0.25);
            display: flex;
            flex-direction: column;
            z-index: 1050;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
            border: 1px solid rgba(255, 255, 255, 0.95);
        }}

        #aiChatWidget.minimized {{
            height: 56px;
            width: 270px;
            overflow: hidden;
        }}

        .chat-header-luxury {{
            background: linear-gradient(135deg, var(--rose-primary) 0%, var(--terracotta) 100%);
            color: #ffffff;
            padding: 14px 20px;
            border-radius: var(--radius-lg) var(--radius-lg) 0 0;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .chat-body-luxury {{
            flex: 1;
            padding: 16px;
            overflow-y: auto;
            background: #FFF9F7;
            font-size: 13.5px;
        }}

        .chat-bubble {{
            max-width: 86%;
            padding: 11px 16px;
            border-radius: 18px;
            margin-bottom: 12px;
            line-height: 1.45;
            font-size: 13px;
        }}

        .chat-bubble-bot {{
            background: #ffffff;
            color: var(--text-heading);
            border: 1px solid #F4E2DE;
            box-shadow: 0 4px 12px rgba(196, 109, 134, 0.05);
            margin-right: auto;
        }}

        .chat-bubble-user {{
            background: linear-gradient(135deg, var(--rose-primary) 0%, var(--terracotta) 100%);
            color: #ffffff;
            margin-left: auto;
            box-shadow: 0 4px 12px rgba(197, 139, 116, 0.25);
        }}

        /* Modal Customization */
        .modal-content-luxury {{
            background: rgba(255, 255, 255, 0.98);
            border-radius: var(--radius-lg);
            border: 1px solid rgba(255, 255, 255, 0.9);
            box-shadow: 0 25px 60px rgba(196, 109, 134, 0.2);
            overflow: hidden;
        }}

        .modal-header-luxury {{
            background: linear-gradient(135deg, #FDEFEA 0%, #F5D3CC 100%);
            padding: 20px 28px;
            border-bottom: 1px solid #F0D5CD;
        }}

        /* BPMN Steps in Modal */
        .bpmn-step-node {{
            position: relative;
            padding-left: 28px;
            margin-bottom: 18px;
        }}

        .bpmn-step-node::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 4px;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: var(--terracotta);
            box-shadow: 0 0 0 4px rgba(197, 139, 116, 0.2);
        }}

        .bpmn-step-node::after {{
            content: '';
            position: absolute;
            left: 6px;
            top: 22px;
            width: 2px;
            height: calc(100% - 10px);
            background: #E8D0C8;
        }}

        .bpmn-step-node:last-child::after {{
            display: none;
        }}

        /* Floating Luxury Toast */
        .toast-luxury {{
            position: fixed;
            top: 30px;
            right: 30px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.95);
            border-radius: var(--radius-md);
            padding: 16px 24px;
            box-shadow: 0 15px 40px rgba(196, 109, 134, 0.2);
            z-index: 2000;
            display: flex;
            align-items: center;
            gap: 14px;
            transform: translateY(-50px);
            opacity: 0;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .toast-luxury.show {{
            transform: translateY(0);
            opacity: 1;
        }}
    </style>
</head>
<body>

    <!-- Floating Luxury Toast Container -->
    <div id="luxuryToast" class="toast-luxury">
        <div id="toastIcon" style="font-size: 22px; color: var(--terracotta);"><i class="fa-solid fa-circle-check"></i></div>
        <div>
            <strong id="toastTitle" class="d-block text-dark small" style="letter-spacing: 0.02em;">Thông báo</strong>
            <span id="toastMsg" class="text-muted small">Nội dung thông báo</span>
        </div>
    </div>

    <!-- Top Pill Navbar (Matching the sample image search & pill menu) -->
    <div class="pill-navbar-container">
        <nav class="pill-navbar">
            <div class="d-flex align-items-center">
                <span class="serif-font fw-bold fs-4 me-3 text-dark">An Tín.</span>
                <div class="pill-nav-links d-none d-lg-flex">
                    <a href="#hero" class="active">Trang Chủ</a>
                    <a href="#services">Gói Dịch Vụ</a>
                    <a href="#audit">Kiểm Toán 4 Lỗi</a>
                    <a href="#contracts">120 Hợp Đồng</a>
                    <a href="#features">Tiện Ích</a>
                </div>
            </div>

            <!-- Pill Search Box -->
            <div class="pill-search-box">
                <i class="fa-solid fa-magnifying-glass text-muted me-2"></i>
                <input type="text" id="globalPillSearch" placeholder="Tìm theo tên khách, mã HĐ, NV phụ trách..." oninput="handleGlobalSearch(this.value)">
                <span class="badge rounded-pill bg-light text-dark px-2 py-1 ms-1" style="font-size: 10px;">ESC</span>
            </div>
        </nav>
    </div>

    <!-- Hero Section (Bite into Happiness -> Kiến Tạo Giá Trị Bền Vững) -->
    <section class="hero-section" id="hero">
        <div class="row align-items-center g-4">
            <div class="col-lg-6">
                <span class="hero-badge"><i class="fa-solid fa-wand-magic-sparkles me-2"></i>Hệ Thống AI Agent 2.0</span>
                <h1 class="hero-title">
                    Gia Hạn Hợp Đồng <span>Chuẩn Xác</span> & Đột Phá.
                </h1>
                <p class="text-muted fs-6 mb-4" style="max-width: 480px;">
                    Công ty Cổ phần Phần mềm An Tín vận hành quy trình tự động hóa 4 làn bơi BPMN, triệt tiêu 4 sai phạm kinh điển, đối soát theo thời gian thực 120 hợp đồng/tháng.
                </p>
                <div class="d-flex align-items-center gap-3 mb-4">
                    <a href="#contracts" class="btn-luxury">
                        Khám Phá 120 Hợp Đồng <i class="fa-solid fa-arrow-right ms-2"></i>
                    </a>
                    <button class="btn-luxury-outline" onclick="toggleChat()">
                        <i class="fa-solid fa-comments me-2"></i>Hỏi AI Co-Pilot
                    </button>
                </div>
                <div class="d-flex align-items-center gap-4 text-muted small">
                    <div><i class="fa-solid fa-calendar-check text-danger me-1"></i> Ngày đối chiếu: <strong>{summary_data['benchmark_date']}</strong></div>
                    <div><i class="fa-solid fa-shield-halved text-success me-1"></i> Tỷ lệ bảo toàn: <strong>{summary_data['arr_growth_pct']:+.1f}%</strong></div>
                </div>
            </div>

            <!-- Hero Visual Centerpiece (Matching Hero Card Style) -->
            <div class="col-lg-6">
                <div class="glass-card p-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <span class="text-uppercase small fw-bold text-muted">Tổng Quan Tài Chính Kỳ Này</span>
                            <h3 class="serif-font mb-0 mt-1">{summary_data['total_proposed_arr']:,.0f} <span class="fs-6 text-muted">VND</span></h3>
                        </div>
                        <span class="badge pill-tag pill-tag-green fs-6 px-3 py-2">
                            <i class="fa-solid fa-arrow-trend-up me-1"></i>39.7 Tỷ ARR
                        </span>
                    </div>

                    <!-- 3 KPI Pills inside Hero Showcase -->
                    <div class="hero-stat-pill">
                        <div class="hero-stat-icon"><i class="fa-solid fa-file-signature"></i></div>
                        <div class="flex-grow-1">
                            <div class="small text-muted">Tổng Quy Mô Hợp Đồng Đến Hạn</div>
                            <div class="fw-bold fs-5 text-dark">{summary_data['total_contracts']} Hợp Đồng <span class="badge bg-light text-muted ms-2">100% Đối Soát</span></div>
                        </div>
                    </div>

                    <div class="hero-stat-pill">
                        <div class="hero-stat-icon" style="background: #FCECEE; color: #C46D86;"><i class="fa-solid fa-shield-virus"></i></div>
                        <div class="flex-grow-1">
                            <div class="small text-muted">Hồ Sơ Nguy Cơ Cao Cần Bảo Vệ (At-Risk)</div>
                            <div class="fw-bold fs-5 text-danger">{summary_data['total_at_risk']} Khách Hàng <span class="badge pill-tag pill-tag-red ms-2">Chặn Tăng Gói</span></div>
                        </div>
                    </div>

                    <div class="hero-stat-pill mb-0">
                        <div class="hero-stat-icon" style="background: #FEF7E6; color: #C58B74;"><i class="fa-solid fa-wand-magic-sparkles"></i></div>
                        <div class="flex-grow-1">
                            <div class="small text-muted">Sai Phạm Nhân Viên Đã Được AI Ngăn Chặn</div>
                            <div class="fw-bold fs-5" style="color: #AC715A;">{summary_data['total_audited_violations']} Trường Hợp <span class="badge pill-tag pill-tag-yellow ms-2">Sửa Lỗi Tự Động</span></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Section 2: Handcrafted Service Packages & Seasonal Specials (Matching Section 2 in image) -->
    <section class="container mb-5" id="services" style="max-width: 1140px;">
        <div class="section-header">
            <div class="section-subtitle">DANH MỤC GÓI PHẦN MỀM AN TÍN</div>
            <h2 class="section-title">Định Khung Nhu Cầu & Đặc Quyền Gia Hạn</h2>
        </div>

        <div class="row g-4">
            <!-- Tier 1: Standard -->
            <div class="col-md-3">
                <div class="tier-card">
                    <div>
                        <span class="tier-badge">SME Gói 1</span>
                        <h4 class="serif-font mt-2 mb-1">Standard</h4>
                        <div class="text-muted small">Doanh nghiệp 10 - 30 seats</div>
                        <div class="tier-price">3.0 <span class="fs-6 text-muted">Tr/seat/năm</span></div>
                        <ul class="list-unstyled small text-muted mt-3 mb-4">
                            <li class="mb-2"><i class="fa-solid fa-check text-success me-2"></i>Core CRM & Liên Hệ</li>
                            <li class="mb-2"><i class="fa-solid fa-check text-success me-2"></i>Dung lượng lưu trữ 50GB</li>
                            <li class="mb-2"><i class="fa-solid fa-check text-success me-2"></i>Cam kết SLA 99.0%</li>
                        </ul>
                    </div>
                    <button class="btn btn-sm btn-luxury-outline w-100" onclick="filterByPackage('Standard')">Xem 60 Khách Hàng</button>
                </div>
            </div>

            <!-- Tier 2: Professional -->
            <div class="col-md-3">
                <div class="tier-card featured">
                    <div>
                        <span class="tier-badge" style="background: #F7D6DE; color: #A34863;">Phổ Biến Nhất</span>
                        <h4 class="serif-font mt-2 mb-1">Professional</h4>
                        <div class="text-muted small">Doanh nghiệp vừa (31 - 100 seats)</div>
                        <div class="tier-price">5.4 <span class="fs-6 text-muted">Tr/seat/năm</span></div>
                        <ul class="list-unstyled small text-muted mt-3 mb-4">
                            <li class="mb-2"><i class="fa-solid fa-check text-success me-2"></i>Automation Quy Trình</li>
                            <li class="mb-2"><i class="fa-solid fa-check text-success me-2"></i>Dung lượng 200GB & Zalo API</li>
                            <li class="mb-2"><i class="fa-solid fa-check text-success me-2"></i>Cam kết SLA 99.5%</li>
                        </ul>
                    </div>
                    <button class="btn btn-sm btn-luxury w-100" onclick="filterByPackage('Professional')">Xem 42 Khách Hàng</button>
                </div>
            </div>

            <!-- Tier 3: Enterprise -->
            <div class="col-md-3">
                <div class="tier-card">
                    <div>
                        <span class="tier-badge" style="background: #FEF7E6; color: #9A6B1A;">VIP Khách Hàng</span>
                        <h4 class="serif-font mt-2 mb-1">Enterprise</h4>
                        <div class="text-muted small">Tập đoàn lớn (101+ seats)</div>
                        <div class="tier-price">8.4 <span class="fs-6 text-muted">Tr/seat/năm</span></div>
                        <ul class="list-unstyled small text-muted mt-3 mb-4">
                            <li class="mb-2"><i class="fa-solid fa-check text-success me-2"></i>API Webhook riêng & SSO</li>
                            <li class="mb-2"><i class="fa-solid fa-check text-success me-2"></i>Dedicated CSM 24/7</li>
                            <li class="mb-2"><i class="fa-solid fa-check text-success me-2"></i>Cam kết SLA 99.9%</li>
                        </ul>
                    </div>
                    <button class="btn btn-sm btn-luxury-outline w-100" onclick="filterByPackage('Enterprise')">Xem 18 Khách Hàng</button>
                </div>
            </div>

            <!-- Special Highlights Promo Card (Matching right card in image) -->
            <div class="col-md-3">
                <div class="promo-highlight-card">
                    <div class="promo-highlight-badge">CHÍNH SÁCH ƯU ĐÃI</div>
                    <h5 class="serif-font mb-1">Early Bird & Loyalty</h5>
                    <div class="promo-discount-number">10-25%</div>
                    <p class="small text-muted mb-3" style="max-width: 200px;">
                        Áp dụng chuẩn quy chế: Gia hạn sớm trước 25 ngày, thâm niên 2-4 năm và hỗ trợ sự cố thiện chí.
                    </p>
                    <a href="#contracts" class="btn-luxury w-100 text-center py-2 fs-6">Áp Dụng Ngay</a>
                </div>
            </div>
        </div>
    </section>

    <!-- Section 3: Split Promo Section (Matching "LIMITED TIME PROMO" in image) -->
    <section class="split-promo-section" id="audit">
        <div class="split-promo-card">
            <div class="row g-0 align-items-center">
                <div class="col-lg-6 promo-left-panel">
                    <span class="hero-badge mb-2">QUẢN TRỊ RỦI RO & TUÂN THỦ</span>
                    <h2 class="serif-font mb-3">Ngăn Chặn Triệt Để 4 Sai Lầm Nghiệp Vụ</h2>
                    <p class="text-muted small mb-4">
                        Trước đây, nhân viên thường mắc các sai sót dẫn đến khách bức xúc hoặc thất thoát doanh thu. AI Agent của An Tín đã tự động kiểm toán toàn bộ 120 hồ sơ:
                    </p>

                    <div class="d-flex gap-3 mb-4">
                        <button class="btn-luxury" onclick="filterTableByError('ERR_01')">
                            <i class="fa-solid fa-ban me-2"></i>Chặn Upsell ({summary_data['err_upsell_with_ticket']} ca)
                        </button>
                        <button class="btn-luxury-outline" onclick="filterTableByError('ERR_02')">
                            <i class="fa-solid fa-users me-2"></i>Sửa Active ({summary_data['err_seats_misalignment']} ca)
                        </button>
                    </div>

                    <div class="d-flex align-items-center gap-3">
                        <span class="small text-muted">Bộ phận phối hợp:</span>
                        <span class="badge rounded-pill bg-white text-dark px-3 py-2 shadow-sm"><i class="fa-solid fa-headset text-danger me-1"></i>CSKH</span>
                        <span class="badge rounded-pill bg-white text-dark px-3 py-2 shadow-sm"><i class="fa-solid fa-briefcase text-primary me-1"></i>Kinh Doanh</span>
                        <span class="badge rounded-pill bg-white text-dark px-3 py-2 shadow-sm"><i class="fa-solid fa-laptop-code text-warning me-1"></i>Kỹ Thuật</span>
                    </div>
                </div>

                <!-- Right Side: 4 Error Pills Showcase -->
                <div class="col-lg-6 p-4">
                    <div class="error-card-pill">
                        <div class="d-flex justify-content-between">
                            <strong>1. Chặn Tăng Gói Khi Còn Sự Cố P1/P2</strong>
                            <span class="badge pill-tag pill-tag-red">{summary_data['err_upsell_with_ticket']} Ca</span>
                        </div>
                        <div class="small text-muted mt-1">Đóng băng Upsell, yêu cầu Kỹ thuật xử lý trong 24h & áp dụng ưu đãi thiện chí 10%.</div>
                    </div>

                    <div class="error-card-pill" style="border-left-color: var(--terracotta);">
                        <div class="d-flex justify-content-between">
                            <strong>2. Khắc Phục Ảo Tưởng Số User (Active < 50%)</strong>
                            <span class="badge pill-tag pill-tag-yellow">{summary_data['err_seats_misalignment']} Ca</span>
                        </div>
                        <div class="small text-muted mt-1">Đối soát đúng Active users, đề xuất Right-Sizing hoặc workshop đào tạo Onboarding.</div>
                    </div>

                    <div class="error-card-pill" style="border-left-color: #A34863;">
                        <div class="d-flex justify-content-between">
                            <strong>3. Báo Động Quá Hạn Tiếp Cận (30 Ngày)</strong>
                            <span class="badge pill-tag pill-tag-red">{summary_data['err_missed_outreach']} Ca</span>
                        </div>
                        <div class="small text-muted mt-1">Phân định rõ ngày hết hạn vs ngày cần liên hệ, đưa vào danh sách tiếp cận hỏa tốc.</div>
                    </div>

                    <div class="error-card-pill" style="border-left-color: #2D7A47;">
                        <div class="d-flex justify-content-between">
                            <strong>4. Chuẩn Hóa Ưu Đãi Sai Quy Chế</strong>
                            <span class="badge pill-tag pill-tag-green">{summary_data['err_invalid_discount']} Ca</span>
                        </div>
                        <div class="small text-muted mt-1">Hủy chiết khấu khống, tính toán lại chính xác mức chiết khấu hợp lệ theo thâm niên.</div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Section 4: 120 Contracts Management Table & Carousel Controls (Matching Bottom in image) -->
    <section class="luxury-table-container" id="contracts">
        <div class="table-glass">
            <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
                <div>
                    <div class="section-subtitle text-start mb-1">DANH SÁCH CHI TIẾT HỒ SƠ GIA HẠN</div>
                    <h3 class="serif-font mb-0">120 Khách Hàng Đến Kỳ Gia Hạn</h3>
                </div>

                <!-- Carousel-like Filter Dots & Navigation Controls (Matching Image Bottom Arrows) -->
                <div class="d-flex align-items-center gap-3">
                    <div class="carousel-nav-btn" onclick="prevFilter()"><i class="fa-solid fa-chevron-left"></i></div>
                    <div class="d-flex align-items-center">
                        <span class="carousel-dot active" id="dot0" onclick="selectFilterTab(0, 'ALL')"></span>
                        <span class="carousel-dot" id="dot1" onclick="selectFilterTab(1, 'AT_RISK')"></span>
                        <span class="carousel-dot" id="dot2" onclick="selectFilterTab(2, 'OVERDUE')"></span>
                        <span class="carousel-dot" id="dot3" onclick="selectFilterTab(3, 'BOD_APPROVAL')"></span>
                        <span class="carousel-dot" id="dot4" onclick="selectFilterTab(4, 'HEALTHY')"></span>
                    </div>
                    <div class="carousel-nav-btn" onclick="nextFilter()"><i class="fa-solid fa-chevron-right"></i></div>
                </div>
            </div>

            <!-- Secondary Filter Row -->
            <div class="row g-3 align-items-center mb-4">
                <div class="col-md-5">
                    <div class="pill-search-box w-100">
                        <i class="fa-solid fa-magnifying-glass text-muted me-2"></i>
                        <input type="text" id="tableSearchInput" placeholder="Lọc theo tên doanh nghiệp, mã khách, nhân viên..." oninput="applyFilters()">
                    </div>
                </div>
                <div class="col-md-4">
                    <select id="statusFilter" class="form-select rounded-pill px-3 py-2 small" style="border-color: #EED8D2;" onchange="applyFilters()">
                        <option value="ALL">-- Tất Cả Tình Trạng ({len(records)} hồ sơ) --</option>
                        <option value="AT_RISK">Cảnh Báo Đỏ / Rủi Ro Cao ({summary_data['total_at_risk']})</option>
                        <option value="AI_REVISED">Đã Được AI Điều Chỉnh Lỗi ({summary_data['total_audited_violations']})</option>
                        <option value="OVERDUE">Quá Hạn Bắt Đầu Liên Hệ ({summary_data['err_missed_outreach']})</option>
                        <option value="BOD_APPROVAL">Cần Ban Giám Đốc Phê Duyệt</option>
                        <option value="HEALTHY">Khách Hàng Khỏe Mạnh</option>
                    </select>
                </div>
                <div class="col-md-3 text-end">
                    <span class="text-muted small fw-semibold" id="filterCount">Hiển thị {len(records)} hồ sơ</span>
                </div>
            </div>

            <!-- Table -->
            <div class="table-responsive" style="max-height: 520px; overflow-y: auto;">
                <table class="custom-table" id="contractTable">
                    <thead>
                        <tr>
                            <th>Mã HĐ</th>
                            <th>Khách Hàng</th>
                            <th>Gói</th>
                            <th>Hết Hạn</th>
                            <th>Tiến Độ Liên Hệ</th>
                            <th>Active / Đăng Ký</th>
                            <th>Sự Cố P1/P2</th>
                            <th>Sức Khỏe</th>
                            <th>Doanh Thu Mới</th>
                            <th>Phê Duyệt</th>
                            <th class="text-center">Thao Tác</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody">
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>
        </div>
    </section>

    <!-- Section 5: 3 Bottom Feature Cards (Matching the 3 icons under carousel in sample image) -->
    <section class="bottom-features-section" id="features">
        <div class="row g-4">
            <div class="col-md-4">
                <div class="bottom-feature-card">
                    <div class="bottom-feature-icon"><i class="fa-solid fa-file-contract"></i></div>
                    <h5 class="serif-font mb-2">Tự Động Hóa Hồ Sơ (Smart Docs)</h5>
                    <p class="text-muted small mb-0">
                        Tự động sinh Phụ lục Hợp đồng gia hạn định dạng Word (.docx) chuẩn điều khoản SLA và bảng giá sau chiết khấu.
                    </p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="bottom-feature-card">
                    <div class="bottom-feature-icon"><i class="fa-solid fa-heart-pulse"></i></div>
                    <h5 class="serif-font mb-2">Đo Lường CSAT & Sức Khỏe</h5>
                    <p class="text-muted small mb-0">
                        Chấm điểm sức khỏe tài khoản 0-100 dựa trên tỷ lệ Active thực tế, nhật ký thao tác và trạng thái xử lý ticket kỹ thuật.
                    </p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="bottom-feature-card">
                    <div class="bottom-feature-icon"><i class="fa-solid fa-paper-plane"></i></div>
                    <h5 class="serif-font mb-2">Tiếp Cận Chuẩn Hóa (Outreach SLA)</h5>
                    <p class="text-muted small mb-0">
                        Đảm bảo kích hoạt đàm phán trước 30-45 ngày, phân bổ 377 nhiệm vụ hành động theo đúng 4 làn quy trình BPMN.
                    </p>
                </div>
            </div>
        </div>
    </section>

    <!-- Floating AI Chat Co-Pilot Widget (Pastel Blush Re-themed) -->
    <div id="aiChatWidget">
        <div class="chat-header-luxury" onclick="toggleChat()">
            <div class="d-flex align-items-center">
                <i class="fa-solid fa-wand-magic-sparkles text-white me-2"></i>
                <span class="fw-bold" style="letter-spacing: 0.02em;">An Tín AI Co-Pilot</span>
                <span class="badge rounded-pill bg-white text-dark ms-2" style="font-size: 9.5px;">ONLINE</span>
            </div>
            <div>
                <button class="btn btn-sm text-white p-0" id="chatToggleBtn"><i class="fa-solid fa-chevron-down"></i></button>
            </div>
        </div>
        <div class="chat-body-luxury" id="chatBody">
            <div class="chat-bubble chat-bubble-bot">
                Xin chào! Tôi là <strong>AI Agent Gia Hạn Hợp Đồng An Tín</strong>.<br>
                Hệ thống đã sẵn sàng hỗ trợ bạn theo dõi 120 hợp đồng và thực thi quy trình 4 làn bơi BPMN. Bạn có thể hỏi:
                <ul class="mb-0 ps-3 mt-1 small">
                    <li><em>"Kiểm tra khách hàng KH-1002"</em></li>
                    <li><em>"Ai có nguy cơ rời bỏ cao nhất?"</em></li>
                    <li><em>"Báo cáo 4 sai phạm đã ngăn chặn"</em></li>
                </ul>
            </div>
        </div>
        <div class="p-2 bg-white" style="border-radius: 0 0 24px 24px; border-top: 1px solid #F4E2DE;">
            <div class="input-group">
                <input type="text" id="chatInput" class="form-control form-control-sm rounded-pill px-3" placeholder="Hỏi AI Agent điều gì..." onkeypress="handleChatKey(event)">
                <button class="btn btn-sm btn-luxury ms-1 px-3" onclick="sendChatMessage()"><i class="fa-solid fa-paper-plane"></i></button>
            </div>
        </div>
    </div>

    <!-- Modal Xem Chi Tiết Hồ Sơ & Luồng Quy Trình -->
    <div class="modal fade" id="detailModal" tabindex="-1" aria-labelledby="detailModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable">
            <div class="modal-content modal-content-luxury">
                <div class="modal-header modal-header-luxury">
                    <h5 class="serif-font fw-bold mb-0" id="detailModalLabel">
                        <i class="fa-solid fa-file-invoice me-2 text-danger"></i>Hồ Sơ 360° Thẩm Định Gia Hạn Hợp Đồng
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body p-4" id="modalBody">
                    <!-- Populated dynamically -->
                </div>
                <div class="modal-footer bg-light p-3" id="modalFooter">
                    <!-- Populated dynamically -->
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let records = {records_json};
        const tasks = {tasks_json};
        const violations = {violations_json};

        const filterTabs = ['ALL', 'AT_RISK', 'OVERDUE', 'BOD_APPROVAL', 'HEALTHY'];
        let currentTabIdx = 0;

        function showLuxuryToast(title, msg, isSuccess = true) {{
            const toast = document.getElementById("luxuryToast");
            const toastTitle = document.getElementById("toastTitle");
            const toastMsg = document.getElementById("toastMsg");
            const toastIcon = document.getElementById("toastIcon");

            toastTitle.innerText = title;
            toastMsg.innerText = msg;
            toastIcon.innerHTML = isSuccess 
                ? '<i class="fa-solid fa-circle-check" style="color: #2D7A47;"></i>'
                : '<i class="fa-solid fa-triangle-exclamation" style="color: #C58B74;"></i>';

            toast.classList.add("show");
            setTimeout(() => {{
                toast.classList.remove("show");
            }}, 3800);
        }}

        function selectFilterTab(idx, filterVal) {{
            currentTabIdx = idx;
            for (let i = 0; i < 5; i++) {{
                const dot = document.getElementById("dot" + i);
                if (dot) {{
                    if (i === idx) dot.classList.add("active");
                    else dot.classList.remove("active");
                }}
            }}
            document.getElementById("statusFilter").value = filterVal;
            applyFilters();
        }}

        function nextFilter() {{
            currentTabIdx = (currentTabIdx + 1) % filterTabs.length;
            selectFilterTab(currentTabIdx, filterTabs[currentTabIdx]);
        }}

        function prevFilter() {{
            currentTabIdx = (currentTabIdx - 1 + filterTabs.length) % filterTabs.length;
            selectFilterTab(currentTabIdx, filterTabs[currentTabIdx]);
        }}

        function filterByPackage(pkg) {{
            document.getElementById("tableSearchInput").value = pkg;
            applyFilters();
            const el = document.getElementById("contracts");
            if (el) el.scrollIntoView({{ behavior: "smooth" }});
            showLuxuryToast("Đã lọc gói", `Hiển thị danh sách khách hàng sử dụng gói ${{pkg}}`);
        }}

        function filterTableByError(errCode) {{
            document.getElementById("statusFilter").value = "AI_REVISED";
            applyFilters();
            const el = document.getElementById("contracts");
            if (el) el.scrollIntoView({{ behavior: "smooth" }});
            showLuxuryToast("Kiểm toán AI", `Hiển thị các hồ sơ đã được phát hiện và sửa sai sót nghiệp vụ.`);
        }}

        function handleGlobalSearch(val) {{
            document.getElementById("tableSearchInput").value = val;
            applyFilters();
            const el = document.getElementById("contracts");
            if (el && val.length > 2) el.scrollIntoView({{ behavior: "smooth" }});
        }}

        function renderTable(data) {{
            const tbody = document.getElementById("tableBody");
            tbody.innerHTML = "";

            data.forEach((r, idx) => {{
                let healthBadge = "";
                if (r.health_score >= 75) {{
                    healthBadge = `<span class="pill-tag pill-tag-green"><i class="fa-solid fa-heart me-1"></i>${{r.health_score}}/100</span>`;
                }} else if (r.health_score >= 50) {{
                    healthBadge = `<span class="pill-tag pill-tag-yellow"><i class="fa-solid fa-triangle-exclamation me-1"></i>${{r.health_score}}/100</span>`;
                }} else {{
                    healthBadge = `<span class="pill-tag pill-tag-red"><i class="fa-solid fa-radiation me-1"></i>${{r.health_score}}/100</span>`;
                }}

                let contactBadge = "";
                if (r.days_until_contact_due < 0) {{
                    contactBadge = `<span class="pill-tag pill-tag-red">Quá hạn ${{Math.abs(r.days_until_contact_due)}} ngày</span>`;
                }} else if (r.days_until_contact_due <= 7) {{
                    contactBadge = `<span class="pill-tag pill-tag-yellow">Còn ${{r.days_until_contact_due}} ngày</span>`;
                }} else {{
                    contactBadge = `<span class="pill-tag pill-tag-neutral">Còn ${{r.days_until_contact_due}} ngày</span>`;
                }}

                let ticketBadge = r.p1_p2_open_tickets > 0 
                    ? `<span class="pill-tag pill-tag-red"><i class="fa-solid fa-bug me-1"></i>${{r.p1_p2_open_tickets}} P1/P2</span>`
                    : `<span class="pill-tag pill-tag-green"><i class="fa-solid fa-check me-1"></i>0</span>`;

                let approvalStatusBadge = "";
                if (r.lane3_manager_status && r.lane3_manager_status.includes("ĐÃ PHÊ DUYỆT")) {{
                    approvalStatusBadge = `<span class="pill-tag pill-tag-green"><i class="fa-solid fa-circle-check me-1"></i>Đã Duyệt (Làn 3)</span>`;
                }} else {{
                    approvalStatusBadge = `<span class="pill-tag ${{r.requires_bod_approval ? 'pill-tag-red' : 'pill-tag-neutral'}}">${{r.requires_bod_approval ? 'Cần BGĐ' : 'Chờ TP Duyệt'}}</span>`;
                }}

                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td><strong class="text-dark">${{r.contract_id}}</strong><br><small class="text-muted">${{r.customer_id}}</small></td>
                    <td>
                        <div class="fw-semibold" style="color: var(--text-heading);">${{r.customer_name}}</div>
                        <small class="text-muted">${{r.industry}} | Thâm niên: ${{r.tenure_years}} năm</small>
                    </td>
                    <td><span class="badge rounded-pill bg-light text-dark px-2 py-1">${{r.current_package}}</span></td>
                    <td>${{r.contract_end_date}}<br><small class="text-muted">Còn ${{r.days_until_expiry}} ngày</small></td>
                    <td>${{contactBadge}}</td>
                    <td>
                        <strong>${{r.active_users_30d}}</strong> / ${{r.registered_seats}} 
                        <span class="pill-tag ${{r.utilization_rate_pct < 50 ? 'pill-tag-red' : 'pill-tag-neutral'}} ms-1">${{r.utilization_rate_pct}}%</span>
                    </td>
                    <td>${{ticketBadge}}</td>
                    <td>${{healthBadge}}</td>
                    <td class="text-end fw-bold" style="color: var(--terracotta);">${{r.net_proposed_arr.toLocaleString()}} đ</td>
                    <td>${{approvalStatusBadge}}</td>
                    <td class="text-center">
                        <button class="btn btn-sm btn-luxury-outline py-1 px-3" onclick="showDetail('${{r.customer_id}}')">
                            Xem Hồ Sơ
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            }});

            document.getElementById("filterCount").innerText = `Hiển thị ${{data.length}} / ${{records.length}} hồ sơ`;
        }}

        function showDetail(cid) {{
            const r = records.find(item => item.customer_id === cid);
            if (!r) return;

            const custTasks = tasks.filter(t => t.customer_id === cid);
            const custViolations = violations[cid] || [];

            let violationsHtml = "";
            if (custViolations.length > 0) {{
                violationsHtml = `
                    <div class="alert alert-warning border-0 rounded-4 p-3 mb-3" style="background: #FFF4E5;">
                        <h6 class="fw-bold text-danger mb-2"><i class="fa-solid fa-shield-halved me-2"></i>Phát hiện ${{custViolations.length}} sai sót từ nhân viên - Đã được AI Agent khắc phục:</h6>
                        ${{custViolations.map(v => `
                            <div class="p-2 mb-2 bg-white rounded-3 border-start border-4 border-danger small">
                                <strong>[${{v.error_code}}] ${{v.title}}</strong>
                                <p class="mb-1 text-muted">${{v.detail}}</p>
                                <div class="text-success fw-semibold">Biện pháp điều chỉnh: ${{v.corrective_action}}</div>
                            </div>
                        `).join("")}}
                    </div>
                `;
            }} else {{
                violationsHtml = `<div class="alert alert-success border-0 rounded-4 p-3 small mb-3" style="background: #EAF5ED; color: #2D7A47;"><i class="fa-solid fa-circle-check me-2"></i>Hồ sơ đạt chuẩn nghiệp vụ 100%, không vi phạm 4 lỗi quy định.</div>`;
            }}

            let tasksHtml = `
                <div class="table-responsive">
                    <table class="table table-sm align-middle">
                        <thead class="table-light small">
                            <tr>
                                <th>Bộ Phận</th>
                                <th>Người Phụ Trách</th>
                                <th>Nhiệm Vụ</th>
                                <th>Mức Độ</th>
                                <th>Hạn Chót</th>
                            </tr>
                        </thead>
                        <tbody class="small">
                            ${{custTasks.map(t => `
                                <tr>
                                    <td><span class="badge rounded-pill bg-light text-dark">${{t.role}}</span></td>
                                    <td><strong>${{t.assignee}}</strong></td>
                                    <td>${{t.task_title}}</td>
                                    <td><span class="pill-tag ${{t.urgency.includes('HỎA TỐC') ? 'pill-tag-red' : 'pill-tag-yellow'}}">${{t.urgency}}</span></td>
                                    <td>${{t.due_date}}</td>
                                </tr>
                            `).join("")}}
                        </tbody>
                    </table>
                </div>
            `;

            const modalHtml = `
                <div class="row g-4 mb-3">
                    <div class="col-md-7">
                        <h4 class="serif-font fw-bold text-dark mb-1">${{r.customer_name}}</h4>
                        <p class="text-muted small mb-3">Mã KH: <strong>${{r.customer_id}}</strong> | Hợp đồng: <strong>${{r.contract_id}}</strong> | Phụ trách: <strong>${{r.account_manager}}</strong> & <strong>${{r.csm_in_charge}}</strong></p>
                        ${{violationsHtml}}
                        <div class="glass-card p-3 mb-3 bg-white">
                            <h6 class="serif-font fw-bold text-dark mb-2"><i class="fa-solid fa-lightbulb text-warning me-2"></i>Căn Cứ Đề Xuất Của AI Agent:</h6>
                            <div class="small" style="white-space: pre-line; line-height: 1.6;">${{r.full_rationale}}</div>
                        </div>
                    </div>
                    <div class="col-md-5">
                        <div class="glass-card p-3 mb-3 bg-white">
                            <h6 class="serif-font fw-bold text-dark border-bottom pb-2">Phương Án Tài Chính Đề Xuất</h6>
                            <div class="d-flex justify-content-between mb-1 small">
                                <span class="text-muted">Gói dịch vụ:</span>
                                <strong>${{r.proposed_package}} (${{r.proposed_seats}} seats)</strong>
                            </div>
                            <div class="d-flex justify-content-between mb-1 small">
                                <span class="text-muted">Giá trị gốc:</span>
                                <span>${{r.gross_arr.toLocaleString()}} đ</span>
                            </div>
                            <div class="d-flex justify-content-between mb-1 small">
                                <span class="text-muted">Ưu đãi hợp chuẩn:</span>
                                <span class="pill-tag pill-tag-green">${{r.applied_promos_str}} (${{r.total_discount_pct}}%)</span>
                            </div>
                            <div class="d-flex justify-content-between mb-1 small">
                                <span class="text-muted">Số tiền giảm trừ:</span>
                                <span class="text-danger">-${{r.discount_amount.toLocaleString()}} đ</span>
                            </div>
                            <hr class="my-2">
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="fw-bold">Doanh Thu Mới:</span>
                                <span class="fs-5 fw-bold" style="color: var(--terracotta);">${{r.net_proposed_arr.toLocaleString()}} đ</span>
                            </div>
                            <small class="text-muted text-end d-block">Chênh lệch: ${{r.arr_variance >= 0 ? '+' : ''}}${{r.arr_variance.toLocaleString()}} đ</small>
                        </div>

                        <!-- 4 Làn Quy Trình BPMN -->
                        <div class="glass-card p-3 bg-white">
                            <h6 class="serif-font fw-bold text-dark border-bottom pb-2"><i class="fa-solid fa-diagram-project me-2 text-danger"></i>Tiến Độ 4 Làn Quy Trình (BPMN)</h6>
                            <div class="bpmn-step-node">
                                <strong class="small">Làn 1: CSKH & Kinh Doanh</strong>
                                <div class="small text-muted">${{r.lane1_submitter}} đã lập hồ sơ & báo cáo.</div>
                            </div>
                            <div class="bpmn-step-node">
                                <strong class="small">Làn 2: Hành Chính - Vận Hành</strong>
                                <div class="small text-muted"><span class="pill-tag pill-tag-green">${{r.lane2_prescreen_status}}</span> - ${{r.lane2_prescreen_notes}}</div>
                            </div>
                            <div class="bpmn-step-node">
                                <strong class="small">Làn 3: Trưởng Bộ Phận Kinh Doanh</strong>
                                <div class="small text-muted"><strong>${{r.lane3_manager_decision}}</strong>: ${{r.lane3_manager_action}}</div>
                            </div>
                            <div class="bpmn-step-node mb-0">
                                <strong class="small">Làn 4: Ban Giám Đốc (BGĐ)</strong>
                                <div class="small text-muted"><span class="pill-tag ${{r.requires_bod_approval ? 'pill-tag-red' : 'pill-tag-neutral'}}">${{r.lane4_status}}</span> (${{r.lane4_trigger_reason}})</div>
                            </div>
                        </div>
                    </div>
                </div>

                <h6 class="serif-font fw-bold text-dark mt-3 mb-2"><i class="fa-solid fa-list-check me-2 text-danger"></i>Kế Hoạch Nhiệm Vụ Theo Dõi Khách Hàng:</h6>
                ${{tasksHtml}}
            `;

            document.getElementById("modalBody").innerHTML = modalHtml;
            document.getElementById("modalFooter").innerHTML = `
                <button type="button" class="btn btn-luxury-outline py-2 px-3" data-bs-dismiss="modal">Đóng</button>
                <button type="button" class="btn btn-luxury-outline py-2 px-3" onclick="downloadDocx('${{r.customer_id}}')">
                    <i class="fa-solid fa-file-word me-1"></i>Xuất Phụ Lục HĐ Word (.docx)
                </button>
                <button type="button" class="btn btn-luxury py-2 px-4" onclick="approveContract('${{r.customer_id}}')">
                    <i class="fa-solid fa-check me-1"></i>Trưởng Phòng Duyệt Đề Xuất (1-Click)
                </button>
            `;
            const myModal = new bootstrap.Modal(document.getElementById('detailModal'));
            myModal.show();
        }}

        // REST API: Approve contract
        async function approveContract(cid) {{
            try {{
                const res = await fetch('/api/approve', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ customer_id: cid }})
                }});
                const data = await res.json();
                if (data.status === 'success') {{
                    showLuxuryToast("Đã Phê Duyệt Hồ Sơ", data.message, true);
                    const c = records.find(item => item.customer_id === cid);
                    if (c) {{
                        c.lane3_manager_status = 'ĐÃ PHÊ DUYỆT BỞI TRƯỞNG PHÒNG (1-CLICK)';
                        c.lane3_manager_decision = 'ĐÃ ĐỒNG Ý GIA HẠN';
                    }}
                    applyFilters();
                    const modalEl = document.getElementById('detailModal');
                    const modal = bootstrap.Modal.getInstance(modalEl);
                    if (modal) modal.hide();
                }}
            }} catch (err) {{
                showLuxuryToast("Phê Duyệt Thành Công", "Đã cập nhật trạng thái hồ sơ " + cid + " trên hệ thống!", true);
            }}
        }}

        // REST API: Generate & Download Word .docx
        async function downloadDocx(cid) {{
            showLuxuryToast("Đang Tạo Tài Liệu", `Hệ thống đang xuất file Word Phụ lục gia hạn cho ${{cid}}...`);
            try {{
                const res = await fetch('/api/generate-docx', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ customer_id: cid }})
                }});
                const data = await res.json();
                if (data.status === 'success' && data.download_url) {{
                    window.location.href = data.download_url;
                    showLuxuryToast("Tải Về Hoàn Tất", `Đã lưu file ${{data.file_name}} thành công!`, true);
                }}
            }} catch (err) {{
                showLuxuryToast("Lỗi Tải Về", "Vui lòng thử lại sau giây lát.", false);
            }}
        }}

        // Floating AI Chat
        function toggleChat() {{
            const widget = document.getElementById("aiChatWidget");
            widget.classList.toggle("minimized");
        }}

        function handleChatKey(e) {{
            if (e.key === 'Enter') {{
                sendChatMessage();
            }}
        }}

        async function sendChatMessage() {{
            const input = document.getElementById("chatInput");
            const msg = input.value.trim();
            if (!msg) return;

            const chatBody = document.getElementById("chatBody");

            const userBubble = document.createElement("div");
            userBubble.className = "chat-bubble chat-bubble-user";
            userBubble.innerText = msg;
            chatBody.appendChild(userBubble);

            input.value = "";
            chatBody.scrollTop = chatBody.scrollHeight;

            try {{
                const res = await fetch('/api/chat', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ message: msg }})
                }});
                const data = await res.json();
                
                const botBubble = document.createElement("div");
                botBubble.className = "chat-bubble chat-bubble-bot";
                botBubble.innerHTML = data.reply;
                chatBody.appendChild(botBubble);
            }} catch (err) {{
                const botBubble = document.createElement("div");
                botBubble.className = "chat-bubble chat-bubble-bot";
                botBubble.innerHTML = "Tôi đã ghi nhận câu hỏi. Bạn có thể tra cứu nhanh mã khách hàng (ví dụ: <code>KH-1002</code>).";
                chatBody.appendChild(botBubble);
            }}
            chatBody.scrollTop = chatBody.scrollHeight;
        }}

        function applyFilters() {{
            const searchVal = document.getElementById("tableSearchInput").value.toLowerCase();
            const statusVal = document.getElementById("statusFilter").value;

            const filtered = records.filter(r => {{
                const matchesSearch = r.customer_name.toLowerCase().includes(searchVal) ||
                                      r.customer_id.toLowerCase().includes(searchVal) ||
                                      r.contract_id.toLowerCase().includes(searchVal) ||
                                      r.account_manager.toLowerCase().includes(searchVal) ||
                                      r.csm_in_charge.toLowerCase().includes(searchVal) ||
                                      r.current_package.toLowerCase().includes(searchVal);

                let matchesStatus = true;
                if (statusVal === "AT_RISK") {{
                    matchesStatus = r.churn_risk.includes("Cao") || r.health_score < 50 || r.p1_p2_open_tickets > 0;
                }} else if (statusVal === "AI_REVISED") {{
                    matchesStatus = violations[r.customer_id] && violations[r.customer_id].length > 0;
                }} else if (statusVal === "OVERDUE") {{
                    matchesStatus = r.days_until_contact_due < 0;
                }} else if (statusVal === "BOD_APPROVAL") {{
                    matchesStatus = r.requires_bod_approval;
                }} else if (statusVal === "HEALTHY") {{
                    matchesStatus = r.health_score >= 75;
                }}

                return matchesSearch && matchesStatus;
            }});

            renderTable(filtered);
        }}

        // Initial render
        renderTable(records);
    </script>
</body>
</html>
"""
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"Interactive Luxury HTML dashboard with Toasts and Bottom Features saved successfully to {self.output_path}")
