# BÁO CÁO MINH CHỨNG: PHÁT TRIỂN CÁC CHỨC NĂNG BACKEND

**Dự án:** Xây dựng Hệ thống Quản lý Chương trình Đào tạo và Hỗ trợ Mở mã ngành đào tạo (CURHUB)

| Hạng mục | Nội dung |
| :--- | :--- |
| **Thời gian hoàn thành** | 30/04/2025 |
| **Người chịu trách nhiệm** | Nhóm xây dựng hệ thống |
| **Tần suất báo cáo** | Sau khi hoàn thành |
| **Hồ sơ** | Mã nguồn |

---

## 1. Tổng quan

Backend của hệ thống CURHUB được xây dựng bằng framework Django, tuân thủ theo kiến trúc Model-View-Template (MVT). Tầng backend chịu trách nhiệm xử lý toàn bộ logic nghiệp vụ, xác thực người dùng, tương tác với cơ sở dữ liệu và trả về dữ liệu cho tầng frontend hiển thị.

Mã nguồn được tổ chức thành các module (Django apps) tương ứng với các nhóm chức năng, trong đó `daotao` là module chính xử lý các nghiệp vụ cốt lõi.

## 2. Minh chứng Mã nguồn các Chức năng Tiêu biểu

Dưới đây là các đoạn mã thực tế từ hệ thống, minh họa cho việc triển khai một số chức năng backend quan trọng.

### 2.1. Chức năng: Cập nhật thông tin chi tiết học phần trực tiếp (Inline Editing)

**Mô tả:** Đây là một API endpoint cho phép người dùng chỉnh sửa nhanh các thông tin của một học phần ngay trên bảng danh sách mà không cần tải lại trang. Chức năng này thể hiện việc xử lý AJAX, kiểm tra quyền và quy tắc nghiệp vụ.

**Tệp liên quan:** `curhub/daotao/views/api_views.py`

```python
# curhub/daotao/views/api_views.py

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from ..models import ChiTietHocPhanTrongCTDT, DanhMucKienThuc

@require_http_methods(["POST"])
@permission_required('daotao.change_chitiethocphantrongctdt', raise_exception=True)
def update_chi_tiet_hoc_phan_inline(request):
    try:
        pk = request.POST.get('pk')
        field = request.POST.get('field')
        value = request.POST.get('value')

        chi_tiet_hp = get_object_or_404(ChiTietHocPhanTrongCTDT, pk=pk)

        # Kiểm tra quy tắc nghiệp vụ: Chỉ cho sửa khi CTĐT ở trạng thái "Bản nháp"
        if chi_tiet_hp.chuong_trinh_dao_tao.trang_thai != 'DRAFT':
            return JsonResponse({'status': 'error', 'message': 'Chỉ có thể chỉnh sửa khi CTĐT ở trạng thái "Bản nháp".'}, status=403)

        # Whitelist các trường được phép chỉnh sửa để bảo mật
        allowed_fields = [
            'hoc_ky_du_kien', 'tin_chi_ly_thuyet_apdung', 'tin_chi_thuc_hanh_apdung',
            'so_gio_ly_thuyet_apdung', 'so_gio_thuc_hanh_apdung', 'la_bat_buoc', 'danh_muc_kien_thuc'
        ]
        if field not in allowed_fields:
            return JsonResponse({'status': 'error', 'message': f'Trường "{field}" không được phép chỉnh sửa.'}, status=400)

        # Xử lý và xác thực kiểu dữ liệu đầu vào
        if field == 'danh_muc_kien_thuc':
            value = get_object_or_404(DanhMucKienThuc, pk=value) if value else None
        elif field == 'la_bat_buoc':
            value = value.lower() in ['true', '1']
        # ... (các xử lý khác)

        setattr(chi_tiet_hp, field, value)
        chi_tiet_hp.save(update_fields=[field])

        return JsonResponse({'status': 'success', 'message': 'Cập nhật thành công!'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
```
**Phân tích:**
- **Bảo mật:** Sử dụng decorator `@permission_required` để đảm bảo chỉ người dùng có quyền `change_chitiethocphantrongctdt` mới có thể thực thi. Đồng thời, sử dụng một `allowed_fields` whitelist để ngăn chặn việc thay đổi các trường không mong muốn.
- **Quy tắc nghiệp vụ:** Kiểm tra trạng thái của CTĐT (`trang_thai != 'DRAFT'`) trước khi cho phép chỉnh sửa, đảm bảo tính toàn vẹn của dữ liệu đã được phê duyệt.
- **Hiệu quả:** Chỉ cập nhật một trường duy nhất trong CSDL (`update_fields=[field]`), giúp tối ưu hiệu năng.
- **UX:** Trả về `JsonResponse` để frontend có thể cập nhật giao diện ngay lập tức mà không cần tải lại trang.

