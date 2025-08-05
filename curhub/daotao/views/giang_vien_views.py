from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import GiangVien, PhanCongGiangDay, ChuongTrinhDaoTao, ChiTietHocPhanTrongCTDT
from ..forms import GiangVienForm, PhanCongForm

from django.core.paginator import Paginator
from django.db.models import Q, Count, Exists, OuterRef
from django.db import models
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods

@login_required
@permission_required('daotao.view_giangvien', raise_exception=True)
def danh_sach_giang_vien(request):
    giang_vien_list = GiangVien.objects.annotate(
        so_ctdt_tham_gia=Count('cac_phan_cong__chi_tiet_hoc_phan__chuong_trinh_dao_tao', distinct=True)
    ).order_by('ten', 'ho')

    query_search = request.GET.get('q', '')
    if query_search:
        giang_vien_list = giang_vien_list.filter(
            Q(ho__icontains=query_search) |
            Q(ten__icontains=query_search) |
            Q(ma_can_bo__icontains=query_search) |
            Q(email__icontains=query_search)
        )

    paginator = Paginator(giang_vien_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'page_title': 'Danh sách Giảng viên',
        'query_search': query_search,
    }
    return render(request, 'daotao/danh_sach_giang_vien.html', context)

@login_required
@permission_required('daotao.change_chuongtrinhdaotao', raise_exception=True)
def quan_ly_giang_vien_ctdt(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    
    # Lấy danh sách các giảng viên đã được phân công trong CTĐT này
    giang_vien_da_phan_cong_subquery = PhanCongGiangDay.objects.filter(
        chi_tiet_hoc_phan__chuong_trinh_dao_tao=ctdt
    ).values('giang_vien_id')

    # Annotate các giảng viên để biết ai đã ở trong CTĐT và ai chưa
    giang_vien_list = GiangVien.objects.annotate(
        is_in_ctdt=Exists(
            PhanCongGiangDay.objects.filter(
                giang_vien_id=OuterRef('pk'),
                chi_tiet_hoc_phan__chuong_trinh_dao_tao_id=pk_ctdt
            )
        )
    ).order_by('-is_in_ctdt', 'ten', 'ho')

    query_search = request.GET.get('q', '')
    if query_search:
        giang_vien_list = giang_vien_list.filter(
            Q(ho__icontains=query_search) |
            Q(ten__icontains=query_search) |
            Q(ma_can_bo__icontains=query_search)
        )

    paginator = Paginator(giang_vien_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'ctdt': ctdt,
        'page_obj': page_obj,
        'page_title': f'Quản lý Giảng viên cho CTĐT: {ctdt.ten_nganh_ctdt}',
        'query_search': query_search,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'daotao/partials/_quan_ly_giang_vien_list.html', context)

    return render(request, 'daotao/quan_ly_giang_vien_ctdt.html', context)

@login_required
@require_http_methods(["POST"])
@permission_required('daotao.change_chuongtrinhdaotao', raise_exception=True)
def cap_nhat_giang_vien_ctdt(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    giang_vien_pk = request.POST.get('giang_vien_pk')
    action = request.POST.get('action')

    if not giang_vien_pk or not action:
        return JsonResponse({'status': 'error', 'message': 'Dữ liệu không hợp lệ.'}, status=400)

    giang_vien = get_object_or_404(GiangVien, pk=giang_vien_pk)
    is_draft = ctdt.trang_thai == 'DRAFT'

    if action == 'add':
        if not is_draft:
            return JsonResponse({'status': 'error', 'message': 'Chỉ có thể thêm giảng viên khi CTĐT ở trạng thái "Bản nháp".'}, status=403)
        
        # Create a default teaching assignment for the lecturer to persist the assignment
        # Assign to the first course in the program or create a placeholder if no courses exist
        first_course = ChiTietHocPhanTrongCTDT.objects.filter(chuong_trinh_dao_tao=ctdt).first()
        if first_course:
            PhanCongGiangDay.objects.create(
                giang_vien=giang_vien,
                chi_tiet_hoc_phan=first_course,
                vai_tro=PhanCongGiangDay.VAI_TRO_CHOICES[0][0]  # Default role, e.g., first choice
            )
        else:
            # No courses in program, just create an assignment with null course (if allowed)
            # Or skip assignment creation
            pass

        message = f"Đã thêm giảng viên {giang_vien.ho_ten} vào chương trình đào tạo."

        # Re-fetch the lecturer with updated assignments to render the list partial
        giang_vien_updated = GiangVien.objects.prefetch_related(
            models.Prefetch(
                'cac_phan_cong',
                queryset=PhanCongGiangDay.objects.filter(chi_tiet_hoc_phan__chuong_trinh_dao_tao=ctdt)
                                                   .select_related('chi_tiet_hoc_phan__hoc_phan'),
                to_attr='phan_cong_trong_ctdt'
            )
        ).get(pk=giang_vien_pk)

        context = {
            'giang_vien_da_tham_gia': [giang_vien_updated],
            'ctdt': ctdt,
            'is_draft': is_draft
        }
        lecturer_html = render_to_string('daotao/partials/_giang_vien_da_tham_gia_list.html', context, request=request)

    elif action == 'remove':
        # This action will remove all assignments for this lecturer in this CTDT
        PhanCongGiangDay.objects.filter(
            giang_vien=giang_vien,
            chi_tiet_hoc_phan__chuong_trinh_dao_tao=ctdt
        ).delete()
        message = f"Đã xóa tất cả phân công của giảng viên {giang_vien.ho_ten} khỏi chương trình."
        
        # Render the HTML for the newly available lecturer
        context = {
            'gv': giang_vien,
            'is_draft': is_draft,
            'ctdt': ctdt
        }
        lecturer_html = render_to_string('daotao/partials/_giang_vien_chua_tham_gia_list.html', context, request=request)

    else:
        return JsonResponse({'status': 'error', 'message': 'Hành động không hợp lệ.'}, status=400)

    return JsonResponse({
        'status': 'success', 
        'message': message, 
        'lecturer_html': lecturer_html,
        'gv_name': giang_vien.ho_ten
    })

@login_required
def load_giang_vien_tab(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    # This view will just render the container partial.
    # The actual lists will be populated by another API call from the frontend JS.
    return render(request, 'daotao/partials/_quan_ly_giang_vien_tab.html', {'ctdt': ctdt})
