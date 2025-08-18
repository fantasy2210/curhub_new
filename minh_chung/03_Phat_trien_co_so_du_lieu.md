# BÁO CÁO MINH CHỨNG: PHÁT TRIỂN CƠ SỞ DỮ LIỆU

**Dự án:** Xây dựng Hệ thống Quản lý Chương trình Đào tạo và Hỗ trợ Mở mã ngành đào tạo (CURHUB)

| Hạng mục | Nội dung |
| :--- | :--- |
| **Thời gian hoàn thành** | 31/12/2024 |
| **Người chịu trách nhiệm** | Nhóm xây dựng hệ thống |
| **Tần suất báo cáo** | Sau khi hoàn thành |
| **Hồ sơ** | Mô hình CSDL |

---

## 1. Tổng quan

Cơ sở dữ liệu của hệ thống CURHUB được thiết kế theo mô hình quan hệ, sử dụng hệ quản trị CSDL MySQL. Việc thiết kế tuân thủ các nguyên tắc chuẩn hóa để đảm bảo tính toàn vẹn, nhất quán và giảm thiểu dư thừa dữ liệu. Django ORM được sử dụng để ánh xạ các mô hình dữ liệu trong mã nguồn Python sang các bảng trong CSDL.

## 2. Sơ đồ Quan hệ Thực thể (ERD - Entity-Relationship Diagram) Chi tiết

Sơ đồ dưới đây mô tả các thực thể chính và mối quan hệ giữa chúng, phản ánh cấu trúc trong tệp `models.py` của hệ thống.

```mermaid
erDiagram
    ChuongTrinhDaoTao {
        int id PK
        string ma_nganh_ctdt UK
        string ten_nganh_ctdt
        string version
        string trang_thai
        int phien_ban_goc_id FK
        int don_vi_quan_ly_id FK
    }

    HocPhan {
        int id PK
        string ma_hoc_phan UK
        string ten_hoc_phan
        int tong_so_tin_chi_goc
    }

    ChiTietHocPhanTrongCTDT {
        int id PK
        int chuong_trinh_dao_tao_id FK
        int hoc_phan_id FK
        boolean la_bat_buoc
        int hoc_ky_du_kien
    }

    DeCuongHocPhan {
        int id PK
        int hoc_phan_id FK
        string ten_de_cuong_phien_ban
        boolean la_phien_ban_hien_hanh
        string trang_thai
    }

    MucTieuDaoTao {
        int id PK
        int chuong_trinh_dao_tao_id FK
        string ma_muc_tieu
        text noi_dung
    }

    ChuanDauRa {
        int id PK
        int chuong_trinh_dao_tao_id FK
        string ma_cdr
        text noi_dung
    }

    ChuanDauRaHocPhan {
        int id PK
        int de_cuong_id FK
        string ma_clo
        text noi_dung
    }

    GiangVien {
        int id PK
        string ho_ten
        string ma_can_bo
    }

    TaiLieuHocTap {
        int id PK
        string nhan_de
        string tac_gia
    }

    DeCuongTaiLieu {
        int id PK
        int de_cuong_id FK
        int tai_lieu_id FK
        string loai_lien_ket
    }

    ChuongTrinhDaoTao ||--o{ MucTieuDaoTao : "có các"
    ChuongTrinhDaoTao ||--o{ ChuanDauRa : "có các"
    ChuongTrinhDaoTao }o--o{ GiangVien : "có các giảng viên tham gia"
    ChuongTrinhDaoTao }o--o{ HocPhan : "bao gồm các" (through ChiTietHocPhanTrongCTDT)
    
    ChiTietHocPhanTrongCTDT ||--|{ ChuongTrinhDaoTao : "thuộc về"
    ChiTietHocPhanTrongCTDT ||--|{ HocPhan : "tham chiếu tới"

    HocPhan ||--o{ DeCuongHocPhan : "có các phiên bản"
    DeCuongHocPhan ||--o{ ChuanDauRaHocPhan : "có các"
    DeCuongHocPhan }o--o{ TaiLieuHocTap : "sử dụng" (through DeCuongTaiLieu)

    ChuanDauRaHocPhan }o--o{ ChuanDauRa : "đáp ứng"

```

## 3. Mô tả các Bảng (Thực thể) chính

