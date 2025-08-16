# Hướng dẫn sử dụng tính năng Gợi ý AI trong Form Đề cương học phần

## Tổng quan

Form Đề cương học phần đã được cải thiện với giao diện hiện đại và tính năng gợi ý thông minh từ AI. Tính năng này giúp tạo ra các đề xuất cho học liệu tham khảo và chuẩn đầu ra học phần một cách nhanh chóng và hiệu quả.

## Tính năng mới

### 1. Giao diện người dùng cải thiện
- **Bố cục logic**: Form được chia thành 3 phần rõ ràng với tiêu đề và mô tả chi tiết
- **Thiết kế hiện đại**: Sử dụng màu sắc, gradient và hiệu ứng chuyển tiếp mượt mà
- **Responsive**: Hoạt động tốt trên cả máy tính và thiết bị di động
- **Thanh tiến trình**: Hiển thị tỷ lệ hoàn thành form

### 2. Tính năng AI Suggestions
- **Gợi ý học liệu**: Tự động đề xuất sách giáo khoa, tài liệu tham khảo và học liệu trực tuyến
- **Gợi ý chuẩn đầu ra**: Tạo ra các chuẩn đầu ra học phần phù hợp với từng danh mục
- **Modal hiện đại**: Hiển thị gợi ý trong cửa sổ popup đẹp mắt với trạng thái loading

### 3. Quản lý form động
- **Thêm/xóa linh hoạt**: Có thể thêm hoặc xóa học liệu và chuẩn đầu ra một cách dễ dàng
- **Validation tự động**: Kiểm tra các trường bắt buộc trước khi lưu
- **Select2 tích hợp**: Trải nghiệm chọn lựa tốt hơn với thư viện Select2

## Cấu hình AI Suggestions

### Bước 1: Lấy API Key từ OpenAI
1. Truy cập [OpenAI Platform](https://platform.openai.com/)
2. Đăng nhập hoặc tạo tài khoản
3. Vào mục "API Keys" và tạo một API key mới
4. Sao chép API key này

### Bước 2: Cấu hình trong Django
Mở file `curhub/curhub/settings.py` và thêm cấu hình sau:

```python
# AI/LLM Configuration
OPENAI_API_KEY = 'your-openai-api-key-here'  # Thay bằng API key thực tế
OPENAI_MODEL = "gpt-3.5-turbo"  # Model có thể thay đổi
OPENAI_MAX_TOKENS = 500  # Số token tối đa cho mỗi gợi ý
OPENAI_TEMPERATURE = 0.7  # Độ sáng tạo (0-1)
```

### Bước 3: Kiểm tra hoạt động
1. Khởi động lại server Django
2. Truy cập form tạo/sửa đề cương học phần
3. Nhấn nút "Gợi ý học liệu từ AI" hoặc "Gợi ý từ AI"
4. Nếu thấy modal với thông báo "Đang tạo gợi ý từ AI..." thì đã hoạt động thành công

## Hướng dẫn sử dụng

### 1. Tạo đề cương học phần mới
1. Đi đến danh sách học phần
2. Chọn học phần cần tạo đề cương
3. Nhấn nút "Thêm đề cương"
4. Điền thông tin theo các phần được gợi ý

### 2. Sử dụng AI để gợi ý học liệu
1. Ở phần "Danh sách Học liệu tham khảo"
2. Nhấn nút "Gợi ý học liệu từ AI"
3. Chờ AI tạo gợi ý
4. Sao chép và dán vào các trường tương ứng

### 3. Sử dụng AI để gợi ý chuẩn đầu ra
1. Ở phần "Chuẩn đầu ra của học phần"
2. Chọn danh mục cần gợi ý (Kiến thức, Kỹ năng, Thái độ)
3. Nhấn nút "Gợi ý từ AI"
4. Chờ AI tạo gợi ý
5. Áp dụng hoặc chỉnh sửa cho phù hợp

### 4. Quản lý học liệu và chuẩn đầu ra
- **Thêm**: Nhấn nút "Thêm học liệu" hoặc "Thêm CĐR"
- **Xóa**: Nhấn nút × ở góc trên bên phải của mỗi mục
- **Sắp xếp**: Các mục được đánh số tự động

## Troubleshooting

### 1. AI không hoạt động
- Kiểm tra đã thêm `OPENAI_API_KEY` trong settings.py chưa
- Kiểm tra API key có hợp lệ và còn hạn sử dụng không
- Kiểm tra kết nối internet

### 2. Form hiển thị không đẹp
- Kiểm tra đã include CSS file `de_cuong_form.css` chưa
- Kiểm tra browser có hỗ trợ CSS modern không
- Xóa cache browser và thử lại

### 3. Lỗi khi lưu form
- Kiểm tra đã điền đầy đủ các trường bắt buộc
- Kiểm tra các giá trị nhập vào có hợp lệ không
- Kiểm tra console browser để xem lỗi chi tiết

## Tối ưu hóa

### 1. Tùy chỉnh prompt
Bạn có thể chỉnh sửa các prompt trong file `suggestion_service.py` để phù hợp hơn với nhu cầu:

```python
# Trong file suggestion_service.py
def generate_syllabus_suggestions(course_name, course_description=None, clo_category=None):
    # Tùy chỉnh prompt tại đây
```

### 2. Thêm các loại gợi ý khác
Có thể mở rộng tính năng để gợi ý:
- Phương pháp giảng dạy
- Tiêu chí đánh giá
- Kế hoạch bài giảng

### 3. Tích hợp với các AI khác
Ngoài OpenAI, có thể tích hợp với:
- Google Gemini
- Anthropic Claude
- Các mô hình mã nguồn mở

## Kết luận

Form đề cương học phần đã được cải thiện đáng kể với giao diện hiện đại và tính năng AI thông minh. Việc sử dụng AI giúp tiết kiệm thời gian và tạo ra các đề cương chất lượng cao hơn.

Để có trải nghiệm tốt nhất, hãy đảm bảo:
- Đã cấu hình đúng API key
- Kết nối internet ổn định
- Sử dụng trình duyệt hiện đại
