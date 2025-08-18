# Báo cáo Tiến độ Thực hiện Use Case - Hệ thống CURHUB

Dựa trên tài liệu "Đặc tả Use Case Hệ thống CURHUB" và kết quả phân tích mã nguồn ngày 18/08/2025, dưới đây là báo cáo chi tiết về tiến độ hoàn thành của từng Use Case.

## Bảng Tổng kết Tiến độ

| Module | Đã làm | Đang làm | Chưa làm | Tổng số |
| :--- | :---: | :---: | :---: | :---: |
| 2.1. Quản lý CTĐT | 10 | 1 | 4 | 15 |
| 2.2. Hỗ trợ Mở ngành Đào tạo | 0 | 3 | 3 | 6 |
| 2.3. Quản trị Hệ thống | 0 | 3 | 2 | 5 |
| **Tổng cộng** | **10** | **7** | **9** | **26** |

---

**Quy ước:**

*   **[Đã làm]**: Chức năng đã được hiện thực và có thể sử dụng.
*   **[Đang làm]**: Chức năng đã được hiện thực một phần.
*   **[Chưa làm]**: Chức năng chưa được hiện thực trong mã nguồn.

---

## 2.1. Module Quản lý CTĐT

### UC-01: Quản lý thông tin chung của CTĐT

*   **UC-01a: Tạo mới CTĐT**: **[Đã làm]**
    *   *Ghi chú:* Chức năng được hiện thực qua view `them_chuong_trinh_dao_tao`.
*   **UC-01b: Cập nhật CTĐT**: **[Đã làm]**
    *   *Ghi chú:* Chức năng được hiện thực qua view `sua_ctdt`. Hệ thống có kiểm tra trạng thái "Bản nháp" và ghi lại lịch sử thay đổi.

### UC-02: Quản lý chuẩn đầu ra (CĐR) của CTĐT

*   **UC-02a: Xây dựng CĐR**: **[Đã làm]**
    *   *Ghi chú:* Chức năng thêm/sửa/xóa CĐR (PLO) và Mục tiêu đào tạo (PO) đã được hiện thực trong view `chi_tiet_ctdt` và các API liên quan (`api_them_po`, `api_sua_plo`...).
*   **UC-02b: Khảo sát CĐR**: **[Chưa làm]**
    *   *Ghi chú:* Không tìm thấy chức năng tạo mẫu khảo sát, gửi email, hay thu thập kết quả.
*   **UC-02c: Phê duyệt CĐR**: **[Đang làm]**
    *   *Ghi chú:* Quy trình phê duyệt CĐR được gắn liền với quy trình phê duyệt chung của CTĐT (`gui_duyet_ctdt`, `xu_ly_duyet_ctdt`). Chưa có quy trình phê duyệt riêng lẻ cho CĐR.

### UC-03: Quản lý danh mục học phần

*   **UC-03a: Thêm học phần mới**: **[Đã làm]**
    *   *Ghi chú:* Chức năng quản lý thư viện học phần chung (thêm, sửa, xóa) đã được hiện thực trong `hoc_phan_views.py`.

### UC-04: Quản lý đề cương chi tiết học phần

*   **UC-04a: Tạo đề cương**: **[Đã làm]**
    *   *Ghi chú:* Hiện thực qua view `them_de_cuong`.
*   **UC-04b: Cập nhật nội dung đề cương**: **[Đã làm]**
    *   *Ghi chú:* Hiện thực qua view `sua_de_cuong`.
*   **UC-04c: Phê duyệt đề cương**: **[Đã làm]**
    *   *Ghi chú:* Có các view `submit_for_approval`, `approve_de_cuong`, `reject_de_cuong` để xử lý quy trình phê duyệt.
*   **UC-04d: Quản lý phiên bản đề cương**: **[Chưa làm]**
    *   *Ghi chú:* Hệ thống hiện tại chỉ lưu một phiên bản đề cương cho mỗi học phần, chưa có chức năng quản lý nhiều phiên bản, so sánh hay khôi phục.

### UC-05: Quản lý phiên bản của CTĐT

*   **UC-05a: Tạo phiên bản mới**: **[Đã làm]**
    *   *Ghi chú:* Hiện thực qua view `tao_phien_ban_moi_ctdt`, cho phép clone một CTĐT thành phiên bản mới.
*   **UC-05b: So sánh phiên bản**: **[Đã làm]**
    *   *Ghi chú:* Hiện thực qua view `doi_sanh_ctdt`.
*   **UC-05c: Khôi phục phiên bản**: **[Chưa làm]**
    *   *Ghi chú:* Chưa có chức năng khôi phục CTĐT về một phiên bản cũ.

