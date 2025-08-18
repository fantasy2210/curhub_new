# BÁO CÁO MINH CHỨNG: PHÂN TÍCH YÊU CẦU HỆ THỐNG

**Dự án:** Xây dựng Hệ thống Quản lý Chương trình Đào tạo và Hỗ trợ Mở mã ngành đào tạo (CURHUB)

| Hạng mục | Nội dung |
| :--- | :--- |
| **Thời gian hoàn thành** | 30/09/2024 |
| **Người chịu trách nhiệm** | Nhóm xây dựng hệ thống |
| **Tần suất báo cáo** | Sau khi hoàn thành |
| **Hồ sơ** | Tài liệu đặc tả yêu cầu hệ thống |

---

## 1. Giới thiệu

Tài liệu này phân tích các yêu cầu cốt lõi của **Hệ thống Quản lý Chương trình Đào tạo và Hỗ trợ Mở mã ngành đào tạo (CURHUB)** tại Trường Đại học Trà Vinh. Mục tiêu của hệ thống là số hóa và tích hợp quy trình xây dựng, quản lý chương trình đào tạo (CTĐT) và quy trình mở ngành, nhằm tăng cường hiệu quả quản lý, giám sát, và đảm bảo tính minh bạch.

## 2. Bối cảnh và Mục tiêu

- **Bối cảnh:** Quy trình xây dựng CTĐT và mở ngành hiện tại còn thực hiện thủ công, dẫn đến nhu cầu cấp thiết về việc số hóa và tự động hóa để quản lý tập trung.
- **Mục tiêu:**
    - Số hóa toàn bộ quy trình xây dựng CTĐT và mở ngành.
    - Rút ngắn 50% thời gian xử lý.
    - Giảm 90% việc sử dụng văn bản giấy.
    - Tăng độ chính xác của dữ liệu lên 99%.
    - Cung cấp khả năng tra cứu, báo cáo dễ dàng và minh bạch.

## 3. Các Bên Liên Quan (Actors)

Hệ thống xác định các nhóm người dùng chính và phụ với vai trò và quyền hạn rõ ràng:

- **Primary Actors:**
    - **Ban Giám hiệu:** Phê duyệt cuối cùng, ban hành quyết định.
    - **Đơn vị chuyên môn (Khoa/Bộ môn):** Chủ trì xây dựng CTĐT, đề xuất mở ngành.
    - **Trung tâm Học liệu - Phát triển Dạy và Học (TT.HL-DH):** Quản trị hệ thống, điều phối quy trình.
    - **Các Hội đồng (Hội đồng Trường, HĐ Khoa học & Đào tạo, HĐ Thẩm định):** Phê duyệt chủ trương, thẩm định chuyên môn, đánh giá độc lập.
- **Secondary Actors:**
    - **Các phòng ban chức năng:** Đảm bảo chất lượng, Tổ chức nhân sự, Đào tạo, v.v.
    - **Chuyên gia bên ngoài, Giảng viên, Đơn vị sử dụng lao động.**

## 4. Yêu cầu Chức năng (Functional Requirements)

Hệ thống được cấu thành từ các module chính với các chức năng cụ thể như sau:

### 4.1. Module Quản lý CTĐT
- **(UC-01)** Quản lý thông tin chung của CTĐT (tạo mới, cập nhật).
- **(UC-02)** Quản lý chuẩn đầu ra (CĐR) của CTĐT.
- **(UC-03)** Quản lý danh mục học phần.
- **(UC-04)** Quản lý đề cương chi tiết học phần.
- **(UC-05)** Quản lý phiên bản của CTĐT, cho phép so sánh và khôi phục.
- **(UC-15)** Đối sánh CTĐT với các chương trình khác.
- **(UC-17)** Đánh giá CTĐT định kỳ.

### 4.2. Module Hỗ trợ Mở ngành Đào tạo
- **(UC-27)** Quản lý tờ trình đề xuất chủ trương mở ngành.
- **(UC-06)** Quản lý việc thành lập và hoạt động của các Hội đồng.
- **(UC-28, UC-32)** Quản lý quy trình thẩm định các cấp.
- **(UC-07)** Quản lý minh chứng và tài liệu liên quan.
- **(UC-08)** Quản lý quy trình phê duyệt và ban hành quyết định.
- **(UC-18)** Quản lý các điều kiện đảm bảo mở ngành (giảng viên, CSVC,...).

### 4.3. Module Quản trị Hệ thống
- **(UC-10)** Quản lý người dùng và phân quyền chi tiết theo vai trò.
- **(UC-39)** Quản lý luồng công việc (workflow) và hệ thống nhắc việc tự động.
- **(UC-09)** Quản lý báo cáo và thống kê động.
- **(UC-11)** Quản lý và cấu hình các tham số hệ thống.
- **(UC-14)** Quản lý sao lưu và phục hồi dữ liệu.

## 5. Yêu cầu Phi Chức năng (Non-Functional Requirements)

- **Hiệu năng (Performance):**
    - Thời gian phản hồi cho các tác vụ thông thường dưới 3 giây.
    - Hỗ trợ tối thiểu 100 người dùng đồng thời.
- **Bảo mật (Security):**
    - Tích hợp xác thực một lần (SSO).
    - Phân quyền dựa trên vai trò (RBAC).
    - Mã hóa dữ liệu nhạy cảm và ghi log toàn bộ hoạt động.
- **Tính sẵn sàng (Availability):**
    - Uptime đạt 99.9% trong giờ hành chính.
    - Có cơ chế sao lưu hàng ngày và kế hoạch phục hồi sau thảm họa (RTO < 4 giờ).
- **Khả năng mở rộng (Scalability):**
    - Hệ thống có kiến trúc module, cho phép dễ dàng mở rộng, nâng cấp chức năng trong tương lai.
- **Giao diện (Interface):**
    - Giao diện thân thiện, dễ sử dụng, tuân thủ thiết kế responsive để tương thích trên nhiều thiết bị (desktop, mobile).

## 6. Ràng buộc và Quy tắc Nghiệp vụ

Hệ thống phải tuân thủ các quy tắc và ràng buộc nghiệp vụ đã được định nghĩa chi tiết trong tài liệu đặc tả, bao gồm:
- Quy trình đề xuất, xây dựng và phê duyệt CTĐT.
- Cấu trúc và nội dung CTĐT (khối lượng tín chỉ, chuẩn đầu ra, ma trận tương quan).
- Quy trình và thành phần Hội đồng thẩm định.
- Quy tắc quản lý học phần, phiên bản, và các thay đổi.
- Các điều kiện đảm bảo chất lượng và kiểm định.

---
**KẾT LUẬN**

Bản phân tích này tóm lược các yêu cầu trọng tâm, là cơ sở để đội ngũ phát triển tiến hành thiết kế, xây dựng và kiểm thử hệ thống CURHUB, đảm bảo sản phẩm cuối cùng đáp ứng đúng và đủ các nhu-cầu nghiệp vụ đã đặt ra.
