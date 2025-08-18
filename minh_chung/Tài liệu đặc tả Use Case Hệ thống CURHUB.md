# Tài liệu đặc tả Use Case Hệ thống CURHUB

## 1. Giới thiệu

Tài liệu này mô tả chi tiết các kịch bản sử dụng (Use Case Scenarios) cho Hệ thống Quản lý Chương trình Đào tạo và Hỗ trợ Mở mã ngành đào tạo (CURHUB), dựa trên tài liệu "Phân tích yêu cầu hệ thống" và "Đặc tả phần mềm hệ thống PTCT".

## 2. Các kịch bản Use Case

### 2.1. Module Quản lý CTĐT

#### UC-01: Quản lý thông tin chung của CTĐT (tạo mới, cập nhật)

**UC-01a: Tạo mới CTĐT**

*   **Mục đích:** Tạo mới một chương trình đào tạo trong hệ thống.
*   **Actor chính:** Đơn vị chuyên môn (ĐVCM).
*   **Điều kiện tiên quyết:**
    *   Người dùng đã đăng nhập với quyền ĐVCM.
    *   Đã có nghị quyết phê duyệt chủ trương.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn chức năng "Tạo mới CTĐT".
    2.  Hệ thống hiển thị form nhập thông tin với các trường:
        *   Mã ngành (bắt buộc)
        *   Tên ngành (bắt buộc)
        *   Trình độ đào tạo (bắt buộc)
        *   Hình thức đào tạo
        *   Thời gian đào tạo
        *   Đơn vị quản lý
        *   Mô tả chung
    3.  Người dùng nhập thông tin.
    4.  Hệ thống kiểm tra:
        *   Tính đầy đủ của thông tin bắt buộc.
        *   Tính hợp lệ của dữ liệu.
        *   Tính duy nhất của mã CTĐT.
    5.  Hệ thống lưu thông tin và tạo mã CTĐT.
    6.  Hệ thống thông báo tạo mới thành công.
*   **Luồng xử lý thay thế:**
    *   **4a. Thông tin không hợp lệ:**
        1.  Hệ thống hiển thị thông báo lỗi.
        2.  Quay lại bước 3.
    *   **4b. Mã CTĐT đã tồn tại:**
        1.  Hệ thống cảnh báo trùng mã.
        2.  Yêu cầu nhập mã khác.
*   **Điều kiện sau:**
    *   CTĐT được tạo trong hệ thống.
    *   Tự động tạo các thành phần mặc định.
    *   Gửi thông báo cho các bên liên quan.

**UC-01b: Cập nhật CTĐT**

*   **Mục đích:** Cập nhật thông tin của một chương trình đào tạo đã tồn tại.
*   **Actor chính:** Đơn vị chuyên môn (ĐVCM).
*   **Điều kiện tiên quyết:**
    *   Người dùng đã đăng nhập với quyền ĐVCM.
    *   CTĐT cần cập nhật đã tồn tại trong hệ thống.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn CTĐT cần cập nhật từ danh sách.
    2.  Hệ thống hiển thị form với thông tin hiện tại của CTĐT.
    3.  Người dùng chỉnh sửa các thông tin cần thiết.
    4.  Hệ thống kiểm tra tính hợp lệ của dữ liệu.
    5.  Hệ thống lưu thông tin đã cập nhật.
    6.  Hệ thống tạo một phiên bản mới của CTĐT (nếu có thay đổi đáng kể).
    7.  Hệ thống thông báo cập nhật thành công và ghi nhận lịch sử thay đổi.
*   **Luồng xử lý thay thế:**
    *   **4a. Thông tin không hợp lệ:**
        1.  Hệ thống hiển thị thông báo lỗi.
        2.  Người dùng quay lại chỉnh sửa.
*   **Điều kiện sau:**
    *   CTĐT được cập nhật trong hệ thống.
    *   Lịch sử thay đổi được ghi nhận.
    *   Phiên bản mới của CTĐT được tạo (nếu áp dụng).

#### UC-02: Quản lý chuẩn đầu ra (CĐR) của CTĐT

**UC-02a: Xây dựng CĐR**

*   **Mục đích:** Xây dựng và quản lý Chuẩn đầu ra (CĐR) của Chương trình đào tạo.
*   **Actor chính:** Đơn vị chuyên môn (ĐVCM), Hội đồng xây dựng.
*   **Điều kiện tiên quyết:** Chương trình đào tạo (CTĐT) đã được tạo.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn CTĐT cần quản lý CĐR.
    2.  Hệ thống hiển thị giao diện quản lý CĐR.
    3.  Người dùng thêm CĐR với các thông tin:
        *   Mã CĐR
        *   Phân loại
        *   Nội dung
        *   Nhóm CĐR (Kiến thức/Kỹ năng/Thái độ)
        *   Trình độ năng lực
        *   Chỉ báo đánh giá
    4.  Hệ thống kiểm tra tính hợp lệ của dữ liệu và lưu thông tin.
    5.  Hệ thống tự động cập nhật ma trận CĐR.
*   **Luồng xử lý thay thế:**
    *   **4a. Thông tin không hợp lệ:**
        1.  Hệ thống hiển thị thông báo lỗi.
        2.  Người dùng quay lại chỉnh sửa.
*   **Điều kiện sau:**
    *   CĐR được thêm vào CTĐT.
    *   Ma trận CĐR được cập nhật.

**UC-02b: Khảo sát CĐR**

*   **Mục đích:** Thu thập ý kiến về CĐR từ các bên liên quan.
*   **Actor chính:** TT.HL-DH, ĐVCM.
*   **Điều kiện tiên quyết:** CĐR đã được xây dựng.
*   **Luồng xử lý chính:**
    1.  Người dùng tạo mẫu khảo sát:
        *   Chọn đối tượng khảo sát (sinh viên, giảng viên, doanh nghiệp...).
        *   Thiết kế câu hỏi liên quan đến CĐR.
        *   Cấu hình thời gian khảo sát.
    2.  Hệ thống tạo link khảo sát và gửi thông báo (email) đến đối tượng khảo sát.
    3.  Hệ thống thu thập kết quả khảo sát và lưu trữ phản hồi.
    4.  Hệ thống thống kê và phân tích dữ liệu, tổng hợp ý kiến và tạo báo cáo phân tích.
*   **Luồng xử lý thay thế:**
    *   **2a. Lỗi gửi khảo sát:**
        1.  Hệ thống ghi nhận lỗi.
        2.  Hệ thống thử gửi lại tự động.
    *   **3a. Tỷ lệ phản hồi thấp:**
        1.  Hệ thống gửi nhắc nhở đến đối tượng khảo sát.
        2.  Người dùng có thể gia hạn thời gian khảo sát.
*   **Điều kiện sau:**
    *   Kết quả khảo sát được lưu trữ.
    *   Báo cáo phân tích CĐR được tạo.

**UC-02c: Phê duyệt CĐR**

*   **Mục đích:** Phê duyệt Chuẩn đầu ra của CTĐT.
*   **Actor chính:** Hội đồng Khoa học và Đào tạo (HĐKH&ĐT), Ban Giám hiệu.
*   **Điều kiện tiên quyết:** CĐR đã được xây dựng và khảo sát (nếu có).
*   **Luồng xử lý chính:**
    1.  ĐVCM trình duyệt CĐR lên các cấp có thẩm quyền (HĐKH&ĐT, Ban Giám hiệu).
    2.  Các cấp phê duyệt xem xét CĐR, ghi nhận góp ý (nếu có).
    3.  ĐVCM cập nhật chỉnh sửa CĐR dựa trên góp ý.
    4.  Sau khi đạt được sự đồng thuận, CĐR được ban hành (kèm theo Quyết định phê duyệt).
*   **Luồng xử lý thay thế:**
    *   **2a. Yêu cầu chỉnh sửa:**
        1.  Cấp phê duyệt yêu cầu chỉnh sửa.
        2.  ĐVCM thực hiện chỉnh sửa và trình duyệt lại.
*   **Điều kiện sau:**
    *   CĐR được phê duyệt và ban hành chính thức.
    *   Hồ sơ phê duyệt được lưu trữ.

#### UC-03: Quản lý danh mục học phần

**UC-03a: Thêm học phần mới**

