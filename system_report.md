# Báo cáo Chi tiết Tình trạng Hệ thống Quản lý Chương trình Đào tạo

**Ngày báo cáo:** 08/08/2025

**Người tạo báo cáo:** Cline - Kỹ sư phần mềm AI

## 1. Tổng quan

Báo cáo này cung cấp một cái nhìn tổng quan chi tiết về tình trạng hiện tại của hệ thống "Curriculum Hub" (curhub), được thiết kế để hỗ trợ việc chuyển giao dự án cho một nhóm phát triển mới. Báo cáo bao gồm phân tích về công nghệ, kiến trúc, cấu trúc dữ liệu và các chức năng chính của hệ thống.

## 2. Phân tích Công nghệ

Hệ thống được xây dựng dựa trên một ngăn xếp công nghệ hiện đại và phổ biến, tập trung vào hệ sinh thái Python và Django.

### 2.1. Framework và Thư viện chính

Dựa trên tệp `requirements.txt`, các công nghệ cốt lõi bao gồm:

- **Backend Framework:** `Django==5.2.1` - Một framework web Python mạnh mẽ và an toàn, cung cấp nền tảng vững chắc cho ứng dụng.
- **Cơ sở dữ liệu:** Hệ thống sử dụng MySQL, được thể hiện qua các thư viện `mysql-connector-python==9.4.0` và `mysqlclient==2.2.7`.
- **Xử lý dữ liệu:** `pandas==2.3.1` và `numpy==2.3.1` được sử dụng, cho thấy khả năng xử lý, phân tích và có thể là nhập/xuất dữ liệu hàng loạt (ví dụ: từ các tệp CSV, Excel).
- **Giao diện người dùng (Frontend):**
    - `django-crispy-forms==2.4` và `crispy-bootstrap5==2025.6` được dùng để render các form Django một cách đẹp mắt và nhất quán với Bootstrap 5.
    - `django-widget-tweaks==1.5.0` cung cấp khả năng tùy chỉnh widget của form một cách linh hoạt.
- **Tích hợp AI/LLM:** Sự hiện diện của `ollama` và `langextract` cho thấy hệ thống có tích hợp các mô hình ngôn ngữ lớn (LLM) để hỗ trợ các tác vụ như đánh giá hoặc trích xuất thông tin.
- **Thư viện tiện ích:** `python-dateutil`, `pytz`, `six`, `sqlparse`, `tzdata`, `XlsxWriter`, `python-docx`, `requests` là các thư viện hỗ trợ cho các tác vụ khác nhau.

### 2.2. Môi trường

- **Hệ điều hành:** Windows 11
- **Web Server (phát triển):** Django development server.
- **Cấu hình:** Tệp `curhub/curhub/settings.py` chứa tất cả các cấu hình của dự án.

## 3. Kiến trúc Hệ thống

Hệ thống tuân theo kiến trúc Model-View-Template (MVT) tiêu chuẩn của Django.

- **Project chính:** `curhub`
- **Ứng dụng (App) chính:** `daotao` - Chứa hầu hết logic nghiệp vụ của hệ thống.

### 3.1. Cấu trúc Thư mục

Cấu trúc thư mục được tổ chức tốt, phân tách rõ ràng các thành phần:

- `curhub/`: Thư mục gốc của dự án Django.
    - `curhub/`: Thư mục chứa cấu hình dự án (`settings.py`, `urls.py` chính).
    - `daotao/`: Ứng dụng chính.
        - `models.py`: Định nghĩa cấu trúc cơ sở dữ liệu.
        - `views/`: Logic xử lý được chia thành nhiều tệp nhỏ (`ctdt_views.py`, `hoc_phan_views.py`, `api_views.py`, v.v.), giúp dễ quản lý.
        - `urls.py`: Định tuyến URL cho ứng dụng `daotao`.
        - `templates/`: Chứa các tệp HTML template.
        - `templatetags/`: Các template tag và filter tùy chỉnh.
        - `management/commands/`: Các lệnh quản lý tùy chỉnh (ví dụ: import/export dữ liệu).
    - `static/`: Chứa các tệp tĩnh (CSS, JS, hình ảnh).
    - `templates/`: Chứa các template cơ sở (base templates).

### 3.2. Định tuyến URL

- **URL gốc:** Tất cả các URL của ứng dụng được đặt dưới tiền tố `/daotao/`.
- **Phân tách logic:** `daotao/urls.py` phân chia các URL theo chức năng (CTĐT, học phần, đơn vị, giảng viên, API), giúp dễ dàng theo dõi và bảo trì.
- **API Endpoints:** Hệ thống có một lượng lớn các API endpoint (`/daotao/api/...`), cho thấy giao diện người dùng có tính tương tác cao, sử dụng nhiều JavaScript để cập nhật dữ liệu động mà không cần tải lại trang.

## 4. Cấu trúc Cơ sở dữ liệu (Phân tích từ `models.py`)

Cơ sở dữ liệu là trái tim của hệ thống, được thiết kế chi tiết để quản lý toàn diện quy trình đào tạo.

### 4.1. Các Model Chính

- **`ChuongTrinhDaoTao` (CTĐT):** Thực thể trung tâm, đại diện cho một chương trình đào tạo cụ thể. Model này rất chi tiết, bao gồm:
    - Thông tin định danh (mã, tên, trình độ, hình thức).
    - Quản lý phiên bản (`version`, `phien_ban_goc`, `ly_do_thay_doi`).
    - Quy trình phê duyệt (`trang_thai`: Nháp, Chờ duyệt, Đã phê duyệt).
    - Mối quan hệ Many-to-Many với `HocPhan` và `GiangVien`.
