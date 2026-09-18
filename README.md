# LQManager - Quản lý Tài khoản Liên Quân Mobile

Công cụ desktop quản lý và kiểm tra hàng loạt tài khoản Liên Quân Mobile. Giao diện được xây dựng bằng **CustomTkinter** với thiết kế Dark Mode hiện đại.

> **Lưu ý:** Phiên bản hiện tại sử dụng **Mock Check Engine** (giả lập kiểm tra tài khoản) để demo giao diện. Kiến trúc modular cho phép thay thế bằng engine thực khi có API phù hợp.

## Tính năng

- 📂 Nhập tài khoản từ file `.txt` (định dạng `username|password`)
- ✅ Kiểm tra trạng thái tài khoản: Hoạt động, Sai MK, Bị khóa, Kẹt Captcha
- 📊 Hiển thị thông tin chi tiết: Tướng, Trang phục, Vàng, Quân huy, Bậc Rank, Điểm uy tín
- 🔍 Lọc theo trạng thái, tìm kiếm theo tên tài khoản
- 💾 Xuất tài khoản Live ra file `.txt`
- 📈 Xuất báo cáo đầy đủ ra file `.csv` (mở được bằng Excel)
- ⏯ Tạm dừng / Tiếp tục / Dừng tiến trình kiểm tra
- ⏱ Tùy chỉnh độ trễ (delay) giữa mỗi lần check (1-10 giây)
- 🔐 Mật khẩu ẩn mặc định, double-click để hiện
- 📋 Right-click context menu: Copy tài khoản, Copy mật khẩu, Check lại, Xóa

## Yêu cầu hệ thống

- Python 3.10+
- tkinter (thường đi kèm Python, trên Arch Linux cần `sudo pacman -S tk`)

## Cài đặt

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# Cài dependencies
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
source venv/bin/activate
python src/main.py
```

## Cấu trúc dự án

```
LQManager/
├── data/
│   └── accounts_sample.txt     # File tài khoản mẫu
├── docs/
│   ├── requirement.md          # Yêu cầu chi tiết
│   └── implementation_plan.md  # Kế hoạch triển khai
├── src/
│   ├── main.py                 # Entry point
│   ├── app.py                  # Main application window
│   ├── models.py               # Data models
│   ├── account_parser.py       # Parser file accounts
│   ├── check_engine.py         # Mock check engine
│   ├── exporter.py             # Export CSV/TXT
│   ├── utils.py                # Utility helpers
│   └── widgets/
│       ├── account_table.py    # Bảng dữ liệu chính
│       ├── toolbar.py          # Thanh công cụ
│       ├── filter_bar.py       # Bộ lọc
│       └── status_bar.py       # Thanh trạng thái
├── requirements.txt
└── README.md
```

## Sử dụng

1. Nhấn **📂 Chọn File** để tải file tài khoản (format: `username|password` mỗi dòng)
2. Điều chỉnh **Delay** bằng thanh trượt (khuyến nghị 3-5 giây)
3. Nhấn **▶ Bắt đầu Kiểm tra** để bắt đầu quét
4. Sử dụng bộ lọc để xem chỉ nick Live, Ban, v.v.
5. Nhấn **💾 Xuất Live** hoặc **📊 Xuất CSV** để lưu kết quả

## Ảnh chụp màn hình

_(Sẽ được cập nhật)_
# LQManager