*   **Mục đích:** Thêm một học phần mới vào danh mục học phần chung của hệ thống.
*   **Actor chính:** Đơn vị chuyên môn (ĐVCM), TT.HL-DH.
*   **Điều kiện tiên quyết:** Người dùng có quyền thêm học phần.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn chức năng "Thêm học phần mới".
    2.  Hệ thống hiển thị form nhập thông tin học phần với các trường:
        *   Mã học phần (duy nhất)
        *   Tên học phần (Tiếng Việt, Tiếng Anh)
        *   Số tín chỉ (lý thuyết, thực hành, tự học)
        *   Loại học phần (bắt buộc, tự chọn)
        *   Điều kiện tiên quyết (nếu có)
        *   Mô tả học phần
    3.  Người dùng nhập thông tin.
    4.  Hệ thống kiểm tra:
        *   Tính hợp lệ của dữ liệu.
        *   Mã học phần không trùng lặp.
    5.  Hệ thống lưu thông tin học phần vào danh mục chung.
    6.  Hệ thống tự động cập nhật tổng số tín chỉ của CTĐT (nếu học phần này được thêm vào một CTĐT cụ thể) và cấu trúc chương trình.
*   **Luồng xử lý thay thế:**
    *   **4a. Thông tin không hợp lệ hoặc trùng mã:**
        1.  Hệ thống hiển thị thông báo lỗi/cảnh báo.
        2.  Người dùng quay lại chỉnh sửa.
*   **Điều kiện sau:**
    *   Học phần mới được thêm vào danh mục.
    *   Thông tin liên quan trong CTĐT được cập nhật (nếu có).

#### UC-04: Quản lý đề cương chi tiết học phần

**UC-04a: Tạo đề cương**

*   **Mục đích:** Tạo mới đề cương chi tiết cho một học phần.
*   **Actor chính:** Giảng viên phụ trách, ĐVCM.
*   **Điều kiện tiên quyết:** Học phần đã tồn tại trong hệ thống.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn học phần cần tạo đề cương.
    2.  Hệ thống hiển thị form tạo đề cương với các mục:
        *   Thông tin chung học phần
        *   Mục tiêu học phần
        *   Chuẩn đầu ra học phần (CĐRHP)
        *   Nội dung chi tiết (chương, mục, thời lượng)
        *   Phương pháp giảng dạy
        *   Phương pháp đánh giá
        *   Tài liệu học tập
        *   Nhiệm vụ sinh viên
    3.  Người dùng nhập/chọn thông tin cho từng mục.
    4.  Hệ thống kiểm tra tính đầy đủ và hợp lệ của dữ liệu.
    5.  Hệ thống lưu đề cương dưới dạng bản nháp (draft).
*   **Luồng xử lý thay thế:**
    *   **4a. Thiếu thông tin bắt buộc/không hợp lệ:**
        1.  Hệ thống hiển thị thông báo lỗi.
        2.  Người dùng quay lại chỉnh sửa.
*   **Điều kiện sau:**
    *   Đề cương học phần được tạo và lưu trữ.
    *   Trạng thái đề cương là "Nháp".

**UC-04b: Cập nhật nội dung đề cương**

*   **Mục đích:** Chỉnh sửa nội dung của đề cương học phần.
*   **Actor chính:** Giảng viên phụ trách, ĐVCM.
*   **Điều kiện tiên quyết:** Đề cương học phần đã tồn tại và người dùng có quyền chỉnh sửa.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn đề cương cần cập nhật.
    2.  Hệ thống hiển thị nội dung đề cương hiện tại.
    3.  Người dùng chỉnh sửa các mục cần thiết.
    4.  Hệ thống kiểm tra tính hợp lệ của dữ liệu.
    5.  Hệ thống lưu các thay đổi.
    6.  Hệ thống tự động tạo phiên bản mới hoặc cập nhật phiên bản hiện tại (tùy theo quy định).
*   **Luồng xử lý thay thế:**
    *   **4a. Dữ liệu không hợp lệ:**
        1.  Hệ thống hiển thị thông báo lỗi.
        2.  Người dùng quay lại chỉnh sửa.
*   **Điều kiện sau:**
    *   Đề cương học phần được cập nhật.
    *   Lịch sử thay đổi được ghi nhận.

**UC-04c: Phê duyệt đề cương**

*   **Mục đích:** Phê duyệt đề cương học phần để đưa vào sử dụng chính thức.
*   **Actor chính:** Trưởng đơn vị chuyên môn (Trưởng Khoa/Bộ môn).
*   **Điều kiện tiên quyết:** Đề cương học phần đã hoàn thiện và được trình duyệt.
*   **Luồng xử lý chính:**
    1.  Giảng viên/ĐVCM trình duyệt đề cương lên Trưởng đơn vị.
    2.  Trưởng đơn vị xem xét nội dung đề cương.
    3.  Trưởng đơn vị có thể:
        *   **Phê duyệt:** Đề cương được chấp thuận.
        *   **Yêu cầu chỉnh sửa:** Ghi nhận góp ý và gửi lại cho người tạo.
        *   **Từ chối:** Đề cương không được chấp thuận.
    4.  Hệ thống cập nhật trạng thái của đề cương (Đã phê duyệt/Yêu cầu chỉnh sửa/Từ chối).
    5.  Hệ thống gửi thông báo kết quả phê duyệt cho các bên liên quan.
*   **Luồng xử lý thay thế:**
    *   **3a. Yêu cầu chỉnh sửa:**
        1.  Người tạo đề cương nhận được thông báo và góp ý.
        2.  Người tạo chỉnh sửa và trình duyệt lại.
*   **Điều kiện sau:**
    *   Đề cương học phần có trạng thái "Đã phê duyệt" hoặc "Yêu cầu chỉnh sửa" hoặc "Từ chối".
    *   Lịch sử phê duyệt được ghi nhận.

**UC-04d: Quản lý phiên bản đề cương**

*   **Mục đích:** Theo dõi và quản lý các phiên bản của đề cương học phần.
*   **Actor chính:** TT.HL-DH, ĐVCM.
*   **Điều kiện tiên quyết:** Đề cương học phần đã có nhiều phiên bản.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn đề cương học phần.
    2.  Hệ thống hiển thị danh sách các phiên bản của đề cương, bao gồm:
        *   Mã phiên bản
        *   Ngày tạo/cập nhật
        *   Người thực hiện
        *   Mô tả thay đổi
    3.  Người dùng có thể:
        *   **Xem chi tiết từng phiên bản:** Hiển thị nội dung của phiên bản đó.
        *   **So sánh hai phiên bản:** Hiển thị sự khác biệt giữa hai phiên bản được chọn.
        *   **Khôi phục phiên bản:** Đặt một phiên bản cũ làm phiên bản hiện tại (cần quyền).
*   **Điều kiện sau:**
    *   Lịch sử phiên bản được duy trì.
    *   Khả năng truy xuất và so sánh các phiên bản.

#### UC-05: Quản lý phiên bản của CTĐT, cho phép so sánh và khôi phục

**UC-05a: Tạo phiên bản mới**

*   **Mục đích:** Tạo một phiên bản mới của Chương trình đào tạo để ghi nhận các thay đổi.
*   **Actor chính:** Đơn vị chuyên môn (ĐVCM), Trung tâm Học liệu - Phát triển Dạy và Học (TT.HL-DH).
*   **Điều kiện tiên quyết:** CTĐT đã tồn tại trong hệ thống và có sự thay đổi cần ghi nhận.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn CTĐT cần tạo phiên bản.
    2.  Hệ thống hiển thị form với các thông tin:
        *   Phiên bản hiện tại
        *   Lý do thay đổi (bắt buộc)
        *   Mô tả chi tiết thay đổi
        *   File đính kèm (nếu có)
    3.  Người dùng nhập thông tin lý do và mô tả thay đổi.
    4.  Hệ thống:
        *   Tạo mã phiên bản mới (theo quy tắc major.minor.patch).
        *   Sao chép dữ liệu từ phiên bản cũ.
        *   Lưu thông tin thay đổi và người thực hiện.
    5.  Hệ thống thông báo tạo phiên bản thành công.
*   **Luồng xử lý thay thế:**
    *   **3a. Thiếu thông tin bắt buộc:**
        1.  Hệ thống hiển thị thông báo lỗi.
        2.  Người dùng quay lại nhập thông tin.
*   **Điều kiện sau:**
    *   Phiên bản mới của CTĐT được tạo và lưu trữ.
    *   Lịch sử thay đổi được ghi nhận.

**UC-05b: So sánh phiên bản**

