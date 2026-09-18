# Tool Quản lý & Kiểm tra Tài khoản Liên Quân Mobile

Xây dựng ứng dụng desktop GUI quản lý tài khoản Liên Quân Mobile theo yêu cầu trong [requirement.md](file:///home/kin/Documents/LQManager/docs/requirement.md). Ứng dụng cho phép import danh sách tài khoản, mô phỏng kiểm tra trạng thái, hiển thị thông tin in-game, và export kết quả.

## User Review Required

> [!IMPORTANT]
> **Về tính năng "kiểm tra trạng thái đăng nhập" và "thu thập thông tin in-game":** Garena không cung cấp public API cho việc xác thực tài khoản hay lấy thông tin in-game. Việc thực sự đăng nhập vào Garena và thu thập dữ liệu in-game yêu cầu reverse-engineering API Garena/Liên Quân, có thể vi phạm ToS và rất phức tạp. 
>
> **Giải pháp:** Tôi sẽ xây dựng toàn bộ kiến trúc ứng dụng hoàn chỉnh với **mock/simulated check engine** — tức là phần logic kiểm tra sẽ **sinh dữ liệu mô phỏng** (random trạng thái, tướng, skin...) để demo giao diện. Kiến trúc được thiết kế modular để sau này bạn có thể thay thế mock engine bằng engine thực khi có API phù hợp.

> [!IMPORTANT]  
> **Chọn công nghệ:** Tôi đề xuất dùng **Python + CustomTkinter** (giao diện desktop modern, dark theme, không cần cài thêm browser). Đây là lựa chọn nhẹ nhàng, dễ đóng gói thành `.exe`, và phù hợp cho tool cá nhân.

## Open Questions

1. **Ngôn ngữ lập trình:** Bạn có muốn dùng Python + CustomTkinter như đề xuất, hay muốn dùng công nghệ khác (Electron, C# WinForms, Java...)?
2. **Tính năng Webview giải Captcha:** Do dùng CustomTkinter (không có built-in webview), tính năng mở Webview giải Captcha thủ công sẽ được bỏ qua hoặc thay bằng mở trình duyệt mặc định. Bạn có chấp nhận không?

---

## Proposed Changes

### Cấu trúc dự án

```
LQManager/
├── docs/
│   └── requirement.md
├── data/                       # [NEW] Thư mục chứa file dữ liệu
│   └── accounts_sample.txt     # [NEW] File mẫu
├── src/                        # [NEW] Source code chính
│   ├── __init__.py
│   ├── main.py                 # [NEW] Entry point
│   ├── app.py                  # [NEW] Main application window
│   ├── models.py               # [NEW] Data models (Account, CheckResult)
│   ├── account_parser.py       # [NEW] Parser cho file accounts.txt
│   ├── check_engine.py         # [NEW] Mock check engine (interface + simulation)
│   ├── exporter.py             # [NEW] Export live_accounts.txt & report.csv
│   ├── widgets/                # [NEW] Custom widgets
│   │   ├── __init__.py
│   │   ├── account_table.py    # [NEW] Bảng dữ liệu chính (Treeview)
│   │   ├── toolbar.py          # [NEW] Thanh công cụ điều khiển
│   │   ├── filter_bar.py       # [NEW] Bộ lọc
│   │   └── status_bar.py       # [NEW] Thanh trạng thái (tiến trình check)
│   └── utils.py                # [NEW] Clipboard, formatting helpers
├── requirements.txt            # [NEW] Dependencies
└── README.md                   # [NEW] Hướng dẫn sử dụng
```

---

### Data Models — [models.py](file:///home/kin/Documents/LQManager/src/models.py)

#### [NEW] models.py

Định nghĩa dataclass:

- `Account`: username, password, status (`Chưa check` / `Hoạt động` / `Sai mật khẩu` / `Bị khóa` / `Kẹt Captcha`), security_info, heroes_count, skins_count, gold, military_rank, credibility_score
- `CheckResult`: Kết quả trả về từ engine sau khi check 1 tài khoản

---

### Account Parser — [account_parser.py](file:///home/kin/Documents/LQManager/src/account_parser.py)

#### [NEW] account_parser.py

- Đọc file `.txt`, parse mỗi dòng theo format `username|password`
- Bỏ qua dòng trống, dòng comment
- Trả về `list[Account]`

---

### Check Engine — [check_engine.py](file:///home/kin/Documents/LQManager/src/check_engine.py)

#### [NEW] check_engine.py

- Abstract base class `BaseCheckEngine` với method `check(account) -> CheckResult`
- Concrete class `MockCheckEngine`:
  - Mô phỏng delay (configurable, mặc định 3-5 giây)
  - Random trạng thái: ~60% Live, ~20% Sai MK, ~10% Bị khóa, ~10% Captcha
  - Random thông tin in-game: số tướng (10-100), skin (5-200), vàng (1000-999999), rank, điểm uy tín (0-100)
  - Random bảo mật: Trắng thông tin / Đã gắn SĐT / Đã gắn Email
- Chạy trong **background thread** để không block GUI

---

### Exporter — [exporter.py](file:///home/kin/Documents/LQManager/src/exporter.py)

#### [NEW] exporter.py

- `export_live_accounts(accounts, filepath)`: Xuất chỉ tài khoản có trạng thái `Hoạt động` ra `.txt`
- `export_report_csv(accounts, filepath)`: Xuất toàn bộ thông tin ra `.csv` với header tiếng Việt

---

### GUI — Main Application

#### [NEW] [app.py](file:///home/kin/Documents/LQManager/src/app.py)

- Window chính dùng CustomTkinter
- Layout: Toolbar (trên) → Filter Bar → Account Table (giữa, chiếm chính) → Status Bar (dưới)
- Quản lý state: danh sách accounts, trạng thái check (running/paused/stopped)

#### [NEW] [toolbar.py](file:///home/kin/Documents/LQManager/src/widgets/toolbar.py)

- Nút **Chọn File**: mở file dialog `.txt`
- Nút **Bắt đầu Kiểm tra**: start check engine trong thread
- Nút **Tạm dừng / Tiếp tục**: toggle pause
- Nút **Dừng**: stop hoàn toàn
- Nút **Xuất Live**: export live accounts
- Nút **Xuất Báo cáo CSV**: export report
- Thanh trượt **Delay**: điều chỉnh delay giữa mỗi lần check (1-10 giây)

#### [NEW] [account_table.py](file:///home/kin/Documents/LQManager/src/widgets/account_table.py)

- Bảng Treeview với đầy đủ các cột theo requirement
- Mật khẩu hiển thị `••••••••`, double-click để hiện/ẩn
- Nút thao tác trên mỗi dòng: Copy Pass, Check lại, Xóa
- Color-coding: Hoạt động (xanh), Sai MK (đỏ), Bị khóa (cam), Captcha (vàng)
- Context menu (right-click) với các thao tác nhanh

#### [NEW] [filter_bar.py](file:///home/kin/Documents/LQManager/src/widgets/filter_bar.py)

- Dropdown lọc theo trạng thái: Tất cả / Chỉ nick Live / Chỉ nick Ban / Trắng thông tin
- Ô tìm kiếm theo tên tài khoản

#### [NEW] [status_bar.py](file:///home/kin/Documents/LQManager/src/widgets/status_bar.py)

- Progress bar hiển thị tiến trình check
- Label: "Đã check X/Y | Live: A | Ban: B | Sai MK: C"

---

### Entry Point & Config

#### [NEW] [main.py](file:///home/kin/Documents/LQManager/src/main.py)

- Khởi tạo app, chạy mainloop

#### [NEW] [requirements.txt](file:///home/kin/Documents/LQManager/requirements.txt)

```
customtkinter>=5.2.0
```

#### [NEW] [README.md](file:///home/kin/Documents/LQManager/README.md)

- Hướng dẫn cài đặt, chạy, sử dụng

---

## Verification Plan

### Automated Tests

```bash
cd /home/kin/Documents/LQManager
python -m pytest tests/ -v    # (nếu có thời gian viết test)
```

### Manual Verification

1. Chạy `python src/main.py` — kiểm tra GUI hiển thị đúng
2. Chọn file `data/accounts_sample.txt` — kiểm tra bảng load dữ liệu
3. Nhấn "Bắt đầu Kiểm tra" — kiểm tra mock engine chạy, cập nhật bảng real-time
4. Thử Pause/Resume/Stop
5. Thử các bộ lọc
6. Double-click mật khẩu để hiện/ẩn
7. Xuất `live_accounts.txt` và `report.csv` — kiểm tra nội dung file
