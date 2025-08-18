# BÁO CÁO MINH CHỨNG: PHÁT TRIỂN GIAO DIỆN NGƯỜI DÙNG

**Dự án:** Xây dựng Hệ thống Quản lý Chương trình Đào tạo và Hỗ trợ Mở mã ngành đào tạo (CURHUB)

| Hạng mục | Nội dung |
| :--- | :--- |
| **Thời gian hoàn thành** | 28/02/2025 |
| **Người chịu trách nhiệm** | Nhóm xây dựng hệ thống |
| **Tần suất báo cáo** | Sau khi hoàn thành |
| **Hồ sơ** | Các giao diện người dùng |

---

## 1. Tổng quan Thiết kế Giao diện (UI/UX)

Giao diện người dùng (UI) của hệ thống CURHUB được xây dựng dựa trên theme **AdminLTE**, một template quản trị phổ biến, responsive và thân thiện với người dùng. Thiết kế tập trung vào các nguyên tắc sau:

- **Tính nhất quán:** Các màn hình có bố cục, màu sắc và cách sử dụng các thành phần (nút, bảng, form) đồng nhất, giúp người dùng dễ dàng làm quen và sử dụng.
- **Tính rõ ràng:** Thông tin được trình bày một cách có tổ chức, ưu tiên các chức năng quan trọng. Các nhãn, tiêu đề và thông báo được viết rõ ràng, dễ hiểu.
- **Tính hiệu quả:** Tối ưu hóa luồng công việc, giảm thiểu số lần nhấp chuột cần thiết để hoàn thành một tác vụ. Các chức năng tìm kiếm, lọc và sắp xếp được tích hợp để giúp người dùng truy xuất thông tin nhanh chóng.
- **Thiết kế Responsive:** Giao diện tự động điều chỉnh để hiển thị tốt trên các kích thước màn hình khác nhau, từ máy tính để bàn đến máy tính bảng và điện thoại di động.

## 2. Mô tả các Giao diện Chính

Dưới đây là mô tả chi tiết về một số giao diện người dùng tiêu biểu của hệ thống.

### 2.1. Giao diện: Danh sách Chương trình Đào tạo (`danh_sach_ctdt.html`)

**Mục đích:** Hiển thị danh sách tất cả các chương trình đào tạo có trong hệ thống, cho phép người dùng tìm kiếm, lọc và thực hiện các thao tác cơ bản.

**Bố cục và Thành phần:**

1.  **Thanh điều hướng (Navigation Bar):** Nằm ở bên trái, chứa menu truy cập nhanh đến các module chính của hệ thống (Quản lý CTĐT, Mở ngành, Báo cáo, Quản trị).
2.  **Tiêu đề trang:** "Danh sách Chương trình Đào tạo".
3.  **Khu vực Chức năng:**
    - **Nút "Thêm mới CTĐT":** Nổi bật ở góc trên bên phải, cho phép người dùng có quyền tạo một CTĐT mới.
    - **Bộ lọc (Filters):** Các ô chọn (dropdown) để lọc danh sách theo:
        - Trình độ đào tạo (Đại học, Thạc sĩ, Tiến sĩ).
        - Đơn vị quản lý (Khoa/Viện).
        - Trạng thái (Đang hoạt động, Ngừng tuyển sinh).
    - **Thanh tìm kiếm:** Cho phép tìm kiếm nhanh theo Tên CTĐT hoặc Mã ngành.
4.  **Bảng dữ liệu (Data Table):**
    - Hiển thị danh sách các CTĐT dưới dạng bảng, có phân trang.
    - **Các cột:** STT, Tên chương trình đào tạo, Mã ngành, Trình độ, Đơn vị quản lý, Phiên bản, Trạng thái.
    - **Cột "Hành động":** Chứa các nút chức năng cho mỗi dòng:
        - **Xem chi tiết:** Điều hướng đến trang chi tiết của CTĐT.
        - **Sửa:** Mở form chỉnh sửa thông tin CTĐT.
        - **Xóa:** Mở hộp thoại xác nhận xóa CTĐT.
        - **Đối sánh:** Bắt đầu quy trình đối sánh CTĐT.

### 2.2. Giao diện: Chi tiết Chương trình Đào tạo (`chi_tiet_ctdt.html`)

**Mục đích:** Hiển thị toàn bộ thông tin chi tiết về một chương trình đào tạo, là trung tâm để quản lý tất cả các thành phần liên quan.

**Bố cục và Thành phần:**

1.  **Tiêu đề trang:** "Chi tiết CTĐT: [Tên chương trình đào tạo]".
2.  **Khu vực Thông tin tổng quan:**
    - Hiển thị các thông tin cơ bản của CTĐT: Mã ngành, Trình độ, Đơn vị quản lý, Phiên bản, **Trạng thái** (Bản nháp, Chờ duyệt, Đã phê duyệt).
    - **Các nút hành động theo ngữ cảnh:**
        - Nếu trạng thái là "Bản nháp": Hiển thị nút "Gửi duyệt", "Sửa", "Tạo phiên bản mới".
        - Nếu trạng thái là "Chờ duyệt" (đối với người có quyền): Hiển thị nút "Phê duyệt", "Từ chối/Yêu cầu chỉnh sửa".
3.  **Hệ thống Tab (Tabbed Interface):** Giao diện được chia thành nhiều tab để tổ chức thông tin:
    - **Tab "Mục tiêu (PO) & Chuẩn đầu ra (PLO)":**
        - Hiển thị danh sách các Mục tiêu đào tạo (PO) và Chuẩn đầu ra (PLO) của CTĐT.
        - Cho phép Thêm/Sửa/Xóa PO và PLO thông qua các form trong modal (cửa sổ pop-up), được xử lý bằng API để không cần tải lại trang.
    - **Tab "Khung chương trình":**
        - Hiển thị danh sách các học phần trong CTĐT dưới dạng bảng, có thể chỉnh sửa trực tiếp (inline editing) các thông tin như học kỳ, số tín chỉ áp dụng, loại học phần (bắt buộc/tự chọn).
        - Các chức năng chính: "Thêm học phần từ thư viện", "Thêm học phần hàng loạt" (từ file Excel).
    - **Tab "Ma trận CĐR":**
        - (Chức năng đang phát triển) Hiển thị ma trận tương quan giữa PLO của CTĐT và CLO của các học phần.
    - **Tab "Đề cương học phần":**
        - Liệt kê danh sách các học phần và trạng thái đề cương. Cung cấp liên kết để đi đến trang quản lý chi tiết đề cương cho từng học phần.
    - **Tab "Giảng viên tham gia":**
        - Hiển thị và cho phép quản lý danh sách giảng viên được phân công cho CTĐT.
    - **Tab "Lịch sử & Phiên bản":**
        - Hiển thị lịch sử các thay đổi và danh sách các phiên bản trước đó của CTĐT.
        - Cho phép so sánh sự khác biệt giữa các phiên bản.
    - **Tab "Lưu đồ chương trình":**
        - Sử dụng API để lấy dữ liệu và vẽ lưu đồ các học phần, thể hiện mối quan hệ tiên quyết/song hành một cách trực quan.

---
**KẾT LUẬN**

Thiết kế giao diện người dùng của CURHUB hướng tới sự đơn giản, hiệu quả và thân thiện. Bằng cách sử dụng các mẫu thiết kế quen thuộc và tổ chức thông tin một cách logic, hệ thống giúp người dùng dễ dàng thực hiện các nghiệp vụ phức tạp, từ đó nâng cao hiệu quả công việc và trải nghiệm người dùng.