*   **Mục đích:** So sánh sự khác biệt giữa hai phiên bản bất kỳ của CTĐT.
*   **Actor chính:** ĐVCM, TT.HL-DH, Ban Giám hiệu, Hội đồng.
*   **Điều kiện tiên quyết:** CTĐT có ít nhất hai phiên bản.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn CTĐT và hai phiên bản cần so sánh từ danh sách.
    2.  Hệ thống thực hiện so sánh và hiển thị kết quả:
        *   Thông tin cơ bản của hai phiên bản.
        *   Các thay đổi về cấu trúc chương trình.
        *   Thay đổi về danh mục học phần.
        *   Thay đổi về Chuẩn đầu ra (CĐR).
        *   Các thay đổi khác (mô tả chung, thời gian đào tạo...).
    3.  Người dùng có thể:
        *   Xem chi tiết từng thay đổi.
        *   Xuất báo cáo so sánh (PDF, Excel).
        *   Đánh dấu các thay đổi quan trọng.
*   **Điều kiện sau:**
    *   Báo cáo so sánh được hiển thị và có thể xuất ra.

**UC-05c: Khôi phục phiên bản**

*   **Mục đích:** Khôi phục CTĐT về một phiên bản trước đó.
*   **Actor chính:** TT.HL-DH (có quyền quản trị cao nhất).
*   **Điều kiện tiên quyết:** CTĐT có các phiên bản đã lưu trữ và người dùng có quyền khôi phục.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn CTĐT và phiên bản cần khôi phục.
    2.  Hệ thống hiển thị cảnh báo về thông tin phiên bản và các ảnh hưởng khi khôi phục, yêu cầu xác nhận.
    3.  Người dùng xác nhận muốn khôi phục.
    4.  Hệ thống:
        *   Tạo một phiên bản mới (để ghi nhận việc khôi phục).
        *   Sao chép dữ liệu từ phiên bản được chọn làm phiên bản hiện tại.
        *   Cập nhật trạng thái của CTĐT.
    5.  Hệ thống thông báo kết quả khôi phục thành công.
*   **Luồng xử lý thay thế:**
    *   **3a. Người dùng không xác nhận:**
        1.  Hệ thống hủy thao tác khôi phục.
*   **Điều kiện sau:**
    *   CTĐT được khôi phục về trạng thái của phiên bản đã chọn.
    *   Lịch sử khôi phục được ghi nhận.

#### UC-15: Đối sánh CTĐT với các chương trình khác

*   **Mục đích:** Thực hiện đối sánh Chương trình đào tạo (CTĐT) với các chương trình khác trong và ngoài nước để đánh giá và cải tiến.
*   **Actor chính:** Đơn vị chuyên môn (ĐVCM), Trung tâm Học liệu - Phát triển Dạy và Học (TT.HL-DH).
*   **Điều kiện tiên quyết:**
    *   CTĐT cần đối sánh đã được tạo trong hệ thống.
    *   Có dữ liệu CTĐT tham chiếu (từ các trường khác, chuẩn quốc tế...).
    *   Người dùng có quyền thực hiện đối sánh.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn chức năng "Đối sánh CTĐT".
    2.  Hệ thống hiển thị form cho phép người dùng:
        *   Chọn CTĐT cần đối sánh.
        *   Chọn danh sách CTĐT tham chiếu (có thể là nhiều CTĐT).
        *   Chọn các tiêu chí đối sánh (Cấu trúc chương trình, Nội dung chi tiết, Chuẩn đầu ra, Phương pháp giảng dạy, v.v.).
    3.  Người dùng chọn CTĐT, CTĐT tham chiếu và các tiêu chí đối sánh.
    4.  Hệ thống thực hiện quá trình đối sánh dựa trên các tiêu chí đã chọn và hiển thị kết quả:
        *   Bảng so sánh chi tiết các tiêu chí.
        *   Biểu đồ trực quan hóa sự khác biệt/tương đồng.
        *   Phân tích điểm mạnh/điểm yếu của CTĐT đang xét so với các CTĐT tham chiếu.
        *   Đề xuất các điểm có thể cải tiến.
    5.  Người dùng xem xét kết quả đối sánh và có thể xác nhận hoặc yêu cầu phân tích thêm.
*   **Luồng xử lý thay thế:**
    *   **4a. Thiếu dữ liệu đối sánh:**
        1.  Hệ thống thông báo thiếu dữ liệu tham chiếu.
        2.  Yêu cầu người dùng bổ sung thông tin hoặc chọn CTĐT tham chiếu khác.
    *   **4b. Kết quả không hợp lệ/không rõ ràng:**
        1.  Hệ thống cảnh báo về chất lượng kết quả.
        2.  Đề xuất người dùng điều chỉnh tiêu chí đối sánh hoặc cung cấp dữ liệu chi tiết hơn.
*   **Điều kiện sau:**
    *   Báo cáo đối sánh được tạo và lưu trữ trong hệ thống.
    *   Lịch sử đối sánh của CTĐT được cập nhật.
    *   Gửi thông báo kết quả đối sánh cho các bên liên quan (nếu cần).

#### UC-17: Đánh giá CTĐT định kỳ

*   **Mục đích:** Thực hiện đánh giá định kỳ hoặc đột xuất chất lượng Chương trình đào tạo (CTĐT).
*   **Actor chính:** Đơn vị chuyên môn (ĐVCM), Hội đồng Khoa học & Đào tạo (HĐKH&ĐT).
*   **Điều kiện tiên quyết:**
    *   CTĐT đã vận hành ít nhất một chu kỳ đào tạo.
    *   Có đầy đủ dữ liệu đánh giá (kết quả học tập, phản hồi sinh viên, giảng viên, nhà tuyển dụng...).
    *   Có quyết định/kế hoạch đánh giá từ cấp quản lý.
*   **Luồng xử lý chính:**
    1.  Người dùng (ĐVCM hoặc TT.HL-DH) tạo một đợt đánh giá mới:
        *   Chọn CTĐT cần đánh giá.
        *   Thiết lập các tiêu chí đánh giá (dựa trên chuẩn đầu ra, mục tiêu đào tạo, chuẩn kiểm định...).
        *   Phân công người đánh giá hoặc tổ đánh giá.
    2.  Hệ thống hỗ trợ thu thập dữ liệu liên quan đến CTĐT, bao gồm:
        *   Kết quả học tập của sinh viên.
        *   Phản hồi từ giảng viên về chất lượng giảng dạy và nội dung học phần.
        *   Ý kiến của người học về chương trình.
        *   Báo cáo việc làm của sinh viên tốt nghiệp.
        *   Các minh chứng khác (biên bản họp, báo cáo NCKH...).
    3.  Người đánh giá thực hiện đánh giá theo các tiêu chí đã thiết lập, nhập nhận xét, đính kèm minh chứng và đề xuất các điểm cần cải tiến.
    4.  Hệ thống tổng hợp kết quả đánh giá, tạo báo cáo tự đánh giá, xác định các điểm mạnh/điểm yếu và đề xuất kế hoạch cải tiến.
*   **Luồng xử lý thay thế:**
    *   **2a. Thiếu minh chứng/dữ liệu:**
        1.  Hệ thống thông báo các minh chứng/dữ liệu còn thiếu.
        2.  Yêu cầu bổ sung thông tin hoặc tạm hoãn đánh giá cho đến khi đủ dữ liệu.
    *   **3a. Kết quả đánh giá không đạt yêu cầu:**
        1.  Hệ thống cảnh báo về kết quả không đạt.
        2.  Yêu cầu rà soát lại quá trình đánh giá hoặc đề xuất các biện pháp khắc phục.
*   **Điều kiện sau:**
    *   Báo cáo đánh giá CTĐT được tạo và phê duyệt.
    *   Kế hoạch cải tiến CTĐT được xây dựng dựa trên kết quả đánh giá.
    *   Trạng thái của CTĐT được cập nhật (ví dụ: "Đã đánh giá", "Cần cải tiến").

### 2.2. Module Hỗ trợ Mở ngành Đào tạo

#### UC-27: Quản lý tờ trình đề xuất chủ trương mở ngành