### 3.1. `daotao_chuongtrinhdaotao`
- **Mô tả:** Lưu trữ thông tin cốt lõi về một phiên bản cụ thể của chương trình đào tạo. Hệ thống quản lý phiên bản và quy trình duyệt được tích hợp ngay trong model này.
- **Các trường chính:** `ma_nganh_ctdt`, `ten_nganh_ctdt`, `don_vi_quan_ly`, `version`, `trang_thai` (Bản nháp, Chờ duyệt, Đã phê duyệt...), `phien_ban_goc`.

### 3.2. `daotao_hocphan`
- **Mô tả:** Đóng vai trò là một thư viện học phần chung cho toàn trường, chứa các thông tin gốc của một học phần.
- **Các trường chính:** `ma_hoc_phan`, `ten_hoc_phan`, `tong_so_tin_chi_goc`, `so_gio_ly_thuyet_goc`, `don_vi_quan_ly_goc`.

### 3.3. `daotao_chitiethocphantrongctdt`
- **Mô tả:** Là model trung gian (through model) quan trọng, thể hiện mối quan hệ giữa một CTĐT và một Học phần. Nó cho phép tùy chỉnh các thuộc tính của học phần (số tín chỉ, số giờ, học kỳ,...) cho riêng CTĐT đó mà không ảnh hưởng đến học phần gốc trong thư viện.
- **Các trường chính:** `chuong_trinh_dao_tao`, `hoc_phan`, `danh_muc_kien_thuc`, `la_bat_buoc`, `hoc_ky_du_kien`, `tin_chi_ly_thuyet_apdung`.

### 3.4. `daotao_decuonghocphan`
- **Mô tả:** Quản lý các phiên bản của đề cương học phần. Mỗi học phần có thể có nhiều phiên bản đề cương, nhưng chỉ một phiên bản được đánh dấu là `la_phien_ban_hien_hanh`. Model này cũng có trạng thái để quản lý quy trình duyệt.
- **Các trường chính:** `hoc_phan`, `ten_de_cuong_phien_ban`, `ngay_ban_hanh`, `trang_thai`, `la_phien_ban_hien_hanh`.

### 3.5. `daotao_muctieudaotao` (PO) & `daotao_chuandaura` (PLO)
- **Mô tả:** Lưu trữ các Mục tiêu đào tạo (Program Objectives) và Chuẩn đầu ra (Program Learning Outcomes) của một CTĐT.
- **Các trường chính:** `chuong_trinh_dao_tao`, `ma_muc_tieu`/`ma_cdr`, `noi_dung`.

### 3.6. `daotao_chuandaurahocphan` (CLO)
- **Mô tả:** Lưu trữ các Chuẩn đầu ra của một học phần (Course Learning Outcomes), thuộc về một phiên bản đề cương cụ thể.
- **Các trường chính:** `de_cuong`, `ma_clo`, `noi_dung`, `muc_do_bloom`.

### 3.7. `daotao_giangvien`
- **Mô tả:** Lưu trữ thông tin danh sách giảng viên của trường.
- **Các trường chính:** `ho_ten`, `ma_can_bo`, `chuc_danh_khoa_hoc`, `co_quan_cong_tac`.

### 3.8. Các bảng khác
- **`daotao_tailieuhoctap`:** Kho tài liệu học tập chung.
- **`daotao_decuongtailieu`:** Bảng trung gian kết nối Đề cương và Tài liệu học tập.
- **`daotao_hinhthucdanhgia`:** Các hình thức đánh giá cho một đề cương.
- **`daotao_lichsuthaydoictdt`:** Ghi log lại các thay đổi quan trọng trên CTĐT.
- **Lưu ý:** Các model liên quan đến quy trình mở ngành tổng thể (Hội đồng, Đề án,...) chưa được triển khai trong phiên bản hiện tại.

---
**KẾT LUẬN**

Mô hình CSDL được thiết kế để phản ánh chính xác các quy trình nghiệp vụ phức tạp của việc quản lý CTĐT và mở ngành. Việc sử dụng Django ORM không chỉ giúp đẩy nhanh quá trình phát triển mà còn đảm bảo tính nhất quán và dễ bảo trì của tầng dữ liệu. Mô hình này có khả năng mở rộng để đáp ứng các yêu cầu phát sinh trong tương lai.
