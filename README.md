# HỆ THỐNG AI AGENT ĐIỀU PHỐI & THẨM ĐỊNH GIA HẠN HỢP ĐỒNG - CÔNG TY AN TÍN

Hệ thống AI Agent giải quyết toàn diện bài toán gia hạn hợp đồng B2B SaaS cho Công ty An Tín, tích hợp mô hình ngôn ngữ lớn **Google Gemini (Gemini 3.8 Flash)** kết hợp động cơ thẩm định nghiệp vụ (Deterministic Rules Engine), tự động hóa quy trình theo đúng **Sơ đồ vận hành 4 làn bơi (BPMN)**, triệt tiêu 4 sai phạm kinh điển và phục vụ trực tiếp trên **Localhost:8000**.

---

## 1. Các Tính Năng Đang Chạy Trên Localhost (`http://localhost:8000`)

* **Web Dashboard Tương Tác**: Quản lý 120 hợp đồng, lọc theo rủi ro, xem tiến độ 4 làn BPMN.
* **AI Agent Co-Pilot (Chatbox Trực Tuyến)**: Tích hợp Gemini 3.8 Flash, hỏi đáp tự nhiên, tra cứu hồ sơ 360 độ, tư vấn chiến lược đàm phán và giải trình căn cứ.
* **1-Click Phê Duyệt**: Trưởng phòng Kinh doanh duyệt nhanh đề xuất hợp lệ chỉ với 1 click, tự động cập nhật hệ thống.
* **Tự Động Sinh Phụ Lục Hợp Đồng Word (.docx)**: Tạo ngay phụ lục hợp đồng mẫu chuẩn pháp lý có đầy đủ điều khoản SLA, bảng giá sau ưu đãi để khách hàng ký kết.

---

## 2. Kiến Trúc Dual-Engine (Hybrid AI Architecture)

```
                   [Người Dùng: Trưởng Phòng / CSKH / Sales]
                                          │
                     ┌────────────────────┴────────────────────┐
                     ▼                                         ▼
           [Giao Diện Web / Chat]                        [Công Cụ CLI]
             (localhost:8000)                              (cli.py)
                     │                                         │
                     └────────────────────┬────────────────────┘
                                          │
                                 [HỆ THỐNG AI AGENT]
                                          │
            ┌─────────────────────────────┴─────────────────────────────┐
            ▼                                                           ▼
 [Deterministic Rule Engine]                                [Gemini 3.8 Flash LLM]
  • Rà soát & chặn 4 sai sót                                 • Phân tích ngôn ngữ tự nhiên
  • Chấm điểm sức khỏe (0-100)                               • Soạn thảo email/kịch bản đàm phán
  • Kiểm tra trần chiết khấu                                 • Giải trình chuyên sâu cho BGĐ
  • Sinh Action Tasks BPMN                                   • Tư vấn xử lý tình huống khẩn cấp
```

---

## 3. Cấu Trúc Mã Nguồn

```text
Agent QTKD1/
├── .env                                # Cấu hình bảo mật API Key (Gemini API Key)
├── .gitignore                          # Ngăn chặn rò rỉ credential
├── data/                               # Dữ liệu nguồn mô phỏng
│   ├── contracts.csv                   # 120 hợp đồng khách hàng
│   ├── usage_logs.csv                  # Nhật ký hoạt động, Active users, Storage
│   ├── support_tickets.csv             # Lịch sử sự cố, trạng thái, CSAT
│   ├── service_packages.json           # Danh mục gói & định mức giá
│   └── discount_policies.json          # Quy chế ưu đãi & hạn mức
├── engine/                             # Các module AI Agent chuyên trách
│   ├── data_loader.py                  # Thu thập & đối soát theo Ngày đối chiếu
│   ├── audit_engine.py                 # Rà soát & khắc phục 4 sai phạm
│   ├── health_scorer.py                # Chấm điểm Sức khỏe & Rủi ro Churn (0-100)
│   ├── recommendation_engine.py        # Đề xuất gói & ưu đãi có căn cứ định lượng
│   ├── workflow_tracker.py             # Điều phối 4 làn bơi & phân công nhiệm vụ
│   ├── doc_generator.py                # Tự động sinh Phụ lục Hợp đồng Word (.docx)
│   ├── llm_client.py                   # Kết nối Google Gemini 3.8 Flash
│   ├── excel_exporter.py               # Xuất bộ báo cáo Excel 5 Sheets cao cấp
│   └── html_dashboard.py               # Sinh Dashboard trực quan tương tác
├── output/                             # Sản phẩm đầu ra
│   ├── Bao_Cao_Gia_Han_Hop_Dong_An_Tin.xlsx
│   ├── Dashboard_Gia_Han_An_Tin.html
│   └── Phu_Luc_Gia_Han_*.docx
├── cli.py                              # Công cụ dòng lệnh tra cứu & quản trị
├── simulate_agents.py                  # Mô phỏng tranh luận & phối hợp Multi-Agent
├── server.py                           # Máy chủ Web Localhost & REST API
├── main.py                             # Pipeline chính thực thi hệ thống
└── README.md                           # Tài liệu hướng dẫn
```

---

## 4. Hướng Dẫn Sử Dụng

### 1. Truy cập Web Dashboard & Chatbot:

Mở trình duyệt bất kỳ: **`http://localhost:8000`**

### 2. Sử dụng công cụ CLI:

* Xem tổng quan KPIs: `python cli.py summary`
* Tra cứu hồ sơ 360 độ: `python cli.py inspect KH-1002`
* Xuất file Word Phụ lục: `python cli.py export-docx KH-1002`
* Xem danh sách nhiệm vụ: `python cli.py tasks --role cskh`

### 3. Chạy kịch bản mô phỏng Multi-Agent:

```powershell
python simulate_agents.py
```