*   **Mục đích:** Quản lý việc lập và trình duyệt tờ trình đề xuất mở ngành/chuyên ngành mới.
*   **Actor chính:** Đơn vị chuyên môn (ĐVCM).
*   **Điều kiện tiên quyết:**
    *   Người dùng có quyền ĐVCM.
    *   Có báo cáo khảo sát nhu cầu xã hội sơ bộ.
    *   Có đánh giá năng lực cơ sở đào tạo ban đầu.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn chức năng "Tạo tờ trình đề xuất chủ trương mở ngành".
    2.  Hệ thống hiển thị form tạo tờ trình với các thông tin cơ bản:
        *   Tên ngành đề xuất, Mã ngành (dự kiến).
        *   Trình độ đào tạo (Đại học, Thạc sĩ, Tiến sĩ).
        *   Đơn vị quản lý (Khoa/Bộ môn đề xuất).
    3.  Người dùng nhập nội dung chính của tờ trình, bao gồm:
        *   Sự cần thiết mở ngành.
        *   Năng lực cơ sở đào tạo hiện có.
        *   Mục tiêu phát triển của ngành.
        *   Giải pháp và lộ trình triển khai.
        *   Phương án phòng ngừa rủi ro.
    4.  Người dùng đính kèm các minh chứng liên quan (báo cáo khảo sát, đánh giá năng lực, kế hoạch triển khai sơ bộ, các văn bản pháp lý liên quan).
    5.  Người dùng trình duyệt tờ trình lên lãnh đạo đơn vị và sau đó gửi đến Hội đồng Khoa học & Đào tạo (HĐKH&ĐT).
    6.  Hệ thống theo dõi trạng thái của tờ trình (Đã trình, Đang xem xét, Yêu cầu chỉnh sửa, Đã phê duyệt, Từ chối).
*   **Luồng xử lý thay thế:**
    *   **4a. Thiếu minh chứng:**
        1.  Hệ thống thông báo các minh chứng còn thiếu.
        2.  Tạm dừng quá trình trình duyệt cho đến khi bổ sung đầy đủ.
    *   **5a. Yêu cầu chỉnh sửa từ cấp duyệt:**
        1.  Người dùng tiếp nhận góp ý từ lãnh đạo đơn vị hoặc HĐKH&ĐT.
        2.  Người dùng chỉnh sửa nội dung tờ trình và các minh chứng kèm theo.
        3.  Người dùng trình duyệt lại tờ trình.
*   **Điều kiện sau:**
    *   Tờ trình đề xuất chủ trương được tạo và lưu trữ trong hệ thống.
    *   Trạng thái của tờ trình được cập nhật theo quy trình phê duyệt.

#### UC-06: Quản lý việc thành lập và hoạt động của các Hội đồng

**UC-06a: Thành lập Hội đồng**

*   **Mục đích:** Quản lý quá trình đề xuất, kiểm tra điều kiện và phê duyệt thành lập các loại Hội đồng (Hội đồng xây dựng CTĐT, Hội đồng thẩm định, v.v.).
*   **Actor chính:** Trung tâm Học liệu - Phát triển Dạy và Học (TT.HL-DH), Đơn vị chuyên môn (ĐVCM), Ban Giám hiệu (BGH).
*   **Điều kiện tiên quyết:** Có nhu cầu thành lập Hội đồng (ví dụ: để xây dựng CTĐT mới, thẩm định đề án mở ngành).
*   **Luồng xử lý chính:**
    1.  ĐVCM hoặc TT.HL-DH tạo đề xuất thành lập Hội đồng, nhập các thông tin:
        *   Loại Hội đồng (xây dựng CTĐT, thẩm định, v.v.).
        *   Mục đích thành lập.
        *   Thời gian dự kiến hoạt động.
        *   Danh sách đề xuất thành viên (Họ tên, chức danh, đơn vị, học hàm, học vị).
    2.  Hệ thống kiểm tra điều kiện thành lập Hội đồng dựa trên quy định:
        *   Đủ số lượng thành viên tối thiểu/tối đa.
        *   Đáp ứng tiêu chuẩn về học hàm, học vị, kinh nghiệm của từng vị trí (Chủ tịch, Thư ký, Phản biện...).
        *   Đảm bảo tính độc lập của thành viên (đối với Hội đồng thẩm định).
    3.  Đề xuất được trình lên Ban Giám hiệu (BGH) để xem xét và phê duyệt.
    4.  Sau khi BGH phê duyệt, hệ thống tự động tạo Quyết định thành lập Hội đồng.
    5.  Hệ thống gửi thông báo cho các thành viên được chỉ định trong Hội đồng.
*   **Luồng xử lý thay thế:**
    *   **2a. Không đủ điều kiện thành lập:**
        1.  Hệ thống hiển thị thông báo lỗi chi tiết về các điều kiện không đạt.
        2.  Người đề xuất phải chỉnh sửa danh sách thành viên hoặc thông tin khác để đáp ứng quy định.
*   **Điều kiện sau:**
    *   Hội đồng được thành lập chính thức trong hệ thống.
    *   Quyết định thành lập được tạo và lưu trữ.
    *   Các thành viên Hội đồng nhận được thông báo và có quyền truy cập liên quan.

**UC-06b: Tổ chức họp Hội đồng**

*   **Mục đích:** Quản lý việc lập kế hoạch, thông báo, ghi nhận biên bản và kết luận các cuộc họp của Hội đồng.
*   **Actor chính:** Thư ký Hội đồng, TT.HL-DH.
*   **Điều kiện tiên quyết:** Hội đồng đã được thành lập.
*   **Luồng xử lý chính:**
    1.  Thư ký Hội đồng lập kế hoạch họp, bao gồm:
        *   Thời gian, địa điểm họp.
        *   Chương trình họp (nội dung thảo luận, trình bày).
        *   Danh sách tài liệu cần chuẩn bị và chia sẻ trước cuộc họp.
    2.  Hệ thống gửi thông báo mời họp (qua email, notification) đến các thành viên Hội đồng và các bên liên quan.
    3.  Trong cuộc họp, Thư ký Hội đồng ghi nhận biên bản:
        *   Điểm danh thành viên tham dự.
        *   Ghi nhận đầy đủ các ý kiến thảo luận, góp ý.
        *   Upload các tài liệu liên quan được trình bày trong cuộc họp.
    4.  Thư ký Hội đồng tổng hợp ý kiến và ghi nhận kết luận của Chủ tịch Hội đồng, bao gồm các yêu cầu chỉnh sửa (nếu có).
*   **Luồng xử lý thay thế:**
    *   **2a. Lỗi gửi thông báo:**
        1.  Hệ thống ghi nhận lỗi và thử gửi lại.
    *   **3a. Không đủ thành viên tham dự:**
        1.  Hệ thống cảnh báo không đủ số lượng thành viên theo quy định.
        2.  Cuộc họp có thể bị hoãn hoặc cần tổ chức lại.
*   **Điều kiện sau:**
    *   Biên bản cuộc họp được tạo và lưu trữ trong hệ thống.
    *   Các yêu cầu chỉnh sửa được ghi nhận và theo dõi.

**UC-06c: Thẩm định CTĐT/Đề án**

*   **Mục đích:** Quản lý quá trình thẩm định nội dung Chương trình đào tạo hoặc Đề án mở ngành bởi Hội đồng.
*   **Actor chính:** Thành viên Hội đồng, Chủ tịch Hội đồng, TT.HL-DH.
*   **Điều kiện tiên quyết:** CTĐT/Đề án đã hoàn thiện và sẵn sàng thẩm định.
*   **Luồng xử lý chính:**
    1.  Chủ tịch Hội đồng phân công các thành viên làm phản biện chính và gửi tài liệu thẩm định cho họ.
    2.  Các thành viên Hội đồng (đặc biệt là phản biện) thu thập nhận xét, đánh giá và upload báo cáo phản biện lên hệ thống.
    3.  Hệ thống tổng hợp các ý kiến góp ý từ các thành viên.
    4.  Hội đồng tổ chức bỏ phiếu (có thể là bỏ phiếu kín) để đánh giá và thông qua CTĐT/Đề án.
    5.  Hệ thống thống kê kết quả bỏ phiếu.
    6.  Hội đồng lập biên bản kết luận thẩm định, ghi rõ các yêu cầu chỉnh sửa (nếu có) và quyết định thông qua.
*   **Luồng xử lý thay thế:**
    *   **2a. Phản biện chậm nộp báo cáo:**
        1.  Hệ thống gửi nhắc nhở tự động.
        2.  Thư ký Hội đồng liên hệ trực tiếp để đôn đốc.
    *   **6a. Không thông qua:**
        1.  Hệ thống ghi nhận lý do không thông qua.
        2.  ĐVCM phải chỉnh sửa CTĐT/Đề án và trình thẩm định lại.
