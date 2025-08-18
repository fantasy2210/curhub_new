# BÁO CÁO MINH CHỨNG: KIỂM THỬ HỆ THỐNG

**Dự án:** Xây dựng Hệ thống Quản lý Chương trình Đào tạo và Hỗ trợ Mở mã ngành đào tạo (CURHUB)

| Hạng mục | Nội dung |
| :--- | :--- |
| **Thời gian hoàn thành** | 31/05/2025 |
| **Người chịu trách nhiệm** | Nhóm xây dựng hệ thống |
| **Tần suất báo cáo** | Sau khi hoàn thành |
| **Hồ sơ** | Báo cáo kiểm thử, danh sách lỗi |

---

## 1. Chiến lược và Mục tiêu Kiểm thử Giai đoạn Nội bộ

Trong giai đoạn hiện tại, hệ thống được triển khai cho Ban Phát triển CTĐT của CELRI sử dụng và kiểm thử. Do đó, chiến lược kiểm thử tập trung vào:

1.  **Integration Testing (Kiểm thử Tích hợp):**
    - **Mục tiêu:** Đảm bảo các chức năng đã phát triển hoạt động trơn tru với nhau. Ví dụ: sau khi thêm một học phần vào CTĐT, nó phải hiển thị đúng trong khung chương trình và có thể tạo đề cương.
    - **Thực hiện:** Lập trình viên và thành viên nhóm CELRI cùng thực hiện.

2.  **End-to-End Workflow Testing (Kiểm thử Luồng nghiệp vụ từ đầu đến cuối):**
    - **Mục tiêu:** Xác minh các quy trình nghiệp vụ chính hoạt động đúng như thiết kế. Đây là phần quan trọng nhất của giai đoạn này.
    - **Các luồng chính cần kiểm thử:**
        - Luồng 1: Tạo mới một CTĐT hoàn chỉnh (nhập thông tin chung, thêm PO, PLO, thêm học phần, phân công giảng viên).
        - Luồng 2: Tạo và phê duyệt một đề cương học phần.
        - Luồng 3: Cập nhật một CTĐT đã có và tạo ra phiên bản mới.
    - **Thực hiện:** Chủ yếu do thành viên Ban Phát triển CTĐT của CELRI thực hiện với sự hỗ trợ của đội ngũ phát triển.

3.  **Usability Testing (Kiểm thử tính khả dụng):**
    - **Mục tiêu:** Thu thập phản hồi về trải nghiệm người dùng, xác định các điểm khó hiểu, các thao tác rườm rà cần cải thiện.
    - **Thực hiện:** Thành viên CELRI sử dụng và ghi nhận lại các góp ý.

## 2. Ví dụ: Kế hoạch Kiểm thử cho Luồng "Cập nhật và Quản lý Phiên bản CTĐT"

Dưới đây là danh sách các trường hợp kiểm thử chi tiết cho một luồng nghiệp vụ quan trọng đã được triển khai.

**Luồng nghiệp vụ:** Cập nhật CTĐT và Quản lý Phiên bản
**Actor:** Người dùng thuộc Ban Phát triển CTĐT (có quyền chỉnh sửa CTĐT)

| ID Test Case | Mô tả | Các bước thực hiện | Kết quả mong đợi | Loại Test | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_VER_01** | **Thành công:** Chỉnh sửa CTĐT ở trạng thái "Bản nháp". | 1. Đăng nhập với tài khoản được cấp quyền.<br>2. Mở một CTĐT có trạng thái "Bản nháp".<br>3. Tại tab "Khung chương trình", sửa trực tiếp học kỳ của một học phần.<br>4. Tải lại trang. | 1. Hệ thống báo "Cập nhật thành công" ngay sau khi sửa.<br>2. Sau khi tải lại, thông tin học kỳ mới được lưu lại chính xác. | Positive | Pass |
| **TC_VER_02** | **Thất bại:** Cố gắng chỉnh sửa CTĐT ở trạng thái "Đã phê duyệt". | 1. Đăng nhập với tài khoản được cấp quyền.<br>2. Mở một CTĐT có trạng thái "Đã phê duyệt".<br>3. Cố gắng sửa trực tiếp học kỳ của một học phần. | 1. Giao diện không cho phép sửa (ô nhập bị vô hiệu hóa) hoặc API trả về lỗi "Chỉ có thể chỉnh sửa khi CTĐT ở trạng thái 'Bản nháp'".<br>2. Dữ liệu không thay đổi. | Negative | Pass |
| **TC_VER_03** | **Thành công:** Tạo phiên bản mới từ một CTĐT đã phê duyệt. | 1. Mở một CTĐT có trạng thái "Đã phê duyệt".<br>2. Nhấn nút "Tạo phiên bản mới".<br>3. Nhập "Lý do thay đổi" và xác nhận.<br>4. Hệ thống chuyển đến trang chi tiết của CTĐT phiên bản mới. | 1. Một CTĐT mới được tạo ra.<br>2. CTĐT mới có trạng thái "Bản nháp".<br>3. Số phiên bản được tăng lên (ví dụ: từ 1.0 thành 1.1 hoặc 2.0).<br>4. CTĐT mới có liên kết đến phiên bản gốc.<br>5. Toàn bộ cấu trúc (học phần, CĐR) được sao chép sang phiên bản mới. | Workflow | Pass |
| **TC_VER_04** | **Thành công:** Gửi duyệt một CTĐT "Bản nháp". | 1. Mở một CTĐT có trạng thái "Bản nháp".<br>2. Nhấn nút "Gửi duyệt".<br>3. Xác nhận hành động. | 1. Trạng thái của CTĐT chuyển thành "Chờ duyệt".<br>2. Các chức năng chỉnh sửa bị vô hiệu hóa.<br>3. Hệ thống gửi thông báo (email) đến người có thẩm quyền phê duyệt. | Workflow | Pass |
| **TC_VER_05** | **Thành công:** Phê duyệt một CTĐT "Chờ duyệt". | 1. Đăng nhập bằng tài khoản có quyền phê duyệt.<br>2. Mở CTĐT có trạng thái "Chờ duyệt".<br>3. Nhấn nút "Phê duyệt".<br>4. Nhập ghi chú (nếu có) và xác nhận. | 1. Trạng thái của CTĐT chuyển thành "Đã phê duyệt".<br>2. Hệ thống ghi nhận người phê duyệt và thời gian phê duyệt. | Workflow | Pass |

---
**KẾT LUẬN**

Quy trình kiểm thử được xây dựng một cách bài bản và có hệ thống, đảm bảo rằng tất cả các chức năng của CURHUB đều được kiểm tra kỹ lưỡng trước khi đưa vào sử dụng. Việc áp dụng các cấp độ kiểm thử khác nhau giúp phát hiện sớm các lỗi tiềm ẩn, từ đó nâng cao chất lượng, độ tin cậy và tính ổn định của sản phẩm.
