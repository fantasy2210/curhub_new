# BÁO CÁO MINH CHỨNG: ĐÁNH GIÁ VÀ ĐIỀU CHỈNH LẦN 1

**Dự án:** Xây dựng Hệ thống Quản lý Chương trình Đào tạo và Hỗ trợ Mở mã ngành đào tạo (CURHUB)

| Hạng mục | Nội dung |
| :--- | :--- |
| **Thời gian hoàn thành** | 30/06/2025 |
| **Người chịu trách nhiệm** | Nhóm xây dựng hệ thống |
| **Tần suất báo cáo** | Sau khi hoàn thành |
| **Hồ sơ** | Báo cáo đánh giá, kế hoạch điều chỉnh |

---

## 1. Mục đích

Báo cáo này nhằm mục đích đánh giá tổng thể hệ thống CURHUB sau khi hoàn thành các giai đoạn phát triển và kiểm thử ban đầu. Dựa trên kết quả đánh giá, báo cáo sẽ đề xuất một kế hoạch điều chỉnh để cải tiến và hoàn thiện sản phẩm trước khi bước vào giai đoạn triển khai thử nghiệm.

## 2. Tóm tắt Kết quả Đánh giá

### 2.1. Các Hạng mục Đã Hoàn thành Tốt

- **Đáp ứng yêu cầu chức năng cốt lõi:** Hệ thống đã triển khai thành công các chức năng chính được mô tả trong tài liệu đặc tả, bao gồm quản lý CTĐT, quản lý học phần, quản lý CĐR, và các quy trình phê duyệt cơ bản.
- **Kiến trúc hệ thống vững chắc:** Kiến trúc Modular Monolith trên nền tảng Django đã chứng tỏ được sự ổn định, hiệu quả và dễ dàng cho việc phát triển, bảo trì.
- **Giao diện người dùng thân thiện:** Giao diện dựa trên AdminLTE nhận được phản hồi tích cực về tính dễ sử dụng, rõ ràng và nhất quán.
- **Kết quả kiểm thử:** Tỷ lệ pass của các test case cho các chức năng cốt lõi đạt trên 95%. Các lỗi nghiêm trọng (critical/blocker) đã được phát hiện và khắc phục.

### 2.2. Các Vấn đề Tồn đọng và Điểm cần Cải thiện

Qua quá trình kiểm thử nội bộ và thu thập phản hồi ban đầu, một số vấn đề đã được ghi nhận:

| ID Vấn đề | Phân loại | Mô tả Vấn đề | Mức độ Ưu tiên |
| :--- | :--- | :--- | :--- |
| **ISSUE-01** | Hiệu năng | Chức năng "Đối sánh CTĐT" (UC-15) có thời gian phản hồi chậm (trên 15 giây) khi so sánh hai chương trình có nhiều học phần. | Cao |
| **ISSUE-02** | UX/UI | Luồng công việc "Quản lý phiên bản CTĐT" (UC-05) còn hơi phức tạp. Người dùng cần nhiều bước để xem sự khác biệt giữa hai phiên bản. | Trung bình |
| **ISSUE-03** | Chức năng | Hệ thống chưa có chức năng thông báo (notification) real-time trong giao diện web. Thông báo hiện chỉ gửi qua email, có thể gây chậm trễ. | Trung bình |
| **ISSUE-04** | Chức năng | Chức năng xuất báo cáo (UC-09) còn thiếu một số mẫu báo cáo theo yêu cầu của TT.HL-DH, ví dụ: báo cáo thống kê số lượng giảng viên tham gia CTĐT theo học hàm/học vị. | Thấp |
| **ISSUE-05** | Nghiệp vụ | Quy tắc kiểm tra điều kiện tiên quyết giữa các học phần (UC-03) chưa xử lý được các trường hợp phức tạp (ví dụ: học phần A yêu cầu học trước 1 trong 2 học phần B hoặc C). | Cao |

## 3. Kế hoạch Điều chỉnh và Cải tiến

Dựa trên các vấn đề đã xác định, nhóm xây dựng hệ thống đề xuất kế hoạch điều chỉnh sau:

| ID Vấn đề | Giải pháp Đề xuất | Người thực hiện | Thời gian Dự kiến |
| :--- | :--- | :--- | :--- |
| **ISSUE-01** | - Tối ưu hóa câu lệnh truy vấn CSDL cho chức năng đối sánh.<br>- Áp dụng kỹ thuật caching cho các dữ liệu ít thay đổi.<br>- Xem xét thực thi tác vụ đối sánh ở chế độ nền (background task) cho các CTĐT lớn. | Backend Team | 2 tuần |
| **ISSUE-02** | - Thiết kế lại giao diện so sánh phiên bản, hiển thị các thay đổi (thêm/sửa/xóa) một cách trực quan hơn, làm nổi bật các điểm khác biệt.<br>- Bổ sung nút "Xem nhanh thay đổi" ngay trên danh sách phiên bản. | Frontend Team, UX Designer | 3 tuần |
| **ISSUE-03** | - Tích hợp thư viện (ví dụ: Django Channels, WebSockets) để xây dựng hệ thống thông báo real-time.<br>- Thêm biểu tượng chuông thông báo trên thanh header. | Backend Team, Frontend Team | 3 tuần |
| **ISSUE-04** | - Làm việc với TT.HL-DH để thu thập yêu cầu chi tiết về các mẫu báo cáo còn thiếu.<br>- Phát triển và bổ sung các mẫu báo cáo mới vào hệ thống. | Backend Team | 2 tuần |
| **ISSUE-05** | - Mở rộng mô hình dữ liệu `HocPhan` để hỗ trợ các quy tắc điều kiện tiên quyết phức tạp (ví dụ: sử dụng một trường text để lưu biểu thức logic).<br>- Cập nhật backend service để phân tích và thực thi các quy tắc này. | Backend Team, DB Designer | 4 tuần |

---
**KẾT LUẬN**

Giai đoạn phát triển và kiểm thử lần 1 đã đạt được những mục tiêu quan trọng, xây dựng được một nền tảng hệ thống vững chắc. Các vấn đề còn tồn đọng đã được nhận diện và có kế hoạch khắc phục rõ ràng. Việc thực hiện thành công kế hoạch điều chỉnh này sẽ giúp nâng cao chất lượng sản phẩm, sẵn sàng cho giai đoạn triển khai thử nghiệm với người dùng cuối.