*   **Điều kiện sau:**
    *   Biên bản kết luận thẩm định được tạo và lưu trữ.
    *   CTĐT/Đề án được cập nhật trạng thái thẩm định.

#### UC-28, UC-32: Quản lý quy trình thẩm định các cấp

**UC-28: Quản lý Thẩm định chủ trương**

*   **Mục đích:** Quản lý quá trình thẩm định tờ trình đề xuất chủ trương mở ngành bởi Hội đồng Khoa học & Đào tạo (HĐKH&ĐT).
*   **Actor chính:** HĐKH&ĐT, Thư ký HĐ.
*   **Điều kiện tiên quyết:** Tờ trình đề xuất chủ trương đã được lập đầy đủ và gửi đến HĐKH&ĐT. Hội đồng đã được thành lập.
*   **Luồng xử lý chính:**
    1.  Thư ký HĐKH&ĐT lập kế hoạch họp thẩm định chủ trương, phân công thành viên xem xét tài liệu và chuẩn bị biểu mẫu đánh giá.
    2.  HĐKH&ĐT tổ chức họp thẩm định:
        *   Xem xét hồ sơ tờ trình và các minh chứng kèm theo.
        *   Thảo luận tập thể về tính cần thiết, khả thi và phù hợp của đề xuất.
        *   Thực hiện bỏ phiếu kín để đưa ra quyết định.
        *   Ghi nhận đầy đủ kết quả bỏ phiếu và các ý kiến góp ý.
    3.  Thư ký HĐKH&ĐT tổng hợp ý kiến và lập biên bản kết luận thẩm định chủ trương.
    4.  Hệ thống thông báo kết quả thẩm định cho ĐVCM và các bên liên quan, đồng thời lưu trữ hồ sơ thẩm định.
*   **Luồng xử lý thay thế:**
    *   **2a. Không đủ thành viên tham dự họp:**
        1.  Cuộc họp bị hoãn.
        2.  Thư ký HĐ lập kế hoạch họp mới.
    *   **3a. Đề xuất không thông qua thẩm định:**
        1.  Hệ thống nêu rõ lý do không thông qua.
        2.  ĐVCM cần điều chỉnh đề xuất và trình thẩm định lại.
*   **Điều kiện sau:**
    *   Biên bản thẩm định chủ trương được tạo và lưu trữ.
    *   Trạng thái của tờ trình đề xuất chủ trương được cập nhật.

**UC-32: Quản lý Thẩm định cuối cùng**

*   **Mục đích:** Quản lý quá trình thẩm định cuối cùng hồ sơ mở ngành (bao gồm Đề án mở ngành và CTĐT) bởi Hội đồng Khoa học & Đào tạo (HĐKH&ĐT) hoặc Hội đồng Thẩm định chuyên biệt.
*   **Actor chính:** HĐKH&ĐT, TT.HL-DH.
*   **Điều kiện tiên quyết:** Đề án mở ngành và CTĐT đã hoàn chỉnh, hồ sơ minh chứng đầy đủ.
*   **Luồng xử lý chính:**
    1.  TT.HL-DH hoặc ĐVCM chuẩn bị hồ sơ thẩm định cuối cùng:
        *   Kiểm tra tính đầy đủ và rà soát nội dung của Đề án, CTĐT và các minh chứng.
        *   Sắp xếp hồ sơ theo logic quy định.
        *   Lập kế hoạch thẩm định (thời gian, phân công nhiệm vụ, chuẩn bị biểu mẫu).
    2.  Hội đồng tổ chức họp thẩm định cuối cùng:
        *   ĐVCM/Ban biên soạn trình bày tóm tắt về Đề án và CTĐT.
        *   Hội đồng thảo luận, đặt câu hỏi và đưa ra ý kiến góp ý.
        *   Thực hiện bỏ phiếu đánh giá.
        *   Ghi nhận biên bản cuộc họp, phiếu đánh giá và các ý kiến góp ý chi tiết.
    3.  Hội đồng tổng hợp đánh giá, lập báo cáo thẩm định cuối cùng.
    4.  Hệ thống thông báo kết quả thẩm định cho các bên liên quan và lưu trữ toàn bộ hồ sơ thẩm định.
*   **Luồng xử lý thay thế:**
    *   **2a. Hồ sơ chưa đạt yêu cầu sau thẩm định:**
        1.  Hệ thống ghi nhận các yêu cầu chỉnh sửa cụ thể.
        2.  ĐVCM/Ban biên soạn bổ sung, chỉnh sửa và lập kế hoạch thẩm định lại.
*   **Điều kiện sau:**
    *   Báo cáo thẩm định cuối cùng được tạo và lưu trữ.
    *   Hồ sơ mở ngành được cập nhật trạng thái "Đã thẩm định".

#### UC-07: Quản lý minh chứng và tài liệu liên quan

**UC-07a: Quản lý Minh chứng**

*   **Mục đích:** Quản lý việc thu thập, upload, phân loại và kiểm soát phiên bản các minh chứng liên quan đến CTĐT và mở ngành.
*   **Actor chính:** Đơn vị chuyên môn (ĐVCM), Trung tâm Học liệu - Phát triển Dạy và Học (TT.HL-DH).
*   **Điều kiện tiên quyết:** Người dùng có quyền truy cập vào hệ thống quản lý tài liệu.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn chức năng "Upload minh chứng" và chọn loại minh chứng (Nghị quyết/Quyết định, Biên bản họp, Khảo sát/Phiếu góp ý, Tài liệu tham khảo, v.v.).
    2.  Người dùng nhập thông tin metadata cho minh chứng:
        *   Tên minh chứng, Mô tả.
        *   Ngày ban hành, Đơn vị ban hành.
        *   Tags/Keywords để dễ tìm kiếm.
    3.  Người dùng upload file minh chứng (hỗ trợ các định dạng PDF, DOC, DOCX, XLS, XLSX, kích thước tối đa 20MB/file, có thể upload nhiều file cùng lúc).
    4.  Hệ thống phân loại minh chứng theo nhóm tiêu chuẩn (Chủ trương mở ngành, Năng lực đơn vị, Chương trình đào tạo, Đội ngũ giảng viên, Cơ sở vật chất...) và theo trạng thái (Draft, Pending, Approved, Archived).
    5.  Hệ thống tự động đánh số phiên bản cho minh chứng, lưu lịch sử thay đổi và theo dõi người thực hiện, cho phép rollback về phiên bản trước.
*   **Luồng xử lý thay thế:**
    *   **3a. File không hợp lệ/quá kích thước/có virus:**
        1.  Hệ thống thông báo lỗi và từ chối upload.
        2.  Yêu cầu người dùng kiểm tra lại file.
*   **Điều kiện sau:**
    *   Minh chứng được upload, phân loại và lưu trữ trong hệ thống.
    *   Thông tin phiên bản và lịch sử thay đổi được ghi nhận.

**UC-07b: Tìm kiếm và Truy xuất Minh chứng**

*   **Mục đích:** Cung cấp khả năng tìm kiếm và truy xuất minh chứng/tài liệu một cách hiệu quả.
*   **Actor chính:** Tất cả người dùng có quyền truy cập.
*   **Điều kiện tiên quyết:** Minh chứng đã được lưu trữ trong hệ thống.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn chức năng "Tìm kiếm minh chứng".
    2.  Người dùng có thể tìm kiếm theo metadata (Mã minh chứng, Tên, Loại, Thời gian, Người tạo) hoặc sử dụng tìm kiếm nâng cao (kết hợp nhiều điều kiện, full-text search, tìm theo tags, filter theo attributes).
    3.  Hệ thống hiển thị danh sách các minh chứng phù hợp với tiêu chí tìm kiếm.
    4.  Người dùng có thể xem chi tiết minh chứng, tải xuống file, hoặc xuất báo cáo minh chứng (Danh mục, Thống kê theo loại, Báo cáo tổng hợp) dưới các định dạng Excel, PDF, Word.
*   **Điều kiện sau:**
    *   Minh chứng được tìm thấy và truy xuất dễ dàng.
    *   Báo cáo minh chứng được tạo theo yêu cầu.

**UC-07c: Phân quyền Truy cập Minh chứng**