### 2.2. Chức năng: Tìm kiếm và Đồng bộ Tài liệu học tập từ API ngoài

**Mô tả:** Chức năng này cho phép người dùng tìm kiếm tài liệu học tập. Nó không chỉ tìm trong CSDL cục bộ mà còn gọi đến một API bên ngoài, sau đó tự động cập nhật hoặc tạo mới (`update_or_create`) các tài liệu tìm thấy vào CSDL cục bộ trước khi trả về kết quả tổng hợp.

**Tệp liên quan:** `curhub/daotao/views/api_views.py`

```python
# curhub/daotao/views/api_views.py

import requests
from django.db.models import Q
from ..models import TaiLieuHocTap

@login_required
def api_search_tai_lieu(request):
    search_term = request.GET.get('q', '').strip()
    if len(search_term) < 3:
        return JsonResponse({'results': []})

    found_pks = set()

    # Bước 1: Tìm kiếm trong CSDL cục bộ
    local_queryset = TaiLieuHocTap.objects.filter(
        Q(nhan_de__icontains=search_term) | Q(tac_gia__icontains=search_term)
    )[:50]
    for item in local_queryset:
        found_pks.add(item.pk)

    # Bước 2: Gọi API bên ngoài để tìm kiếm
    API_URL = 'http://172.16.2.92:8000/search' # Địa chỉ API nội bộ
    params = {'keyword': search_term, 'limit': 50}
    
    try:
        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()
        api_results = response.json()

        # Bước 3: Đồng bộ kết quả từ API vào CSDL cục bộ
        for item in api_results:
            if not item.get('bib_id'):
                continue
            
            obj, created = TaiLieuHocTap.objects.update_or_create(
                bib_id=item.get('bib_id'),
                defaults={ 'nhan_de': item.get('nhan_de'), 'tac_gia': item.get('tac_gia'), ... }
            )
            found_pks.add(obj.pk)
            
    except requests.exceptions.RequestException as e:
        print(f"API search failed: {e}") # Ghi log lỗi nhưng vẫn tiếp tục

    # Bước 4: Truy vấn tất cả kết quả (cục bộ + vừa đồng bộ) và trả về
    final_queryset = TaiLieuHocTap.objects.filter(pk__in=list(found_pks))
    results = [
        {'id': tl.pk, 'text': f"{tl.nhan_de} ({tl.tac_gia}, {tl.nam_xuat_ban or 'N/A'})"}
        for tl in final_queryset
    ]
    
    return JsonResponse({'results': results})
```
**Phân tích:**
- **Tích hợp hệ thống:** Thể hiện khả năng kết nối và lấy dữ liệu từ một service/API khác trong mạng nội bộ.
- **Đồng bộ dữ liệu:** Sử dụng phương thức `update_or_create` của Django ORM, một cách rất hiệu quả để thêm mới hoặc cập nhật dữ liệu từ nguồn bên ngoài mà không tạo ra bản ghi trùng lặp.
- **Thiết kế linh hoạt:** Kể cả khi API ngoài gặp lỗi, chức năng vẫn có thể trả về kết quả tìm thấy trong CSDL cục bộ, tăng tính ổn định cho hệ thống.
- **Hiệu năng:** Sử dụng `set` để quản lý các primary key tìm thấy, đảm bảo không có kết quả trùng lặp và tối ưu cho việc truy vấn cuối cùng.

---
**KẾT LUẬN**

Mã nguồn backend của hệ thống CURHUB được phát triển một cách có cấu trúc, tuân thủ các best practice của Django. Logic nghiệp vụ được tách biệt rõ ràng, dễ dàng cho việc kiểm thử, bảo trì và mở rộng. Việc áp dụng các tính năng mạnh mẽ của Django ORM và hệ thống xác thực giúp đảm bảo hệ thống hoạt động hiệu quả, an toàn và ổn định.
