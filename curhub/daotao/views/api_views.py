from django.db import models
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.db.models import Q, Prefetch
from ..models import (
    HocPhan, ChuongTrinhDaoTao,
    GiangVien, PhanCongGiangDay,
    DeCuongHocPhan, DanhMucKienThuc, MucTieuDaoTao, ChiTietHocPhanTrongCTDT
)
from ..forms import MucTieuDaoTaoForm

# API views will be moved here from views.py

@login_required
@require_http_methods(["POST"])
def update_chi_tiet_hoc_phan_inline(request):
    pk = request.POST.get('pk')
    name = request.POST.get('field') # Changed 'name' to 'field' to match JS
    value = request.POST.get('value')

    if not pk:
        return JsonResponse({'status': 'error', 'message': 'Thiếu thông tin "pk" của chi tiết học phần.'}, status=400)
    if name is None:
        return JsonResponse({'status': 'error', 'message': 'Thiếu thông tin "field" để cập nhật.'}, status=400)

    try:
        chi_tiet_hp = get_object_or_404(ChiTietHocPhanTrongCTDT, pk=pk)
        ctdt = chi_tiet_hp.chuong_trinh_dao_tao

        if ctdt.trang_thai != 'DRAFT':
            return JsonResponse({'status': 'error', 'message': "Chỉ có thể chỉnh sửa khi CTĐT ở trạng thái 'Bản nháp'."}, status=403)

        allowed_fields = [
            'la_bat_buoc', 'hoc_ky_du_kien', 'danh_muc_kien_thuc',
            'tin_chi_ly_thuyet_apdung', 'tin_chi_thuc_hanh_apdung',
            'so_gio_ly_thuyet_apdung', 'so_gio_thuc_hanh_apdung',
            'so_gio_tu_hoc_apdung', 'so_tiet_ly_thuyet_online'
        ]

        if name not in allowed_fields:
            return JsonResponse({'status': 'error', 'message': f'Trường "{name}" không được phép chỉnh sửa inline.'}, status=400)

        if name == 'la_bat_buoc':
            processed_value = (value == 'True')
            setattr(chi_tiet_hp, name, processed_value)
        elif name == 'danh_muc_kien_thuc':
            if value:
                processed_value = get_object_or_404(DanhMucKienThuc, pk=int(value))
            else:
                processed_value = None
            setattr(chi_tiet_hp, name, processed_value)
        else:
            field = ChiTietHocPhanTrongCTDT._meta.get_field(name)
            internal_type = field.get_internal_type()
            if internal_type in ('PositiveIntegerField', 'IntegerField', 'FloatField', 'DecimalField'):
                if value == '' or value is None:
                    processed_value = None
                else:
                    try:
                        float_value = float(value)
                        if internal_type in ('PositiveIntegerField', 'IntegerField'):
                            if float_value < 0 and internal_type == 'PositiveIntegerField':
                                 return JsonResponse({'status': 'error', 'message': f'Giá trị cho "{name}" không thể là số âm.'}, status=400)
                            processed_value = round(float_value)
                        else:
                            processed_value = float_value
                    except (ValueError, TypeError):
                        return JsonResponse({'status': 'error', 'message': f'Giá trị "{value}" không hợp lệ cho trường số.'}, status=400)
                setattr(chi_tiet_hp, name, processed_value)
            else:
                 setattr(chi_tiet_hp, name, value)

        chi_tiet_hp.full_clean()
        chi_tiet_hp.save()

        return JsonResponse({'status': 'success', 'message': 'Cập nhật thành công!'})

    except ChiTietHocPhanTrongCTDT.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Không tìm thấy học phần trong CTĐT.'}, status=404)
    except ValidationError as e:
        return JsonResponse({'status': 'error', 'message': 'Dữ liệu không hợp lệ.', 'errors': e.message_dict}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Đã có lỗi xảy ra: {e}'}, status=500)

def update_muc_tieu_dao_tao_inline(request):
    pass

@login_required
@require_http_methods(["POST"])
def api_them_po(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    if ctdt.trang_thai != 'DRAFT':
        return JsonResponse({'status': 'error', 'message': "Chỉ có thể thêm khi CTĐT ở trạng thái 'Bản nháp'."}, status=403)

    form = MucTieuDaoTaoForm(request.POST)
    if form.is_valid():
        po = form.save(commit=False)
        po.chuong_trinh_dao_tao = ctdt
        po.save()
        return JsonResponse({'status': 'success', 'message': 'Đã thêm Mục tiêu Đào tạo thành công!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Dữ liệu không hợp lệ.', 'errors': form.errors}, status=400)

@login_required
@require_http_methods(["POST"])
def sua_muc_tieu_dao_tao(request, pk_po):
    po = get_object_or_404(MucTieuDaoTao, pk=pk_po)
    ctdt = po.chuong_trinh_dao_tao

    if ctdt.trang_thai != 'DRAFT':
        return JsonResponse({'status': 'error', 'message': "Chỉ có thể sửa khi CTĐT ở trạng thái 'Bản nháp'."}, status=403)

    form = MucTieuDaoTaoForm(request.POST, instance=po)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success', 'message': 'Đã cập nhật Mục tiêu Đào tạo thành công!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Dữ liệu không hợp lệ.', 'errors': form.errors}, status=400)

@login_required
def api_get_po_details(request, pk_po):
    """
    API endpoint to get details for a specific MucTieuDaoTao (PO).
    """
    po = get_object_or_404(MucTieuDaoTao, pk=pk_po)
    data = {
        'pk': po.pk,
        'ma_muc_tieu': po.ma_muc_tieu,
        'noi_dung': po.noi_dung,
    }
    return JsonResponse(data)

def api_them_plo(request, pk_ctdt):
    pass

def api_sua_plo(request, pk_cdr):
    pass

def api_get_plo_details(request, pk_cdr):
    pass

def get_nganh_dao_tao_options(request):
    pass

def get_don_vi_dao_tao_options(request):
    pass

def search_hoc_phan_api(request):
    pass

def search_hoc_phan_in_ctdt_api(request, pk_ctdt):
    pass

def get_hoc_phan_details(request, pk_hoc_phan):
    pass

def api_get_de_cuong_chi_tiet(request, pk_hoc_phan):
    pass

def api_program_flowchart_data(request, pk_ctdt):
    """
    API endpoint to provide data for rendering a program flowchart.
    Returns nodes (courses) and edges (prerequisites) in the format
    expected by the frontend JavaScript.
    """
    try:
        ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
        chi_tiet_hps = ChiTietHocPhanTrongCTDT.objects.filter(
            chuong_trinh_dao_tao=ctdt
        ).select_related('hoc_phan', 'danh_muc_kien_thuc').prefetch_related('hoc_phan_tien_quyet')

        nodes = []
        edges = []

        for chi_tiet_hp in chi_tiet_hps:
            nodes.append({
                'id': f'hp-{chi_tiet_hp.pk}',  # Use a prefix to ensure valid Mermaid ID
                'original_id': chi_tiet_hp.hoc_phan.ma_hoc_phan,
                'name': chi_tiet_hp.hoc_phan.ten_hoc_phan,
                'tin_chi': chi_tiet_hp.tong_so_tin_chi_apdung,
                'khoi_kien_thuc': chi_tiet_hp.danh_muc_kien_thuc.ten_danh_muc if chi_tiet_hp.danh_muc_kien_thuc else '',
                'semester': chi_tiet_hp.hoc_ky_du_kien,
            })

            for tien_quyet in chi_tiet_hp.hoc_phan_tien_quyet.all():
                edges.append({
                    'source': f'hp-{tien_quyet.pk}',
                    'target': f'hp-{chi_tiet_hp.pk}',
                    'type': 'tienquyet' # 'songhanh' can be added later if needed
                })

        return JsonResponse({'nodes': nodes, 'edges': edges})

    except ChuongTrinhDaoTao.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Không tìm thấy chương trình đào tạo.'}, status=404)
    except Exception as e:
        # It's good practice to log the exception for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in flowchart data API: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': f'Đã có lỗi xảy ra khi tạo dữ liệu sơ đồ: {e}'}, status=500)

def api_search_giang_vien_chua_tham_gia(request, pk_ctdt):
    """
    API endpoint to search for lecturers who are not yet assigned to any course in a specific CTDT.
    Returns an HTML snippet.
    """
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    search_term = request.GET.get('q', '')

    # Get IDs of lecturers already participating in the program
    tham_gia_pks = PhanCongGiangDay.objects.filter(
        chi_tiet_hoc_phan__chuong_trinh_dao_tao=ctdt
    ).values_list('giang_vien_id', flat=True).distinct()

    # Query for lecturers not in the program
    giang_vien_qs = GiangVien.objects.filter(trang_thai_lam_viec='Đang làm việc').exclude(pk__in=tham_gia_pks).order_by('ten', 'ho')

    if search_term:
        giang_vien_qs = giang_vien_qs.filter(
            Q(ho_ten__icontains=search_term) |
            Q(ma_can_bo__icontains=search_term) |
            Q(email__icontains=search_term)
        )
    
    context = {
        'giang_vien_chua_tham_gia': giang_vien_qs[:50],  # Limit results for performance
        'ctdt': ctdt,
        'is_draft': ctdt.trang_thai == 'DRAFT'
    }
    return render(request, 'daotao/partials/_giang_vien_chua_tham_gia_list.html', context)

def api_get_giang_vien_da_tham_gia(request, pk_ctdt):
    """
    API endpoint to get lecturers who are already assigned to at least one course in a specific CTDT.
    Returns an HTML snippet.
    """
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    search_term = request.GET.get('q', '')

    # Get lecturers who have at least one assignment in this CTDT
    giang_vien_qs = GiangVien.objects.filter(
        trang_thai_lam_viec='Đang làm việc',
        cac_phan_cong__chi_tiet_hoc_phan__chuong_trinh_dao_tao=ctdt
    ).distinct().prefetch_related(
        Prefetch(
            'cac_phan_cong',
            queryset=PhanCongGiangDay.objects.filter(chi_tiet_hoc_phan__chuong_trinh_dao_tao=ctdt)
                                               .select_related('chi_tiet_hoc_phan__hoc_phan'),
            to_attr='phan_cong_trong_ctdt'
        )
    ).order_by('ten', 'ho')

    if search_term:
        giang_vien_qs = giang_vien_qs.filter(
            Q(ho_ten__icontains=search_term) |
            Q(ma_can_bo__icontains=search_term) |
            Q(email__icontains=search_term)
        )

    context = {
        'giang_vien_da_tham_gia': giang_vien_qs,
        'ctdt': ctdt,
        'is_draft': ctdt.trang_thai == 'DRAFT'
    }
    return render(request, 'daotao/partials/_giang_vien_da_tham_gia_list.html', context)


from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def api_get_phan_cong_form(request, pk_ctdt, pk_gv):
    """
    Return the teaching assignment form data for a lecturer in a training program.
    Includes all courses in the program and the lecturer's current assignments with roles.
    """
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    giang_vien = get_object_or_404(GiangVien, pk=pk_gv)

    # All courses in the program
    chi_tiet_hps = ChiTietHocPhanTrongCTDT.objects.filter(chuong_trinh_dao_tao=ctdt).select_related('hoc_phan')

    # Current assignments of the lecturer in this program
    assignments = PhanCongGiangDay.objects.filter(
        giang_vien=giang_vien,
        chi_tiet_hoc_phan__chuong_trinh_dao_tao=ctdt
    ).select_related('chi_tiet_hoc_phan')

    # Map course id to assignment
    assignment_map = {a.chi_tiet_hoc_phan_id: a for a in assignments}

    # Prepare data for each course: include role if assigned
    data = []
    for cthp in chi_tiet_hps:
        assigned = cthp.pk in assignment_map
        role = assignment_map[cthp.pk].vai_tro if assigned else None
        data.append({
            'course_id': cthp.pk,
            'course_name': cthp.hoc_phan.ten_hoc_phan,
            'assigned': assigned,
            'role': role,
        })

    context = {
        'giang_vien': giang_vien,
        'ctdt': ctdt,
        'assignments': data,
        'roles': PhanCongGiangDay.VAI_TRO_CHOICES,
    }
    html = render_to_string('daotao/partials/_phan_cong_giang_day_form.html', context, request=request)
    return JsonResponse({'status': 'success', 'html': html})


@csrf_exempt
def api_luu_phan_cong(request, pk_ctdt):
    """
    Save teaching assignments for a lecturer in a training program.
    Expects JSON payload with lecturer id, list of course assignments with roles.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Phương thức không hợp lệ.'}, status=405)

    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)

    try:
        data = json.loads(request.body)
        giang_vien_id = data.get('giang_vien_id')
        assignments = data.get('assignments', [])  # List of dicts: {course_id, role}

        giang_vien = get_object_or_404(GiangVien, pk=giang_vien_id)

        if ctdt.trang_thai != 'DRAFT':
            return JsonResponse({'status': 'error', 'message': 'Chỉ có thể cập nhật khi CTĐT ở trạng thái "Bản nháp".'}, status=403)

        # Remove all existing assignments for this lecturer in this program
        PhanCongGiangDay.objects.filter(
            giang_vien=giang_vien,
            chi_tiet_hoc_phan__chuong_trinh_dao_tao=ctdt
        ).delete()

        # Add new assignments
        for assign in assignments:
            course_id = assign.get('course_id')
            role = assign.get('role')
            if course_id is None or role is None:
                continue
            cthp = ChiTietHocPhanTrongCTDT.objects.filter(pk=course_id, chuong_trinh_dao_tao=ctdt).first()
            if cthp:
                PhanCongGiangDay.objects.create(
                    giang_vien=giang_vien,
                    chi_tiet_hoc_phan=cthp,
                    vai_tro=role
                )

        return JsonResponse({'status': 'success', 'message': 'Lưu phân công giảng dạy thành công.'})

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Dữ liệu gửi lên không hợp lệ.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Đã có lỗi xảy ra: {e}'}, status=500)