*   **Mục đích:** Thiết lập và quản lý quyền truy cập vào các minh chứng/tài liệu.
*   **Actor chính:** Quản trị hệ thống (Admin), TT.HL-DH.
*   **Điều kiện tiên quyết:** Người dùng có quyền quản trị hệ thống.
*   **Luồng xử lý chính:**
    1.  Người dùng thiết lập quyền truy cập theo nhóm người dùng (Admin, Manager, Editor, Viewer) hoặc theo loại tài liệu (Public, Internal, Confidential, Secret).
    2.  Hệ thống áp dụng các quy tắc phân quyền đã thiết lập.
    3.  Hệ thống theo dõi truy cập vào từng minh chứng (ghi log người truy cập, thời gian, hành động thực hiện, IP address).
*   **Điều kiện sau:**
    *   Quyền truy cập minh chứng được áp dụng chính xác.
    *   Lịch sử truy cập được ghi log đầy đủ.

#### UC-08: Quản lý quy trình phê duyệt và ban hành quyết định

**UC-08a: Trình phê duyệt CTĐT**

*   **Mục đích:** Quản lý quá trình trình duyệt Chương trình đào tạo (CTĐT) từ khi hoàn thiện đến khi được phê duyệt chính thức.
*   **Actor chính:** Đơn vị chuyên môn (ĐVCM), Trung tâm Học liệu - Phát triển Dạy và Học (TT.HL-DH).
*   **Điều kiện tiên quyết:** CTĐT đã hoàn thiện và sẵn sàng trình phê duyệt (đầy đủ minh chứng, biên bản thẩm định, phụ lục...).
*   **Luồng xử lý chính:**
    1.  ĐVCM chuẩn bị hồ sơ trình duyệt, kiểm tra các điều kiện cần thiết (CTĐT hoàn chỉnh, đầy đủ minh chứng, biên bản thẩm định...).
    2.  ĐVCM tạo phiếu trình duyệt, bao gồm thông tin CTĐT, tóm tắt quá trình xây dựng, các ý kiến góp ý đã tiếp thu và đề xuất phê duyệt.
    3.  Hồ sơ được trình duyệt qua các cấp:
        *   **Cấp Khoa/Đơn vị:** Hội đồng Khoa học & Đào tạo Khoa, Trưởng đơn vị ký duyệt.
        *   **Cấp Trường:** Hội đồng Khoa học & Đào tạo Trường, Ban Giám hiệu.
    4.  Hệ thống theo dõi trạng thái của hồ sơ trình duyệt (Submitted, In Review, Revised, Approved, Rejected) và tự động gửi thông báo cho các bên liên quan khi trạng thái thay đổi.
*   **Luồng xử lý thay thế:**
    *   **3a. Yêu cầu chỉnh sửa từ cấp duyệt:**
        1.  ĐVCM tiếp nhận phản hồi và các yêu cầu chỉnh sửa.
        2.  ĐVCM thực hiện chỉnh sửa CTĐT và hồ sơ, sau đó trình duyệt lại.
*   **Điều kiện sau:**
    *   Hồ sơ trình duyệt được tạo và theo dõi trong hệ thống.
    *   Trạng thái phê duyệt của CTĐT được cập nhật.

**UC-08b: Xử lý Phản hồi trong quy trình phê duyệt**

*   **Mục đích:** Quản lý việc tiếp nhận, phân loại và xử lý các phản hồi (góp ý, yêu cầu chỉnh sửa) từ các cấp phê duyệt.
*   **Actor chính:** ĐVCM, TT.HL-DH.
*   **Điều kiện tiên quyết:** Hồ sơ CTĐT đang trong quá trình phê duyệt và có phản hồi từ cấp duyệt.
*   **Luồng xử lý chính:**
    1.  ĐVCM/TT.HL-DH tiếp nhận phản hồi từ hệ thống, bao gồm ý kiến góp ý và yêu cầu chỉnh sửa.
    2.  Hệ thống hỗ trợ phân loại nội dung phản hồi (Yêu cầu chỉnh sửa, Đề xuất bổ sung, Góp ý cải tiến) và đánh giá mức độ quan trọng (Critical, Major, Minor).
    3.  ĐVCM phân công nhân sự xử lý phản hồi, cập nhật chỉnh sửa vào CTĐT và hồ sơ.
    4.  Hệ thống theo dõi tiến độ xử lý phản hồi và cho phép báo cáo kết quả xử lý.
*   **Điều kiện sau:**
    *   Các phản hồi được ghi nhận và xử lý.
    *   CTĐT và hồ sơ được cập nhật theo yêu cầu.

**UC-08c: Ban hành Quyết định**

*   **Mục đích:** Quản lý việc soạn thảo, trình ký và ban hành Quyết định phê duyệt CTĐT hoặc Quyết định mở ngành.
*   **Actor chính:** Ban Giám hiệu, TT.HL-DH.
*   **Điều kiện tiên quyết:** CTĐT/Đề án mở ngành đã được phê duyệt ở tất cả các cấp.
*   **Luồng xử lý chính:**
    1.  TT.HL-DH soạn thảo dự thảo Quyết định ban hành, bao gồm:
        *   Số quyết định, Ngày ban hành, Nội dung chính.
        *   Hiệu lực thi hành.
        *   Đính kèm CTĐT/Đề án đã được duyệt và danh sách các đơn vị nhận quyết định.
    2.  Dự thảo Quyết định được trình lên Ban Giám hiệu để xem xét và ký ban hành.
    3.  Sau khi có chữ ký của BGH, hệ thống cấp số quyết định chính thức và phát hành quyết định.
    4.  Hệ thống thông báo quyết định ban hành cho các bên liên quan và lưu trữ bản gốc quyết định cùng hồ sơ liên quan.
*   **Luồng xử lý thay thế:**
    *   **2a. Yêu cầu chỉnh sửa từ BGH:**
        1.  TT.HL-DH tiếp nhận ý kiến, chỉnh sửa dự thảo quyết định.
        2.  Trình ký lại BGH.
*   **Điều kiện sau:**
    *   Quyết định ban hành được tạo và lưu trữ chính thức.
    *   Các bên liên quan nhận được thông báo về quyết định.

#### UC-18: Quản lý các điều kiện đảm bảo mở ngành (giảng viên, CSVC,...)

*   **Mục đích:** Quản lý và giám sát việc đáp ứng các điều kiện đảm bảo chất lượng cần thiết để mở ngành đào tạo mới.
*   **Actor chính:** Đơn vị chuyên môn (ĐVCM), Trung tâm Học liệu - Phát triển Dạy và Học (TT.HL-DH).
*   **Điều kiện tiên quyết:**
    *   Đề xuất mở ngành đã được phê duyệt chủ trương.
    *   Có dữ liệu về nguồn lực hiện có của trường (giảng viên, cơ sở vật chất, tài chính...).
*   **Luồng xử lý chính:**
    1.  ĐVCM tạo hồ sơ điều kiện đảm bảo mở ngành, nhập thông tin chi tiết về:
        *   **Đội ngũ giảng viên:** Danh sách giảng viên dự kiến, trình độ, kinh nghiệm, khối lượng giảng dạy.
        *   **Cơ sở vật chất:** Phòng học, phòng thí nghiệm, thư viện, trang thiết bị.
        *   **Chương trình đào tạo:** CTĐT dự kiến, đề cương học phần.
        *   **Kinh phí đầu tư:** Dự toán kinh phí cho việc mở và vận hành ngành.
    2.  Hệ thống tự động kiểm tra các điều kiện này bằng cách:
        *   Đối chiếu với các quy định hiện hành của Bộ GD&ĐT và của Trường.
        *   Tính toán các chỉ số (ví dụ: tỷ lệ giảng viên/sinh viên, diện tích phòng học/sinh viên).
        *   Cảnh báo các thiếu sót hoặc điều kiện chưa đạt.
    3.  ĐVCM cập nhật thông tin, bổ sung minh chứng, điều chỉnh số liệu hoặc giải trình (nếu có) để đáp ứng các điều kiện.
    4.  Hệ thống theo dõi tiến độ hoàn thành các điều kiện, hiển thị tỷ lệ hoàn thành, các điều kiện còn thiếu và thời hạn khắc phục.
*   **Luồng xử lý thay thế:**
    *   **2a. Không đủ điều kiện:**
        1.  Hệ thống thông báo chi tiết các điều kiện không đạt.
        2.  ĐVCM cần đề xuất giải pháp khắc phục hoặc điều chỉnh kế hoạch mở ngành.
    *   **3a. Cần thẩm định lại điều kiện:**
        1.  Hệ thống tạo yêu cầu thẩm định lại các điều kiện đã bổ sung/chỉnh sửa.
        2.  Cập nhật kết quả thẩm định sau khi hoàn tất.
