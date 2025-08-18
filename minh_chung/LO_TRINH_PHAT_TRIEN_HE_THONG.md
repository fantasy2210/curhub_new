# Lộ trình Xây dựng các Use Case còn lại cho Hệ thống CURHUB

Dựa trên báo cáo tiến độ ngày 18/08/2025, lộ trình này được xây dựng để hoàn thiện các chức năng còn thiếu của hệ thống, đảm bảo tính toàn vẹn của các chức năng đã có và đưa ra các checkpoint (cột mốc kiểm tra) rõ ràng.

---

## Giai đoạn 1: Hoàn thiện các chức năng lõi của Module Quản lý CTĐT

**Mục tiêu:** Hoàn thiện các chức năng đang dang dở và bổ sung các tính năng quản lý phiên bản quan trọng để đảm bảo sự ổn định và toàn vẹn dữ liệu của module cốt lõi.

1.  **Hoàn thiện UC-02c (Phê duyệt CĐR)**
    *   **Nội dung:** Tách quy trình phê duyệt Chuẩn đầu ra (CĐR) ra khỏi quy trình phê duyệt Chương trình đào tạo (CTĐT) chung để tăng tính linh hoạt.
    *   **Checkpoint:** Người dùng có thẩm quyền (ví dụ: Trưởng khoa) có thể xem danh sách các CĐR đang chờ duyệt, thực hiện phê duyệt hoặc từ chối một bộ CĐR một cách độc lập với toàn bộ CTĐT.

2.  **Xây dựng UC-04d (Quản lý phiên bản đề cương)**
    *   **Nội dung:** Phát triển chức năng cho phép hệ thống tự động lưu lại một phiên bản mới của đề cương mỗi khi có sự thay đổi và được phê duyệt. Bổ sung giao diện để xem lại lịch sử và so sánh các phiên bản.
    *   **Checkpoint:** Trong trang chi tiết học phần, người dùng có thể truy cập vào lịch sử các phiên bản của đề cương, xem nội dung của phiên bản cũ và so sánh sự khác biệt giữa hai phiên bản bất kỳ.

3.  **Xây dựng UC-05c (Khôi phục phiên bản CTĐT)**
    *   **Nội dung:** Bổ sung chức năng cho phép người quản trị cấp cao có thể khôi phục toàn bộ thông tin của một CTĐT về một phiên bản cũ đã được lưu trước đó.
    *   **Checkpoint:** Trong trang quản lý phiên bản của CTĐT, admin có thể chọn một phiên bản từ danh sách và thực hiện hành động "Khôi phục", hệ thống sẽ sao lưu phiên bản hiện tại và thay thế bằng dữ liệu của phiên bản được chọn.

---

## Giai đoạn 2: Xây dựng các chức năng nâng cao và Module Quản trị Hệ thống

**Mục tiêu:** Xây dựng các công cụ quản trị mạnh mẽ và các tính năng tự động hóa để nâng cao trải nghiệm người dùng và hiệu quả quản lý.

1.  **Hoàn thiện UC-10 (Quản lý người dùng và phân quyền)**
    *   **Nội dung:** Xây dựng giao diện đồ họa cho phép quản trị viên quản lý người dùng, nhóm quyền (vai trò) và gán quyền chi tiết cho từng vai trò mà không cần truy cập trang admin mặc định của Django.
    *   **Checkpoint:** Admin có thể tạo/sửa/xóa vai trò (ví dụ: Giảng viên, Trưởng bộ môn, Admin Khoa), gán các quyền hạn cụ thể (ví dụ: "Được phép phê duyệt đề cương") cho từng vai trò, và gán người dùng vào các vai trò đó.

2.  **Xây dựng UC-09 (Báo cáo và thống kê động)**
    *   **Nội dung:** Phát triển một trang Dashboard tổng quan và các báo cáo động. Dashboard hiển thị các số liệu chính (số CTĐT, số đề cương chờ duyệt,...). Báo cáo động cho phép người dùng tùy chỉnh, lọc và xuất dữ liệu ra các định dạng như Excel, PDF.
    *   **Checkpoint:** Trang Dashboard hiển thị ít nhất 3 loại biểu đồ thống kê. Người dùng có quyền có thể vào mục "Báo cáo", chọn loại báo cáo, áp dụng bộ lọc (ví dụ: theo khoa, theo năm) và xuất kết quả.

3.  **Xây dựng UC-39 (Quản lý workflow và hệ thống nhắc việc)**
    *   **Nội dung:** Tích hợp một hệ thống luồng công việc (workflow) để tự động hóa các quy trình phê duyệt. Cấu hình hệ thống gửi email thông báo và nhắc việc tự động khi có một yêu cầu mới hoặc một yêu cầu sắp đến hạn.
    *   **Checkpoint:** Khi một giảng viên gửi yêu cầu phê duyệt đề cương, hệ thống tự động gửi email đến Trưởng bộ môn. Nếu sau 3 ngày Trưởng bộ môn chưa xử lý, hệ thống sẽ gửi email nhắc việc.

