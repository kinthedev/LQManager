# Quản lý & Kiểm tra Tài khoản Liên Quân Mobile

## 1. Giới thiệu

Phần mềm quản lý cục bộ và tự động kiểm tra tài khoản Liên Quân Mobile (Garena/Facebook). Hỗ trợ tra cứu nhanh các thông số tài nguyên, tình trạng bảo mật và trạng thái đăng nhập nhằm tối ưu hóa việc phân loại và lưu trữ tài khoản cá nhân.

---

## 2. Cấu trúc dữ liệu đầu vào & đầu ra

### 2.1. File nguồn (`accounts.txt`)

- Mỗi tài khoản được đặt trên một dòng độc lập.
- Định dạng phân tách bằng dấu gạch đứng `|`:

```text
tentaikhoan|matkhau
nhatvuong919789|th731269
user_test_02|pass_demo_123
```

### 2.2. Xuất dữ liệu (Export)

- Xuất danh sách tài khoản hợp lệ (Live) ra file riêng: `live_accounts.txt`.
- Xuất báo cáo đầy đủ thông số dưới dạng bảng: `report.csv` (dễ dàng mở bằng Excel).

---

## 3. Thiết kế giao diện người dùng (GUI)

### 3.1. Bảng dữ liệu chính

Hiển thị danh sách tài khoản trực quan với các cột:

| Cột             | Ý nghĩa / Giá trị hiển thị                                                        |
| :-------------- | :-------------------------------------------------------------------------------- |
| **STT**         | Thứ tự dòng nạp từ file.                                                          |
| **Tài khoản**   | Tên đăng nhập (Username).                                                         |
| **Mật khẩu**    | Mặc định hiển thị `••••••••` (click đúp hoặc ấn nút để hiện/sao chép).            |
| **Trạng thái**  | `Chưa check`, `Hoạt động` (Live), `Sai mật khẩu`, `Bị khóa` (Ban), `Kẹt Captcha`. |
| **Bảo mật**     | `Trắng thông tin` (chưa gắn SĐT/Email), `Đã gắn SĐT`, `Đã gắn Email`.             |
| **Tướng**       | Tổng số tướng sở hữu.                                                             |
| **Trang phục**  | Tổng số trang phục (Skin) sở hữu.                                                 |
| **Tài nguyên**  | Số lượng Vàng / Quân huy hiện có.                                                 |
| **Bậc Rank**    | Bậc xếp hạng hiện tại (Đồng, Bạc, Vàng, Kim Cương, Tinh Anh, Cao Thủ...).         |
| **Điểm uy tín** | Thang điểm 0 - 100 (phát hiện tài khoản bị cấm đấu rank/đấu thường).              |
| **Thao tác**    | Nút `Copy Pass`, `Check lại`, `Xóa khỏi bảng`.                                    |

### 3.2. Thanh công cụ điều khiển

- **Chọn File (.txt):** Tải dữ liệu vào bảng.
- **Bắt đầu Kiểm tra (Start Check):** Chạy tự động quét trạng thái lần lượt theo danh sách.
- **Dừng / Tạm dừng:** Kiểm soát tiến trình quét khi cần.
- **Bộ lọc (Filter):**
  - Lọc theo trạng thái: _Tất cả_, _Chỉ nick Live_, _Chỉ nick Ban_, _Trắng thông tin_.
  - Tìm kiếm theo tên tướng hoặc trang phục sở hữu.
- **Xuất kết quả:** Nút bấm xuất dữ liệu theo các tiêu chí đã lọc.

---

## 4. Tính năng chi tiết

- **Tự động kiểm tra trạng thái đăng nhập:**
  - Xác thực tính hợp lệ của cặp tài khoản/mật khẩu.
  - Phân loại lỗi chính xác: sai thông tin, tài khoản bị tạm khóa, hoặc tài khoản cần xác minh hai bước.
- **Thu thập thông tin In-game:**
  - Đồng bộ số lượng tướng, skin, tài nguyên mà không cần tải hay mở trực tiếp client game.
  - Đánh dấu độ an toàn thông tin tài khoản (trắng thông tin hay đã liên kết bảo mật).
- **Tiện ích sao chép nhanh:**
  - 1-click để copy tài khoản hoặc mật khẩu vào Clipboard.
- **Cơ chế kiểm soát an toàn (Anti-Block):**
  - Tùy chỉnh độ trễ (Delay) giữa mỗi lần kiểm tra (khuyến nghị 3 - 5 giây) để tránh bị chặn IP từ hệ thống Garena.
  - Hỗ trợ khung trình duyệt nổi (Webview) để can thiệp giải mã xác thực (Captcha) thủ công khi tài khoản bị yêu cầu.