*   **Điều kiện sau:**
    *   Hồ sơ điều kiện đảm bảo mở ngành được cập nhật và lưu trữ.
    *   Kế hoạch khắc phục các thiếu sót (nếu có) được xây dựng.
    *   Thông báo về tình hình đáp ứng điều kiện được gửi đến các bên liên quan.

### 2.3. Module Quản trị Hệ thống

#### UC-10: Quản lý người dùng và phân quyền chi tiết theo vai trò

**UC-10a: Quản lý Tài khoản Người dùng**

*   **Mục đích:** Quản lý thông tin tài khoản người dùng (tạo mới, cập nhật, xóa, quản lý trạng thái).
*   **Actor chính:** Quản trị hệ thống (Admin), TT.HL-DH.
*   **Điều kiện tiên quyết:** Người dùng có quyền quản trị hệ thống.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn chức năng "Quản lý Tài khoản Người dùng".
    2.  Để tạo mới tài khoản, người dùng nhập thông tin cơ bản (Mã nhân viên/ID, Họ và tên, Email công vụ, Số điện thoại, Đơn vị, Chức danh) và thông tin tài khoản (Username, Password, Trạng thái, Ngày hiệu lực, Nhóm người dùng).
    3.  Để quản lý trạng thái, người dùng có thể Kích hoạt/Vô hiệu hóa, Reset mật khẩu, Gia hạn tài khoản, hoặc Xóa tài khoản.
    4.  Hệ thống kiểm tra tính hợp lệ của dữ liệu và thực hiện thao tác.
    5.  Hệ thống thông báo kết quả thao tác.
*   **Luồng xử lý thay thế:**
    *   **2a. Thông tin không hợp lệ/trùng lặp:**
        1.  Hệ thống hiển thị thông báo lỗi.
        2.  Người dùng quay lại chỉnh sửa.
*   **Điều kiện sau:**
    *   Thông tin tài khoản người dùng được cập nhật trong hệ thống.
    *   Trạng thái tài khoản được thay đổi theo yêu cầu.

**UC-10b: Phân quyền Hệ thống**

*   **Mục đích:** Thiết lập và quản lý vai trò (Roles) và quyền (Permissions) truy cập hệ thống.
*   **Actor chính:** Quản trị hệ thống (Admin), TT.HL-DH.
*   **Điều kiện tiên quyết:** Người dùng có quyền quản trị hệ thống.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn chức năng "Phân quyền Hệ thống".
    2.  Người dùng có thể quản lý các Vai trò (Roles) mặc định (System Admin, Unit Manager, Process Manager, Content Editor, Regular User) hoặc cấu hình vai trò mới (Tên vai trò, Mô tả, Danh sách quyền, Thứ tự ưu tiên).
    3.  Người dùng quản lý các Quyền (Permissions) theo nhóm quyền (Quản lý CTĐT, Quản lý quy trình, Quản lý tài liệu, Quản lý báo cáo) và loại quyền (Create, Read, Update, Delete, Approve).
    4.  Người dùng gán quyền cho người dùng (trực tiếp hoặc thừa kế từ nhóm), theo đơn vị (phân cấp đơn vị, quyền kế thừa) hoặc theo quy trình (theo vai trò, theo giai đoạn).
    5.  Hệ thống áp dụng các cấu hình phân quyền.
*   **Điều kiện sau:**
    *   Hệ thống phân quyền được cấu hình theo yêu cầu.
    *   Quyền truy cập của người dùng được cập nhật.

**UC-10c: Audit và Giám sát**

*   **Mục đích:** Theo dõi và ghi log các hoạt động của người dùng để đảm bảo bảo mật và tuân thủ.
*   **Actor chính:** Quản trị hệ thống (Admin), TT.HL-DH.
*   **Điều kiện tiên quyết:** Hệ thống đã được cấu hình để ghi log.
*   **Luồng xử lý chính:**
    1.  Hệ thống tự động theo dõi và ghi log các hoạt động:
        *   Log đăng nhập (Thời gian, IP address, Thiết bị, Kết quả).
        *   Log thao tác (Người thực hiện, Thời gian, Hành động, Đối tượng tác động).
    2.  Người dùng có thể xem các báo cáo bảo mật (Thống kê truy cập theo thời gian, người dùng, module) và nhận cảnh báo bảo mật (Login fails, Unauthorized access, Suspicious activities).
*   **Điều kiện sau:**
    *   Tất cả các hoạt động quan trọng được ghi log.
    *   Báo cáo và cảnh báo bảo mật được tạo ra.

#### UC-39: Quản lý luồng công việc (workflow) và hệ thống nhắc việc tự động

**UC-39a: Quản lý Workflow**

*   **Mục đích:** Định nghĩa, cấu hình và theo dõi các luồng công việc (workflow) trong hệ thống.
*   **Actor chính:** Quản trị hệ thống (Admin), TT.HL-DH.
*   **Điều kiện tiên quyết:** Người dùng có quyền quản trị workflow.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn chức năng "Quản lý Workflow".
    2.  Người dùng định nghĩa workflow bằng cách xác định:
        *   Các bước thực hiện (ví dụ: Soạn thảo, Thẩm định, Phê duyệt, Ban hành).
        *   Điều kiện chuyển tiếp giữa các bước.
        *   Người thực hiện hoặc vai trò chịu trách nhiệm cho mỗi bước.
    3.  Hệ thống cho phép theo dõi tiến trình của từng quy trình đang chạy:
        *   Trạng thái hiện tại của quy trình.
        *   Lịch sử xử lý (ai đã làm gì, khi nào).
        *   Thời gian còn lại cho mỗi bước.
*   **Điều kiện sau:**
    *   Các workflow được định nghĩa và hoạt động theo đúng quy trình.
    *   Tiến trình của các công việc được theo dõi minh bạch.

**UC-39b: Hệ thống nhắc việc tự động**

*   **Mục đích:** Cấu hình và gửi các thông báo nhắc việc tự động cho người dùng.
*   **Actor chính:** Quản trị hệ thống (Admin), TT.HL-DH.
*   **Điều kiện tiên quyết:** Workflow đã được định nghĩa và có người dùng được phân quyền.
*   **Luồng xử lý chính:**
    1.  Người dùng cấu hình nhắc việc bằng cách thiết lập:
        *   Loại thông báo (ví dụ: Sắp đến hạn, Quá hạn, Yêu cầu phê duyệt mới).
        *   Tần suất nhắc (ví dụ: Hàng ngày, Hàng tuần, Trước 3 ngày).
        *   Kênh thông báo (Email, SMS, Notification trong hệ thống).
    2.  Hệ thống tự động gửi thông báo nhắc việc đến người dùng liên quan dựa trên cấu hình và trạng thái của workflow.
    3.  Hệ thống theo dõi các deadline, cảnh báo khi công việc trễ hạn và cung cấp báo cáo về hiệu quả của hệ thống nhắc việc.
*   **Điều kiện sau:**
    *   Người dùng nhận được nhắc việc kịp thời.
    *   Tiến độ công việc được cải thiện nhờ nhắc việc tự động.

#### UC-09: Quản lý báo cáo và thống kê động

**UC-09a: Báo cáo Tổng hợp CTĐT**

*   **Mục đích:** Cung cấp các báo cáo tổng quan và chi tiết về Chương trình đào tạo (CTĐT).
*   **Actor chính:** Ban Giám hiệu, TT.HL-DH, Đơn vị chuyên môn (ĐVCM).
*   **Điều kiện tiên quyết:** Có quyền truy cập module báo cáo.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn chức năng "Báo cáo Tổng hợp CTĐT".
    2.  Hệ thống hiển thị các báo cáo danh mục CTĐT với thông tin tổng quan (Số lượng CTĐT theo trình độ, Phân bố theo khoa/đơn vị, Trạng thái hoạt động, Thống kê theo năm).
    3.  Người dùng có thể sử dụng chức năng lọc theo thời gian, đơn vị, trạng thái, trình độ đào tạo.
    4.  Hệ thống cung cấp báo cáo chi tiết CTĐT, bao gồm thông tin cấu trúc (Phân bố tín chỉ, Tỷ lệ các khối kiến thức, Danh sách học phần, Ma trận CĐR) và thống kê đối sánh (So sánh giữa các phiên bản, giữa các ngành, phân tích xu hướng).
