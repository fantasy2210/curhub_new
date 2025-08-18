# BÁO CÁO MINH CHỨNG: TRIỂN KHAI THỬ NGHIỆM NỘI BỘ

**Dự án:** Xây dựng Hệ thống Quản lý Chương trình Đào tạo và Hỗ trợ Mở mã ngành đào tạo (CURHUB)

| Hạng mục | Nội dung |
| :--- | :--- |
| **Thời gian hoàn thành** | 15/07/2025 |
| **Người chịu trách nhiệm** | Nhóm xây dựng hệ thống, Ban Phát triển CTĐT của CELRI |
| **Tần suất báo cáo** | Sau khi hoàn thành |
| **Hồ sơ** | Báo cáo triển khai, phản hồi người dùng |

---

## 1. Mục tiêu Giai đoạn Triển khai Thử nghiệm Nội bộ

Giai đoạn này có mục tiêu triển khai phiên bản hiện tại của hệ thống CURHUB cho nhóm người dùng nòng cốt là **Ban Phát triển Chương trình Đào tạo của CELRI** để:
- **Xác thực Luồng nghiệp vụ:** Đảm bảo các chức năng đã xây dựng (tập trung vào quản lý CTĐT) phù hợp và tối ưu cho quy trình làm việc thực tế của Ban.
- **Đánh giá Tính khả dụng (Usability):** Thu thập phản hồi trực tiếp về trải nghiệm người dùng, xác định các điểm cần cải thiện trong giao diện và thao tác.
- **Kiểm thử Chức năng trong Môi trường thật:** Phát hiện các lỗi phát sinh khi hệ thống được vận hành với dữ liệu và kịch bản sử dụng thực tế của nhóm CELRI.

## 2. Phạm vi Thử nghiệm

- **Môi trường:** Hệ thống được triển khai trên máy chủ Staging (`staging.curhub.tvu.edu.vn`), cho phép truy cập trong mạng nội bộ.
- **Đối tượng:** Toàn bộ thành viên của Ban Phát triển CTĐT của CELRI.
- **Dữ liệu:** Sử dụng dữ liệu từ 2-3 chương trình đào tạo thực tế đang được Ban quản lý để nhập liệu và thao tác.
- **Chức năng trọng tâm:**
    - Tạo mới và cập nhật thông tin CTĐT.
    - Quản lý chi tiết cấu trúc CTĐT: Mục tiêu (PO), Chuẩn đầu ra (PLO), Học phần (thêm/sửa/xóa/import).
    - Quản lý phiên bản và quy trình duyệt (Nháp -> Chờ duyệt -> Phê duyệt).
    - Xây dựng và quản lý các phiên bản Đề cương học phần.
    - Sử dụng các tính năng hỗ trợ (tìm kiếm, xem lưu đồ chương trình, các chức năng có tích hợp AI).

## 3. Kế hoạch Triển khai

1.  **Chuẩn bị (Trước 01/07/2025):**
    - Hoàn tất triển khai phiên bản ổn định lên máy chủ Staging.
    - Chuẩn bị tài khoản đăng nhập cho tất cả thành viên của Ban.
    - Tổ chức một buổi họp khởi động (kick-off) ngắn để giới thiệu mục tiêu, phạm vi và kế hoạch thử nghiệm.

2.  **Thực hiện (01/07 - 12/07/2025):**
    - **Tuần 1:** Người dùng làm quen với hệ thống, thực hiện nhập liệu cho 1 CTĐT mẫu theo tài liệu hướng dẫn.
    - **Tuần 2:** Người dùng thực hiện các luồng nghiệp vụ phức tạp hơn như cập nhật CTĐT, tạo phiên bản mới, thực hiện quy trình duyệt, xây dựng đề cương.

3.  **Tổng kết (15/07/2025):**
    - Tổ chức buổi họp tổng kết để thu thập phản hồi cuối cùng, thảo luận về các vấn đề nổi cộm và định hướng cho giai đoạn tiếp theo.

## 4. Quy trình Thu thập và Xử lý Phản hồi

1.  **Kênh thu thập:**
    - **Công cụ theo dõi:** Sử dụng một bảng Trello (hoặc file Excel chia sẻ) để các thành viên CELRI có thể trực tiếp tạo các thẻ (card) cho mỗi vấn đề phát hiện. Mỗi thẻ cần có:
        - Mô tả ngắn gọn.
        - Các bước tái hiện (nếu là lỗi).
        - Ảnh chụp màn hình.
        - Phân loại (Lỗi / Góp ý / Câu hỏi).
    - **Nhóm Zalo:** Một nhóm Zalo chung sẽ được tạo để trao đổi nhanh, hỏi đáp và thông báo các cập nhật.

2.  **Quy trình xử lý:**
    - Nhóm phát triển sẽ kiểm tra bảng Trello hàng ngày.
    - Các lỗi khẩn cấp (critical) sẽ được ưu tiên sửa ngay trong ngày.
    - Các góp ý và lỗi không khẩn cấp sẽ được tổng hợp, phân tích và đưa vào kế hoạch điều chỉnh sau khi giai đoạn thử nghiệm kết thúc.

---
**KẾT LUẬN**

Giai đoạn triển khai thử nghiệm là một bước quan trọng để đảm bảo hệ thống CURHUB thực sự đáp ứng được nhu cầu của người dùng và hoạt động ổn định trong môi trường thực tế. Kế hoạch chi tiết về đối tượng, phạm vi và quy trình xử lý phản hồi sẽ giúp tối đa hóa giá trị thu được từ giai đoạn này, làm tiền đề cho việc hoàn thiện sản phẩm cuối cùng.