- **`HocPhan`:** Thư viện các học phần chung của toàn trường.
- **`ChiTietHocPhanTrongCTDT`:** Model trung gian, cho phép tùy chỉnh thông tin của một học phần (số tín chỉ, giờ học, học phần tiên quyết) cho một CTĐT cụ thể.
- **`DeCuongHocPhan`:** Quản lý các phiên bản đề cương chi tiết cho mỗi học phần.
- **`MucTieuDaoTao` (PO - Program Objectives):** Các mục tiêu cấp cao của một CTĐT.
- **`ChuanDauRa` (PLO - Program Learning Outcomes):** Các chuẩn đầu ra mà sinh viên cần đạt được khi hoàn thành CTĐT.
- **`ChuanDauRaHocPhan` (CLO - Course Learning Outcomes):** Các chuẩn đầu ra của một học phần cụ thể.
- **`GiangVien`:** Thông tin chi tiết về giảng viên.
- **`PhanCongGiangDay`:** Phân công giảng viên cho các học phần trong một CTĐT.
- **Các model phụ trợ:** `DonViDaoTao`, `NganhDaoTao`, `DanhMucKienThuc`, `MaTranCDR_CTHP`, `LichSuThayDoiCTDT`.

### 4.2. Mối quan hệ Dữ liệu

- **CTĐT và Học phần:** Một CTĐT có nhiều học phần, và một học phần có thể thuộc nhiều CTĐT. Model `ChiTietHocPhanTrongCTDT` làm trung gian cho mối quan hệ này.
- **CTĐT và Chuẩn đầu ra (PLO):** Một CTĐT có nhiều PLO.
- **Học phần và Chuẩn đầu ra (CLO):** Một đề cương học phần có nhiều CLO.
- **PLO và CLO:** Mối liên kết giữa chúng được thể hiện qua `MaTranCDR_CTHP`, cho thấy mức độ đóng góp của mỗi học phần vào việc đạt được chuẩn đầu ra của chương trình.

## 5. Chức năng chính của Hệ thống

Dựa trên phân tích URL và model, hệ thống có các nhóm chức năng chính sau:

### 5.1. Quản lý Chương trình Đào tạo (CTĐT)

- **CRUD (Tạo, Đọc, Cập nhật, Xóa)** cho CTĐT.
- **Quản lý phiên bản:** Tạo phiên bản mới từ một CTĐT hiện có.
- **Quy trình phê duyệt:** Gửi duyệt, phê duyệt, từ chối CTĐT.
- **Xây dựng cấu trúc CTĐT:**
    - Thêm/xóa/sửa học phần trong CTĐT (hàng loạt hoặc đơn lẻ).
    - Quản lý mục tiêu đào tạo (PO) và chuẩn đầu ra (PLO).
    - Chỉnh sửa thông tin chi tiết của học phần áp dụng cho CTĐT.
- **So sánh CTĐT:** Chức năng so sánh giữa hai chương trình đào tạo.
- **Quản lý giảng viên:** Phân công giảng viên tham gia giảng dạy trong CTĐT.

### 5.2. Quản lý Học phần và Đề cương

- **Thư viện học phần:** Quản lý danh sách học phần chung.
- **Quản lý đề cương:** Tạo và quản lý các phiên bản đề cương cho mỗi học phần, bao gồm nội dung chi tiết, hình thức đánh giá, và chuẩn đầu ra (CLO).

### 5.3. Quản lý Danh mục

- Quản lý các đơn vị đào tạo (khoa, bộ môn).
- Quản lý các ngành đào tạo.
- Quản lý danh mục kiến thức (ví dụ: kiến thức giáo dục đại cương, kiến thức cơ sở ngành).

### 5.4. Chức năng API và Tương tác

- **Giao diện động:** Nhiều chức năng được thực hiện thông qua API, cho phép cập nhật nội tuyến (inline editing) mà không cần tải lại trang.
- **Tìm kiếm động:** API tìm kiếm học phần, giảng viên.
- **Lấy dữ liệu cho UI:** API cung cấp dữ liệu để vẽ lưu đồ chương trình (`flowchart-data`), hiển thị chi tiết trong các modal.
- **Tích hợp LLM:** API `danh_gia_cdr_api` cho thấy khả năng sử dụng AI để đánh giá chuẩn đầu ra.

## 6. Đề xuất cho Nhóm Phát triển Mới

1.  **Nắm vững `models.py`:** Đây là tệp quan trọng nhất để hiểu logic nghiệp vụ của hệ thống.
2.  **Khám phá các `views`:** Bắt đầu với `ctdt_views.py` và `api_views.py` để hiểu luồng xử lý chính và cách giao diện người dùng tương tác với backend.
3.  **Kiểm tra các template:** Xem các tệp trong `daotao/templates/daotao/` đặc biệt là `chi_tiet_ctdt.html` để hiểu cách dữ liệu được hiển thị và cách các API được gọi (có thể qua các thư viện JavaScript như htmx hoặc custom scripts).
4.  **Thiết lập môi trường:** Cài đặt tất cả các thư viện trong `requirements.txt` và cấu hình kết nối cơ sở dữ liệu MySQL trong `settings.py`.
5.  **Xem xét các lệnh quản lý:** Các lệnh trong `daotao/management/commands/` rất hữu ích cho việc nhập dữ liệu ban đầu hoặc di chuyển dữ liệu.

Báo cáo này hy vọng sẽ là một tài liệu khởi đầu hữu ích cho nhóm phát triển mới. Hệ thống được xây dựng tốt, có cấu trúc rõ ràng và sử dụng các công nghệ phổ biến, tạo điều kiện thuận lợi cho việc tiếp quản và phát triển trong tương lai.