*   **Điều kiện sau:**
    *   Các báo cáo tổng hợp và chi tiết về CTĐT được hiển thị.
    *   Người dùng có thể lọc và xem thông tin theo nhu cầu.

**UC-09b: Báo cáo Tiến độ Mở ngành**

*   **Mục đích:** Cung cấp các báo cáo và dashboard theo dõi tiến độ của quy trình mở ngành.
*   **Actor chính:** Ban Giám hiệu, TT.HL-DH, ĐVCM.
*   **Điều kiện tiên quyết:** Có quyền truy cập module báo cáo.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn chức năng "Báo cáo Tiến độ Mở ngành".
    2.  Hệ thống hiển thị dashboard tiến độ với các chỉ số (Tổng số đề xuất, Đang xử lý, Đã hoàn thành, Tạm dừng/Hủy) và cảnh báo deadline (Sắp đến hạn, Quá hạn, Cần can thiệp).
    3.  Hệ thống cung cấp phân tích quy trình về thời gian xử lý (theo từng bước, theo đơn vị, theo loại hình) và xác định các điểm nghẽn (bottleneck, nguyên nhân chậm trễ, đề xuất cải tiến).
*   **Điều kiện sau:**
    *   Dashboard và báo cáo tiến độ mở ngành được hiển thị.
    *   Các điểm nghẽn trong quy trình được xác định.

**UC-09c: Báo cáo Thống kê Nâng cao**

*   **Mục đích:** Cung cấp khả năng phân tích và trực quan hóa dữ liệu nâng cao.
*   **Actor chính:** Ban Giám hiệu, TT.HL-DH.
*   **Điều kiện tiên quyết:** Có quyền truy cập module báo cáo.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn chức năng "Báo cáo Thống kê Nâng cao".
    2.  Hệ thống cho phép phân tích dữ liệu bằng cách cung cấp thống kê mô tả (các chỉ số cơ bản, biểu đồ phân phối, phân tích xu hướng) và phân tích tương quan (giữa các chỉ tiêu, theo thời gian, theo đơn vị).
    3.  Hệ thống trực quan hóa dữ liệu thông qua các biểu đồ tương tác (Line charts, Bar charts, Pie charts, Heat maps) và dashboard tùy chỉnh (lựa chọn chỉ tiêu, định dạng hiển thị, lưu cấu hình).
*   **Điều kiện sau:**
    *   Các báo cáo thống kê nâng cao và biểu đồ trực quan được tạo ra.
    *   Người dùng có thể tùy chỉnh và lưu cấu hình báo cáo.

#### UC-11: Quản lý và cấu hình các tham số hệ thống

**UC-11a: Quản lý Tham số Hệ thống**

*   **Mục đích:** Quản lý các cấu hình chung và tham số kỹ thuật của hệ thống.
*   **Actor chính:** Quản trị hệ thống (Admin).
*   **Điều kiện tiên quyết:** Có quyền quản trị cao nhất trong hệ thống.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn chức năng "Quản lý Tham số Hệ thống".
    2.  Người dùng có thể cấu hình chung (Thông tin trường, Thời gian timeout, Số lần login tối đa, Kích thước file tối đa, Định dạng file cho phép) và cấu hình quy trình (Workflow settings, Validation rules).
    3.  Hệ thống kiểm tra tính hợp lệ của các tham số và lưu cấu hình.
    4.  Hệ thống thông báo cập nhật thành công.
*   **Điều kiện sau:**
    *   Các tham số hệ thống được cập nhật và áp dụng.

**UC-11b: Quản lý Danh mục**

*   **Mục đích:** Quản lý các danh mục dữ liệu cơ bản và chuyên môn của hệ thống.
*   **Actor chính:** Quản trị hệ thống (Admin), TT.HL-DH.
*   **Điều kiện tiên quyết:** Có quyền quản trị hệ thống.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn chức năng "Quản lý Danh mục".
    2.  Người dùng có thể quản lý danh mục cơ bản (Đơn vị trong trường, Trình độ đào tạo) và danh mục chuyên môn (Ngành đào tạo, Học phần).
    3.  Người dùng có thể thêm mới, chỉnh sửa hoặc xóa các mục trong danh mục.
    4.  Hệ thống kiểm tra tính duy nhất của mã, tính toàn vẹn dữ liệu và các tham chiếu trước khi xóa.
*   **Điều kiện sau:**
    *   Các danh mục dữ liệu được cập nhật và duy trì tính nhất quán.

**UC-11c: Quản lý Template**

*   **Mục đích:** Quản lý các mẫu (template) tài liệu và email được sử dụng trong hệ thống.
*   **Actor chính:** Quản trị hệ thống (Admin), TT.HL-DH.
*   **Điều kiện tiên quyết:** Có quyền quản trị hệ thống.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn chức năng "Quản lý Template".
    2.  Người dùng có thể quản lý template tài liệu (Đề cương học phần, Biên bản họp, Tờ trình, Quyết định) và template email (Thông báo họp, Yêu cầu phê duyệt, Nhắc việc, Thông báo kết quả).
    3.  Người dùng có thể cấu hình định dạng, field mapping, style mặc định, validation rules cho template tài liệu và subject pattern, body template, placeholder, CC/BCC rules cho template email.
*   **Điều kiện sau:**
    *   Các template được cấu hình và sẵn sàng sử dụng.

#### UC-14: Quản lý sao lưu và phục hồi dữ liệu

**UC-14a: Quản lý Backup**

*   **Mục đích:** Cấu hình và quản lý các hoạt động sao lưu dữ liệu của hệ thống.
*   **Actor chính:** Quản trị hệ thống (Admin), TT.HL-DH.
*   **Điều kiện tiên quyết:** Có quyền quản trị hệ thống và quyền truy cập storage.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn chức năng "Quản lý Backup".
    2.  Người dùng cấu hình loại backup (Full, Incremental, Differential, Transaction log) và lịch backup (Daily, Weekly, Monthly, Yearly).
    3.  Người dùng quản lý storage (chọn vị trí lưu trữ: Local, Network, Cloud, Offsite) và thiết lập retention policy (thời gian giữ các bản backup).
    4.  Hệ thống thực hiện sao lưu theo lịch trình và cấu hình đã thiết lập.
*   **Điều kiện sau:**
    *   Dữ liệu hệ thống được sao lưu định kỳ theo cấu hình.

**UC-14b: Quản lý Recovery**

*   **Mục đích:** Lập kế hoạch và thực hiện phục hồi dữ liệu hệ thống khi có sự cố.
*   **Actor chính:** Quản trị hệ thống (Admin), TT.HL-DH.
*   **Điều kiện tiên quyết:** Có các bản backup dữ liệu.
*   **Luồng xử lý chính:**
    1.  Người dùng chọn chức năng "Quản lý Recovery".
    2.  Người dùng lập kế hoạch phục hồi (Recovery Planning) bằng cách xác định loại phục hồi (Point-in-time, System state, File-level, Database) và lịch kiểm thử phục hồi.
    3.  Trong trường hợp thảm họa, người dùng thực hiện các thủ tục phục hồi sau thảm họa (DR procedures) và quản lý failover (chuyển đổi dự phòng).
    4.  Hệ thống thực hiện phục hồi dữ liệu từ bản backup đã chọn.
*   **Điều kiện sau:**
    *   Dữ liệu hệ thống được phục hồi thành công sau sự cố.

**UC-14c: Monitoring và Reporting Backup/Recovery**

*   **Mục đích:** Giám sát trạng thái sao lưu/phục hồi và tạo báo cáo tuân thủ.
*   **Actor chính:** Quản trị hệ thống (Admin), TT.HL-DH.
*   **Điều kiện tiên quyết:** Các hoạt động backup/recovery đang diễn ra.
*   **Luồng xử lý chính:**
    1.  Hệ thống tự động giám sát trạng thái backup (tiến độ, thành công/thất bại, dung lượng lưu trữ, hiệu năng) và hệ thống cảnh báo (khi có lỗi backup, cảnh báo storage, lỗi hệ thống).
    2.  Hệ thống tạo các báo cáo tuân thủ (Backup status reports, Recovery test reports, Audit logs, Compliance documents) theo lịch trình (Daily, Weekly, Monthly, Annual).
*   **Điều kiện sau:**
    *   Trạng thái backup/recovery được giám sát liên tục.
    *   Các báo cáo tuân thủ được tạo ra định kỳ.