---

## Giai đoạn 3: Xây dựng Module Hỗ trợ Mở ngành Đào tạo

**Mục tiêu:** Phát triển từ đầu module Hỗ trợ Mở ngành, một trong những yêu cầu lớn và quan trọng của hệ thống.

1.  **Xây dựng UC-27, UC-06, UC-28, UC-32 (Quy trình mở ngành)**
    *   **Nội dung:** Phát triển các chức năng cốt lõi cho quy trình mở ngành, bao gồm: tạo tờ trình đề xuất, quản lý thông tin hội đồng, và theo dõi các bước thẩm định.
    *   **Checkpoint:** Người dùng có thể khởi tạo một "Hồ sơ mở ngành" mới, điền các thông tin cơ bản, và chuyển hồ sơ qua các trạng thái như "Đang soạn thảo", "Chờ thẩm định cấp Khoa", "Chờ thẩm định cấp Trường".

2.  **Hoàn thiện UC-07 (Quản lý minh chứng theo ngữ cảnh)**
    *   **Nội dung:** Mở rộng module quản lý tài liệu hiện tại để hỗ trợ quản lý minh chứng theo ngữ cảnh của hồ sơ mở ngành. Cho phép đính kèm, phân loại, và quản lý phiên bản các file minh chứng.
    *   **Checkpoint:** Trong một "Hồ sơ mở ngành", người dùng có thể tải lên các file minh chứng và gắn chúng vào các yêu cầu cụ thể (ví dụ: minh chứng về đội ngũ giảng viên, minh chứng về cơ sở vật chất).

3.  **Hoàn thiện UC-18 (Quản lý các điều kiện đảm bảo)**
    *   **Nội dung:** Xây dựng giao diện quản lý các điều kiện đảm bảo chất lượng khác ngoài giảng viên (ví dụ: cơ sở vật chất, phòng thí nghiệm). Tích hợp cơ chế kiểm tra và đối chiếu tự động các điều kiện này với yêu cầu của ngành đề xuất mở.
    *   **Checkpoint:** Hệ thống có thể đưa ra cảnh báo tự động nếu hồ sơ mở ngành không đáp ứng yêu cầu về số lượng giảng viên cơ hữu có trình độ Tiến sĩ hoặc thiếu các phòng thí nghiệm cần thiết.

---

## Giai đoạn 4: Hoàn thiện các chức năng còn lại và Tối ưu hóa

**Mục tiêu:** Hoàn thành nốt các chức năng nghiệp vụ phức tạp, thực hiện rà soát tổng thể và chuẩn bị cho việc triển khai.

1.  **Xây dựng UC-02b (Khảo sát CĐR)**
    *   **Nội dung:** Xây dựng module cho phép tạo các mẫu khảo sát (ví dụ: khảo sát nhà tuyển dụng, khảo sát cựu sinh viên) về CĐR. Hỗ trợ gửi email mời khảo sát hàng loạt và thu thập, tổng hợp kết quả dưới dạng biểu đồ và bảng số liệu.
    *   **Checkpoint:** Người quản lý CTĐT có thể tạo một cuộc khảo sát, chọn danh sách người nhận, gửi đi và sau đó xem báo cáo tổng hợp kết quả phản hồi.

2.  **Xây dựng UC-17 (Đánh giá CTĐT định kỳ)**
    *   **Nội dung:** Xây dựng module cho phép khởi tạo các đợt tự đánh giá CTĐT theo chu kỳ. Hỗ trợ thu thập minh chứng, điền các biểu mẫu tự đánh giá và xuất ra báo cáo hoàn chỉnh theo mẫu quy định.
    *   **Checkpoint:** Hệ thống có thể tạo ra một file Word/PDF báo cáo tự đánh giá CTĐT hoàn chỉnh, với các nội dung và minh chứng được tự động tổng hợp từ dữ liệu đã có trong hệ thống.

3.  **Rà soát, Tối ưu hóa và Sao lưu (UC-14)**
    *   **Nội dung:** Kiểm tra lại toàn bộ hệ thống, tối ưu hóa hiệu năng truy vấn cơ sở dữ liệu, sửa các lỗi còn tồn đọng. Xây dựng kịch bản (script) sao lưu dữ liệu tự động hàng ngày.
    *   **Checkpoint:** Hệ thống hoạt động ổn định, đáp ứng nhanh. Dữ liệu được tự động sao lưu vào một vị trí an toàn mỗi đêm.