### UC-15: Đối sánh CTĐT với các chương trình khác

*   **UC-15**: **[Đã làm]**
    *   *Ghi chú:* Chức năng được hiện thực qua view `doi_sanh_ctdt`, cho phép so sánh hai CTĐT trong hệ thống.

### UC-17: Đánh giá CTĐT định kỳ

*   **UC-17**: **[Chưa làm]**
    *   *Ghi chú:* Không có chức năng tạo đợt đánh giá, thu thập dữ liệu hay tạo báo cáo tự đánh giá.

---

## 2.2. Module Hỗ trợ Mở ngành Đào tạo

*Ghi chú: Hầu hết các Use Case trong module này chưa được tìm thấy trong mã nguồn hiện tại. Hệ thống đang tập trung vào việc quản lý các CTĐT đã tồn tại.*

*   **UC-27: Quản lý tờ trình đề xuất chủ trương mở ngành**: **[Chưa làm]**
*   **UC-06: Quản lý việc thành lập và hoạt động của các Hội đồng**: **[Chưa làm]**
*   **UC-28, UC-32: Quản lý quy trình thẩm định các cấp**: **[Chưa làm]**
*   **UC-07: Quản lý minh chứng và tài liệu liên quan**: **[Đang làm]**
    *   *Ghi chú:* Đã có module `tai_lieu_views.py` để quản lý thư viện tài liệu học tập chung. Tuy nhiên, chưa có chức năng quản lý minh chứng theo ngữ cảnh mở ngành, phân loại, hay quản lý phiên bản minh chứng.
*   **UC-08: Quản lý quy trình phê duyệt và ban hành quyết định**: **[Đang làm]**
    *   *Ghi chú:* Đã có quy trình phê duyệt cho CTĐT và Đề cương học phần. Chưa có quy trình chung cho việc ban hành quyết định mở ngành.
*   **UC-18: Quản lý các điều kiện đảm bảo mở ngành (giảng viên, CSVC,...)**: **[Đang làm]**
    *   *Ghi chú:* Đã có chức năng quản lý Giảng viên (`giang_vien_views.py`) và phân công giảng viên cho CTĐT. Chưa có chức năng quản lý CSVC hay các điều kiện khác, cũng như chưa có cơ chế kiểm tra tự động.

---

## 2.3. Module Quản trị Hệ thống

*   **UC-10: Quản lý người dùng và phân quyền chi tiết theo vai trò**: **[Đang làm]**
    *   *Ghi chú:* Hệ thống sử dụng cơ chế phân quyền sẵn có của Django (`@permission_required`). Việc quản lý người dùng và nhóm quyền được thực hiện qua trang admin của Django, chưa có giao diện riêng.
*   **UC-39: Quản lý luồng công việc (workflow) và hệ thống nhắc việc tự động**: **[Chưa làm]**
*   **UC-09: Quản lý báo cáo và thống kê động**: **[Đang làm]**
    *   *Ghi chú:* Đã có các trang danh sách với bộ lọc và tìm kiếm. Tại trang chi tiết CTĐT có biểu đồ tròn phân bố tín chỉ. Chưa có các báo cáo động, dashboard hay thống kê nâng cao.
*   **UC-11: Quản lý và cấu hình các tham số hệ thống**: **[Đang làm]**
    *   *Ghi chú:* Đã có chức năng quản lý các danh mục như Đơn vị đào tạo, Danh mục kiến thức. Các tham số hệ thống khác có thể đang được quản lý trong file `settings.py` hoặc qua trang admin, chưa có giao diện riêng.
*   **UC-14: Quản lý sao lưu và phục hồi dữ liệu**: **[Chưa làm]**
    *   *Ghi chú:* Đây là chức năng ở tầng hạ tầng, thường được cấu hình ở cấp độ database hoặc server, không có giao diện trong ứng dụng.

---

## Tổng kết

*   **Các chức năng đã hoàn thiện tốt:** Quản lý thông tin CTĐT, quản lý thư viện học phần, quản lý đề cương chi tiết và quy trình phê duyệt đề cương.
*   **Các chức năng cần phát triển thêm:** Quản lý phiên bản (đề cương, CTĐT), báo cáo thống kê, phân quyền chi tiết trên giao diện.
*   **Các chức năng chưa được phát triển:** Toàn bộ module **Hỗ trợ Mở ngành Đào tạo**, khảo sát CĐR, đánh giá CTĐT định kỳ, quản lý workflow.

Báo cáo này cung cấp cái nhìn tổng quan về hiện trạng của dự án so với yêu cầu ban đầu, giúp định hướng cho các giai đoạn phát triển tiếp theo.
