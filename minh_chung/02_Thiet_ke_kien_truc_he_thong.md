# BÁO CÁO MINH CHỨNG: THIẾT KẾ KIẾN TRÚC HỆ THỐNG

**Dự án:** Xây dựng Hệ thống Quản lý Chương trình Đào tạo và Hỗ trợ Mở mã ngành đào tạo (CURHUB)

| Hạng mục | Nội dung |
| :--- | :--- |
| **Thời gian hoàn thành** | 31/10/2024 |
| **Người chịu trách nhiệm** | Nhóm xây dựng hệ thống |
| **Tần suất báo cáo** | Sau khi hoàn thành |
| **Hồ sơ** | Tài liệu thiết kế hệ thống |

---

## 1. Tổng quan Kiến trúc

Hệ thống CURHUB được thiết kế dựa trên kiến trúc **Monolithic với các module được phân tách rõ ràng (Modular Monolith)**, sử dụng framework **Django**. Lựa chọn này nhằm đảm bảo sự phát triển nhanh chóng, dễ dàng triển khai và bảo trì, đồng thời vẫn duy trì tính tổ chức và khả năng mở rộng trong tương lai.

- **Framework:** Django 4.x
- **Ngôn ngữ:** Python 3.10+
- **Cơ sở dữ liệu:** MySQL 8.0
- **Web Server:** Nginx
- **Application Server:** Gunicorn

## 2. Sơ đồ Kiến trúc Tổng thể

```
+------------------+      +------------------+      +----------------------+
|   Người dùng     | <--> |    Web Browser   | <--> |        Nginx         |
| (BGH, ĐVCM, ...) |      | (Desktop/Mobile) |      | (Reverse Proxy &     |
+------------------+      +------------------+      |   Static Files)      |
                                                     +-----------+----------+
                                                                 |
                                                                 v
                                                     +-----------+----------+
                                                     |       Gunicorn       |
                                                     | (Application Server) |
                                                     +-----------+----------+
                                                                 |
                                                                 v
+--------------------------------------------------------------------------------------------------+
|                                          DJANGO APPLICATION (CURHUB)                               |
|--------------------------------------------------------------------------------------------------|
| +----------------------+  +-----------------------+  +-----------------------+  +----------------+ |
| | Middleware & Auth    |  | URL Routing           |  | Templates & Views     |  | Forms          | |
| | (Security, Sessions) |  | (urls.py)             |  | (Giao diện người dùng)|  | (Xử lý input)  | |
| +----------------------+  +-----------------------+  +-----------------------+  +----------------+ |
|--------------------------------------------------------------------------------------------------|
|                                          BUSINESS LOGIC LAYER                                    |
|--------------------------------------------------------------------------------------------------|
| | Module Quản lý CTĐT  |  | Module Mở ngành        |  | Module Quản trị Hệ thống|  | Services       | |
| | (models.py, views.py)|  | (models.py, views.py) |  | (models.py, views.py) |  | (Nghiệp vụ)    | |
| +----------------------+  +-----------------------+  +-----------------------+  +----------------+ |
|--------------------------------------------------------------------------------------------------|
|                                          DATA ACCESS LAYER (ORM)                                 |
|--------------------------------------------------------------------------------------------------|
|                                                Django ORM                                        |
|--------------------------------------------------------------------------------------------------|
+--------------------------------------------------+-------------------------------------------------+
                                                   |
                                                   v
                                       +-----------+-----------+
                                       |      MySQL DB         |
                                       | (Cơ sở dữ liệu chính) |
                                       +-----------------------+
```

## 3. Mô tả các Thành phần

### 3.1. Presentation Layer (Tầng trình diễn)
- **Nginx:** Đóng vai trò là Reverse Proxy, tiếp nhận các yêu cầu HTTP từ người dùng, chuyển tiếp các yêu cầu động đến Gunicorn và phục vụ các tệp tĩnh (CSS, JavaScript, hình ảnh) trực tiếp để tăng hiệu năng.
- **Django Templates:** Sử dụng hệ thống template của Django kết hợp với HTML, CSS (AdminLTE theme) và JavaScript để xây dựng giao diện người dùng (UI) động và responsive.

### 3.2. Application Layer (Tầng ứng dụng)
- **Gunicorn:** Là một WSGI application server, chịu trách nhiệm chạy ứng dụng Django, quản lý các worker process để xử lý đồng thời nhiều yêu cầu.
- **Django Framework:**
    - **URL Routing:** `urls.py` ánh xạ các URL đến các `views` xử lý tương ứng.
    - **Views:** `views.py` chứa logic xử lý yêu cầu, tương tác với `models` và `services` để lấy dữ liệu và trả về response thông qua `templates`.
    - **Middleware:** Xử lý các vấn đề chung như xác thực người dùng (Authentication), quản lý phiên (Session), và bảo mật (CSRF protection).

### 3.3. Business Logic Layer (Tầng nghiệp vụ)
Đây là lõi của ứng dụng, được tổ chức thành các Django apps (modules) tương ứng với các nhóm chức năng chính:
- **Module `daotao` (Quản lý CTĐT & Mở ngành):**
    - **`models.py`:** Định nghĩa các mô hình dữ liệu như `ChuongTrinhDaoTao`, `HocPhan`, `ChuanDauRa`, `DeCuongHocPhan`, `HoiDong`, `MinhChung`.
    - **`views.py`:** Chứa logic cho các chức năng như tạo/sửa CTĐT, quản lý CĐR, quy trình thẩm định, v.v.
    - **`forms.py`:** Định nghĩa các form để nhập và kiểm tra dữ liệu.
    - **`services.py`:** Chứa các logic nghiệp vụ phức tạp, tách biệt khỏi `views` để dễ dàng tái sử dụng và kiểm thử (ví dụ: service tính toán tín chỉ, service kiểm tra điều kiện mở ngành).
- **Module `accounts` (Quản trị Hệ thống):**
    - Quản lý người dùng, vai trò (roles), và phân quyền (permissions) dựa trên hệ thống `django.contrib.auth`.

### 3.4. Data Access Layer (Tầng truy cập dữ liệu)
- **Django ORM (Object-Relational Mapping):** Cung cấp một lớp trừu tượng để tương tác với cơ sở dữ liệu. Logic nghiệp vụ sẽ thao tác trên các đối tượng Python (models) thay vì viết các câu lệnh SQL trực tiếp, giúp mã nguồn dễ đọc, bảo trì và độc lập với hệ quản trị CSDL.
- **MySQL Database:** Là nơi lưu trữ toàn bộ dữ liệu của hệ thống một cách bền vững.

## 4. Thiết kế Tích hợp
- **Single Sign-On (SSO):** Hệ thống sẽ tích hợp với hệ thống xác thực tập trung của nhà trường (ví dụ: LDAP, Active Directory) để người dùng có thể sử dụng một tài khoản duy nhất.
- **API:** Cung cấp các API endpoint (sử dụng Django Rest Framework) để có thể tích hợp với các hệ thống khác trong tương lai (ví dụ: hệ thống quản lý sinh viên, hệ thống học liệu số).

---
**KẾT LUẬN**

Kiến trúc Modular Monolith với Django là một lựa chọn cân bằng, phù hợp với các yêu cầu của dự án CURHUB. Nó không chỉ đáp ứng các yêu cầu chức năng và phi chức năng đã đề ra mà còn tạo nền tảng vững chắc cho việc bảo trì, phát triển và mở rộng hệ thống trong tương lai.
