# BÁO CÁO MINH CHỨNG: ĐÁNH GIÁ VÀ HOÀN THIỆN (SAU THỬ NGHIỆM NỘI BỘ)

**Dự án:** Xây dựng Hệ thống Quản lý Chương trình Đào tạo và Hỗ trợ Mở mã ngành đào tạo (CURHUB)

| Hạng mục | Nội dung |
| :--- | :--- |
| **Thời gian hoàn thành** | 31/07/2025 |
| **Người chịu trách nhiệm** | Nhóm xây dựng hệ thống |
| **Tần suất báo cáo** | Sau khi hoàn thành |
| **Hồ sơ** | Báo cáo đánh giá, kế hoạch điều chỉnh |

---

## 1. Mục đích

Báo cáo này tổng kết các kết quả thu được từ giai đoạn Triển khai Thử nghiệm Nội bộ với Ban Phát triển CTĐT của CELRI. Mục tiêu là phân tích các phản hồi, lỗi và đề xuất để xây dựng kế hoạch hành động nhằm hoàn thiện và ổn định hệ thống.

## 2. Tổng kết Giai đoạn Thử nghiệm Nội bộ

- **Thời gian thực hiện:** 01/07/2025 - 15/07/2025.
- **Đối tượng:** Thành viên Ban Phát triển CTĐT của CELRI.
- **Kết quả chung:** Hệ thống được đánh giá là đã số hóa thành công và hiệu quả quy trình xây dựng, quản lý CTĐT. Các chức năng cốt lõi hoạt động đúng và giúp giảm tải đáng kể công việc thủ công.
- **Tổng số phản hồi:** 28
    - **Lỗi (Bug):** 8
    - **Yêu cầu cải tiến (Enhancement):** 15
    - **Câu hỏi (Question):** 5

## 3. Phân tích các Phản hồi Nổi bật từ Nhóm CELRI

Các phản hồi từ nhóm người dùng nòng cốt rất giá trị, tập trung vào việc tối ưu hóa quy trình và tăng cường tiện ích.

| ID Vấn đề | Phân loại | Mô tả Vấn đề | Phản hồi từ Người dùng CELRI | Mức độ Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| **CELRI-BUG-01** | Lỗi (High) | Khi "Tạo phiên bản mới" cho một CTĐT, các mối quan hệ tiên quyết/song hành của học phần không được sao chép sang phiên bản mới. | "Phải định nghĩa lại toàn bộ quan hệ tiên quyết, rất mất thời gian và dễ sai sót." | Cao |
| **CELRI-ENH-01** | Cải tiến (High) | Chức năng "Thêm học phần hàng loạt" từ file Excel rất hữu ích, nhưng file kết quả trả về không chỉ rõ học phần nào bị lỗi và lỗi ở cột nào. | "Cần cải thiện file kết quả để chúng tôi có thể sửa lỗi và re-upload nhanh chóng." | Cao |
| **CELRI-ENH-02** | Cải tiến (High) | Giao diện quản lý đề cương học phần yêu cầu phải quay lại danh sách CTĐT rồi chọn lại học phần, khá nhiều bước. | "Nên có menu điều hướng nhanh (breadcrumbs) hoặc cách chuyển đổi qua lại giữa các đề cương trong cùng một CTĐT dễ dàng hơn." | Cao |
| **CELRI-ENH-03** | Cải tiến (Medium) | Chức năng gợi ý của AI đôi khi cho kết quả không liên quan hoặc quá chung chung. | "Cần có cơ chế để tinh chỉnh prompt hoặc cung cấp thêm ngữ cảnh cho AI để kết quả gợi ý tốt hơn." | Trung bình |

## 4. Kế hoạch Điều chỉnh và Hoàn thiện

Dựa trên các phản hồi trên, nhóm phát triển sẽ tập trung vào các hạng mục sau:

| ID Vấn đề | Kế hoạch Hành động | Người thực hiện | Thời gian Dự kiến |
| :--- | :--- | :--- | :--- |
| **CELRI-BUG-01** | Cập nhật service `tao_phien_ban_moi_ctdt` để sau khi sao chép các `ChiTietHocPhanTrongCTDT`, sẽ đọc và sao chép lại các quan hệ `hoc_phan_tien_quyet` và `hoc_phan_song_hanh` cho phiên bản mới. | Backend Team | 4 ngày |
| **CELRI-ENH-01** | Cải tiến chức năng import: Khi import thất bại, hệ thống sẽ cho phép tải về một file Excel mới, trong đó file này là file gốc của người dùng và được bổ sung thêm một cột "Kết quả" ghi rõ "Thành công" hoặc "Lỗi: [mô tả chi tiết]". | Full-stack Team | 1 tuần |
| **CELRI-ENH-02** | Bổ sung breadcrumbs (ví dụ: `Trang chủ > Danh sách CTĐT > CTĐT ABC > Đề cương học phần XYZ`) cho trang quản lý đề cương. Thêm một dropdown ở đầu trang đề cương để cho phép người dùng chuyển nhanh đến đề cương của một học phần khác trong cùng CTĐT. | Frontend Team | 3 ngày |
| **CELRI-ENH-03** | Nâng cấp chức năng gợi ý AI: Bổ sung một trường "Ngữ cảnh bổ sung" (tùy chọn) trong giao diện để người dùng có thể cung cấp thêm thông tin (ví dụ: "dành cho sinh viên năm nhất", "tập trung vào ứng dụng thực tế") để AI đưa ra gợi ý chính xác hơn. | Full-stack Team | 1 tuần |

**Công việc tiếp theo:**
- Sau khi hoàn tất các điều chỉnh trên, sẽ triển khai lại phiên bản mới lên máy chủ Staging và mời nhóm CELRI kiểm tra lại (regression test).
- Bắt đầu chuẩn bị cho kế hoạch mở rộng thử nghiệm ra các đơn vị khác.

---
**KẾT LUẬN**

Giai đoạn UAT đã cung cấp những thông tin đầu vào vô giá từ góc độ người dùng cuối. Các phản hồi đã được tổng hợp và phân tích kỹ lưỡng. Kế hoạch điều chỉnh cuối cùng đã được thiết lập rõ ràng và khả thi. Sau khi hoàn thành kế hoạch này, hệ thống CURHUB sẽ đạt được độ hoàn thiện cao, sẵn sàng cho việc tập huấn người dùng và đưa vào sử dụng chính thức.
