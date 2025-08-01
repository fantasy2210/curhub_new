from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q, OuterRef, Exists, Case, When, Value, IntegerField, Count
from django.db import models
from django.contrib import messages
from django.utils import timezone
from .forms import (
    NganhDaoTaoForm, ChuongTrinhDaoTaoModelForm, HocPhanLibModelForm,
    ChiTietHocPhanTrongCTDTModelForm, DonViDaoTaoForm, MucTieuDaoTaoFormSet,
    ChuanDauRaFormSet, UploadHocPhanCTDTForm, ChuanDauRaForm, MucTieuDaoTaoForm,
    DanhMucKienThucForm, DeCuongHocPhanForm, ChuanDauRaHocPhanFormSet,
    NoiDungChiTietDeCuongFormSet, HinhThucDanhGiaFormSet, DoiSanhCTDTForm
)
from .models import (
    NganhDaoTao, ChuongTrinhDaoTao, HocPhan, ChiTietHocPhanTrongCTDT,
    LichSuThayDoiCTDT, DonViDaoTao, MucTieuDaoTao, ChuanDauRa, DanhMucKienThuc,
    DeCuongHocPhan, NoiDungChiTietDeCuong, HinhThucDanhGia, ChuanDauRaHocPhan,
    GiangVien, PhanCongGiangDay
)
from django.db import transaction
from django.template.loader import render_to_string
import pandas as pd
import io
import json

def index(request):
    return redirect('daotao:danh_sach_ctdt')

def them_nganh_dao_tao(request):
    if request.method == 'POST':
        form = NganhDaoTaoForm(request.POST)
        if form.is_valid():
            form.save()
            form = NganhDaoTaoForm()
            return render(request, 'daotao/them_nganh.html', {
                'form': form,
                'message': 'Đã thêm ngành đào tạo thành công!'
            })
    else:
        form = NganhDaoTaoForm()
    context = {'form': form}
    return render(request, 'daotao/them_nganh.html', context)

@login_required
@permission_required('daotao.add_chuongtrinhdaotao', raise_exception=True)
def them_chuong_trinh_dao_tao(request):
    if request.method == 'POST':
        form = ChuongTrinhDaoTaoModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã thêm Chương trình Đào tạo thành công!')
            form = ChuongTrinhDaoTaoModelForm() # Reset form for new entry
        else:
            messages.error(request, 'Có lỗi xảy ra khi thêm Chương trình Đào tạo. Vui lòng kiểm tra lại các trường.')
    else:
        form = ChuongTrinhDaoTaoModelForm()
    context = {
        'form': form,
        'page_title': 'Thêm Chương Trình Đào Tạo Mới'
    }
    return render(request, 'daotao/them_ctdt.html', context)

@login_required
@permission_required('daotao.view_chuongtrinhdaotao', raise_exception=True)
def danh_sach_ctdt(request):
    chuong_trinh_list = ChuongTrinhDaoTao.objects.prefetch_related('hoc_phan_trong_chuong_trinh').order_by('-ngay_cap_nhat')
    query_search = request.GET.get('q', '')
    trang_thai_filter = request.GET.get('trang_thai', '')
    don_vi_filter = request.GET.get('don_vi', '')
    if query_search:
        chuong_trinh_list = chuong_trinh_list.filter(
            Q(ten_nganh_ctdt__icontains=query_search) |
            Q(ma_nganh_ctdt__icontains=query_search)
        )
    if trang_thai_filter:
        chuong_trinh_list = chuong_trinh_list.filter(trang_thai=trang_thai_filter)
    if don_vi_filter:
        chuong_trinh_list = chuong_trinh_list.filter(don_vi_quan_ly__id=don_vi_filter)
    paginator = Paginator(chuong_trinh_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'TRANG_THAI_CHOICES': ChuongTrinhDaoTao.TRANG_THAI_CHOICES,
        'don_vi_list': DonViDaoTao.objects.all(),
        'query_search': query_search,
        'trang_thai_filter': trang_thai_filter,
        'don_vi_filter': don_vi_filter,
    }
    return render(request, 'daotao/danh_sach_ctdt.html', context)

@login_required
@permission_required('daotao.view_chuongtrinhdaotao', raise_exception=True)
def chi_tiet_ctdt(request, pk_ctdt):
    chuong_trinh = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    
    # Lấy và sắp xếp danh sách học phần
    hoc_phan_list = ChiTietHocPhanTrongCTDT.objects.filter(
        chuong_trinh_dao_tao=chuong_trinh
    ).select_related('hoc_phan', 'danh_muc_kien_thuc').order_by('hoc_ky_du_kien', 'hoc_phan__ma_hoc_phan')

    # Nhóm học phần theo khối kiến thức
    hoc_phan_theo_khoi = {}
    hoc_phan_chua_xep_khoi = []
    tong_tin_chi_toan_ctdt = 0

    for hp in hoc_phan_list:
        tong_tin_chi_toan_ctdt += hp.tong_so_tin_chi_apdung
        khoi = hp.danh_muc_kien_thuc
        if khoi is not None:
            # Sử dụng khoi.ten_danh_muc làm key để sắp xếp theo alphabet sau này
            if khoi.ten_danh_muc not in hoc_phan_theo_khoi:
                hoc_phan_theo_khoi[khoi.ten_danh_muc] = {
                    'id': khoi.id,
                    'hoc_phan_list': [],
                    'tong_tin_chi': 0
                }
            hoc_phan_theo_khoi[khoi.ten_danh_muc]['hoc_phan_list'].append(hp)
            hoc_phan_theo_khoi[khoi.ten_danh_muc]['tong_tin_chi'] += hp.tong_so_tin_chi_apdung
        else:
            hoc_phan_chua_xep_khoi.append(hp)

    # Sắp xếp lại dict theo key (ten_danh_muc)
    hoc_phan_theo_khoi = dict(sorted(hoc_phan_theo_khoi.items()))

    # Chuẩn bị dữ liệu cho biểu đồ tròn
    pie_chart_labels = list(hoc_phan_theo_khoi.keys())
    pie_chart_data = [details['tong_tin_chi'] for details in hoc_phan_theo_khoi.values()]

    muc_tieu_dao_tao_ctdt = MucTieuDaoTao.objects.filter(chuong_trinh_dao_tao=chuong_trinh).order_by('ma_muc_tieu')
    
    # Custom ordering for PLOs
    custom_order = Case(
        When(loai_cdr='KT', then=Value(0)),
        When(loai_cdr='KN', then=Value(1)),
        When(loai_cdr='TD', then=Value(2)),
        default=Value(3),
        output_field=IntegerField(),
    )
    chuan_dau_ra_ctdt = ChuanDauRa.objects.filter(
        chuong_trinh_dao_tao=chuong_trinh
    ).prefetch_related('dap_ung_muc_tieu').annotate(
        custom_order=custom_order
    ).order_by('custom_order', 'ma_cdr')

    # Group PLOs by type for the matrix display, maintaining the custom order
    plo_groups = {}
    # Define the desired order of groups
    group_order = ['Về kiến thức', 'Về kỹ năng', 'Về thái độ/Năng lực tự chủ và trách nhiệm', 'Khác']
    for group_name in group_order:
        plo_groups[group_name] = []

    for plo in chuan_dau_ra_ctdt:
        group_name = plo.get_loai_cdr_display()
        # If group_name is None or not in our predefined list, default to 'Khác'
        if group_name not in plo_groups:
            group_name = 'Khác'
        
        # Create a set of related PO pks for quick lookup in the template
        plo.related_pos_pks = set(po.pk for po in plo.dap_ung_muc_tieu.all())
        plo_groups[group_name].append(plo)
    
    # Filter out empty groups
    plo_groups = {k: v for k, v in plo_groups.items() if v}

    # Add forms for modals
    po_form = MucTieuDaoTaoForm()
    plo_form = ChuanDauRaForm(ctdt=chuong_trinh)

    # D. Kế hoạch giảng dạy (Tentative Teaching Plan)
    hoc_phan_theo_hoc_ky = {}
    hoc_phan_chua_phan_bo = []
    for hp in hoc_phan_list:
        hoc_ky = hp.hoc_ky_du_kien
        if hoc_ky:
            if hoc_ky not in hoc_phan_theo_hoc_ky:
                hoc_phan_theo_hoc_ky[hoc_ky] = {
                    'hoc_phan_list': [],
                    'tong_tin_chi': 0
                }
            hoc_phan_theo_hoc_ky[hoc_ky]['hoc_phan_list'].append(hp)
            hoc_phan_theo_hoc_ky[hoc_ky]['tong_tin_chi'] += hp.tong_so_tin_chi_apdung
        else:
            hoc_phan_chua_phan_bo.append(hp)
    
    # Sắp xếp dict theo key (học kỳ)
    hoc_phan_theo_hoc_ky = dict(sorted(hoc_phan_theo_hoc_ky.items()))

    context = {
        'ctdt': chuong_trinh,
        'page_title': f"Chi tiết CTĐT: {chuong_trinh.ten_nganh_ctdt}",
        'hoc_phan_theo_khoi': hoc_phan_theo_khoi,
        'hoc_phan_chua_xep_khoi': hoc_phan_chua_xep_khoi,
        'tong_tin_chi_toan_ctdt': tong_tin_chi_toan_ctdt,
        'pie_chart_labels_json': json.dumps(pie_chart_labels),
        'pie_chart_data_json': json.dumps(pie_chart_data),
        'muc_tieu_dao_tao_ctdt': muc_tieu_dao_tao_ctdt,
        'chuan_dau_ra_ctdt': chuan_dau_ra_ctdt, # Keep for simple list if needed elsewhere
        'plo_groups': plo_groups,
        'is_draft': chuong_trinh.trang_thai == 'DRAFT',
        'po_form': po_form,
        'plo_form': plo_form,
        'lich_su_thay_doi': LichSuThayDoiCTDT.objects.filter(chuong_trinh_dao_tao=chuong_trinh),
        # Dữ liệu cho Kế hoạch giảng dạy
        'hoc_phan_theo_hoc_ky': hoc_phan_theo_hoc_ky,
        'hoc_phan_chua_phan_bo': hoc_phan_chua_phan_bo,
    }
    return render(request, 'daotao/chi_tiet_ctdt.html', context)

@login_required
@permission_required('daotao.change_chuongtrinhdaotao', raise_exception=True)
def sua_ctdt(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    if ctdt.trang_thai != 'DRAFT':
        messages.error(request, "Chỉ có thể sửa CTĐT ở trạng thái 'Bản nháp'.")
        return redirect('daotao:chi_tiet_ctdt', pk_ctdt=pk_ctdt)
    if request.method == 'POST':
        form = ChuongTrinhDaoTaoModelForm(request.POST, instance=ctdt)
        po_formset = MucTieuDaoTaoFormSet(request.POST, instance=ctdt, prefix='po')
        plo_formset = ChuanDauRaFormSet(request.POST, instance=ctdt, prefix='plo')
        if form.is_valid() and po_formset.is_valid() and plo_formset.is_valid():
            change_details = []
            if form.changed_data:
                for field_name in form.changed_data:
                    old_value = form.initial.get(field_name, 'N/A')
                    new_value = form.cleaned_data.get(field_name, 'N/A')
                    field_label = form.fields[field_name].label or field_name
                    change_details.append(f"- Thay đổi '{field_label}' từ '{old_value}' thành '{new_value}'")
            
            # You can add more detailed logging for formsets if needed
            if po_formset.has_changed():
                change_details.append("- Có thay đổi trong Mục tiêu Đào tạo (PO).")
            if plo_formset.has_changed():
                change_details.append("- Có thay đổi trong Chuẩn Đầu Ra (PLO).")

            if not change_details:
                messages.info(request, "Không có thay đổi nào được thực hiện.")
                return redirect('daotao:chi_tiet_ctdt', pk_ctdt=ctdt.id)

            try:
                with transaction.atomic():
                    updated_ctdt = form.save()
                    po_formset.save()
                    plo_formset.save()

                    # Create a history log entry
                    LichSuThayDoiCTDT.objects.create(
                        chuong_trinh_dao_tao=updated_ctdt,
                        nguoi_thuc_hien=request.user,
                        hanh_dong="Cập nhật",
                        chi_tiet_thay_doi="\n".join(change_details)
                    )
                messages.success(request, "Đã cập nhật Chương trình Đào tạo và các mục liên quan thành công!")
                return redirect('daotao:chi_tiet_ctdt', pk_ctdt=updated_ctdt.id)
            except Exception as e:
                messages.error(request, f"Đã có lỗi xảy ra trong quá trình lưu: {e}")

        else:
            messages.error(request, "Có lỗi xảy ra khi cập nhật. Vui lòng kiểm tra lại các trường.")
    else:
        form = ChuongTrinhDaoTaoModelForm(instance=ctdt)
        po_formset = MucTieuDaoTaoFormSet(instance=ctdt, prefix='po')
        plo_formset = ChuanDauRaFormSet(instance=ctdt, prefix='plo')
    hoc_phan_trong_ctdt = ChiTietHocPhanTrongCTDT.objects.filter(
        chuong_trinh_dao_tao=ctdt
    ).order_by('hoc_ky_du_kien', 'hoc_phan__ma_hoc_phan')
    context = {
        'form': form,
        'ctdt': ctdt,
        'po_formset': po_formset,
        'plo_formset': plo_formset,
        'hoc_phan_trong_ctdt': hoc_phan_trong_ctdt,
        'page_title': f'Cập nhật Chương trình: {ctdt.ten_nganh_ctdt}'
    }
    return render(request, 'daotao/sua_ctdt.html', context)

@login_required
@permission_required('daotao.delete_chuongtrinhdaotao', raise_exception=True)
def xoa_ctdt(request, pk_ctdt):
    chuong_trinh_can_xoa = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    if request.method == 'POST':
        chuong_trinh_can_xoa.delete()
        messages.success(request, f"Đã xóa chương trình đào tạo '{chuong_trinh_can_xoa.ten_nganh_ctdt}' thành công.")
        return redirect('daotao:danh_sach_ctdt')
    context = {
        'ctdt': chuong_trinh_can_xoa,
        'page_title': f'Xác nhận Xóa CTĐT: {chuong_trinh_can_xoa.ten_nganh_ctdt}'
    }
    return render(request, 'daotao/xoa_ctdt_confirm.html', context)

@login_required
@permission_required('daotao.view_hocphan', raise_exception=True)
def danh_sach_hoc_phan(request):
    hoc_phan_list = HocPhan.objects.select_related('don_vi_quan_ly_goc').order_by('ma_hoc_phan')
    
    # Lấy các tham số từ query string
    query_search = request.GET.get('q', '')
    don_vi_filter = request.GET.get('don_vi', '')
    
    # Lọc theo query search
    if query_search:
        hoc_phan_list = hoc_phan_list.filter(
            Q(ma_hoc_phan__icontains=query_search) |
            Q(ten_hoc_phan__icontains=query_search)
        )
        
    # Lọc theo đơn vị quản lý
    if don_vi_filter:
        hoc_phan_list = hoc_phan_list.filter(don_vi_quan_ly_goc__id=don_vi_filter)

    paginator = Paginator(hoc_phan_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Lấy danh sách đơn vị để hiển thị trong bộ lọc
    don_vi_list = DonViDaoTao.objects.all()
    
    context = {
        'page_obj': page_obj,
        'page_title': 'Danh Sách Học Phần',
        'don_vi_list': don_vi_list,
        'query_search': query_search,
        'don_vi_filter': don_vi_filter,
    }
    return render(request, 'daotao/danh_sach_hoc_phan.html', context)


@login_required
def search_hoc_phan_api(request):
    search_term = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    ctdt_pk = request.GET.get('ctdt_pk')

    if ctdt_pk:
        try:
            # Search within the context of a specific CTDT
            ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=ctdt_pk)
            queryset = ChiTietHocPhanTrongCTDT.objects.filter(chuong_trinh_dao_tao=ctdt).order_by('hoc_phan__ma_hoc_phan')
            
            if search_term:
                queryset = queryset.filter(
                    Q(hoc_phan__ma_hoc_phan__icontains=search_term) |
                    Q(hoc_phan__ten_hoc_phan__icontains=search_term)
                )
        except ChuongTrinhDaoTao.DoesNotExist:
            return JsonResponse({'results': [], 'pagination': {'more': False}}, status=404)
    else:
        # Fallback to global search if no ctdt_pk is provided
        queryset = HocPhan.objects.all().order_by('ma_hoc_phan')
        if search_term:
            queryset = queryset.filter(
                Q(ma_hoc_phan__icontains=search_term) |
                Q(ten_hoc_phan__icontains=search_term)
            )

    paginator = Paginator(queryset, 30)  # 30 results per page
    try:
        hoc_phan_page = paginator.page(page)
    except PageNotAnInteger:
        hoc_phan_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        hoc_phan_page = paginator.page(paginator.num_pages)

    results = []
    for hoc_phan in hoc_phan_page:
        results.append({
            'id': hoc_phan.pk,
            'text': f"{hoc_phan.ma_hoc_phan} - {hoc_phan.ten_hoc_phan}"
        })

    return JsonResponse({
        'results': results,
        'pagination': {
            'more': hoc_phan_page.has_next()
        }
    })


@login_required
@permission_required('daotao.view_hocphan', raise_exception=True)
def chi_tiet_hoc_phan(request, pk_hoc_phan):
    hoc_phan = get_object_or_404(HocPhan, pk=pk_hoc_phan)
    de_cuong_list = DeCuongHocPhan.objects.filter(hoc_phan=hoc_phan).order_by('-ngay_ban_hanh')
    ctdt_list = ChiTietHocPhanTrongCTDT.objects.filter(hoc_phan=hoc_phan).select_related('chuong_trinh_dao_tao').order_by('chuong_trinh_dao_tao__ma_nganh_ctdt')
    context = {
        'hoc_phan': hoc_phan,
        'de_cuong_list': de_cuong_list,
        'ctdt_list': ctdt_list,
        'page_title': f'Chi tiết học phần: {hoc_phan.ten_hoc_phan}'
    }
    return render(request, 'daotao/chi_tiet_hoc_phan.html', context)

@login_required
@permission_required('daotao.can_manage_program_structure', raise_exception=True)
def them_hoc_phan_hang_loat(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    if request.method == 'GET' and request.GET.get('format') == 'datatables':
        try:
            draw = int(request.GET.get('draw', 1))
            start = int(request.GET.get('start', 0))
            length = int(request.GET.get('length', 10))
            search_ma_hp = request.GET.get('search_ma_hp', '')
            search_ten_hp = request.GET.get('search_ten_hp', '')
            search_don_vi_ql = request.GET.get('search_don_vi_ql', '')

            # Subquery to check if the HocPhan already exists in the current CTDT
            existing_hp_subquery = ChiTietHocPhanTrongCTDT.objects.filter(
                chuong_trinh_dao_tao=ctdt,
                hoc_phan=OuterRef('pk')
            )

            # Base queryset with optimizations
            queryset = HocPhan.objects.select_related('don_vi_quan_ly_goc').annotate(
                is_disabled=Exists(existing_hp_subquery)
            ).order_by('ma_hoc_phan')

            total_records = queryset.count()

            # Apply search filters
            if search_ma_hp:
                queryset = queryset.filter(ma_hoc_phan__icontains=search_ma_hp)
            if search_ten_hp:
                queryset = queryset.filter(ten_hoc_phan__icontains=search_ten_hp)
            if search_don_vi_ql:
                queryset = queryset.filter(don_vi_quan_ly_goc__pk=search_don_vi_ql)

            filtered_records = queryset.count()

            # Apply pagination
            paginated_queryset = queryset[start:start + length]

            data = []
            for hp in paginated_queryset:
                try:
                    # 'is_disabled' is now an attribute from the annotation
                    checkbox_html = f'''
                        <input type="checkbox" name="selected_hoc_phan" value="{hp.pk}" class="hoc-phan-checkbox"
                        {'disabled' if hp.is_disabled else ''} title="{'Học phần này đã có trong CTĐT' if hp.is_disabled else ''}">
                    '''
                    hoc_ky_input_html = f'<input type="number" name="hoc_ky" class="form-control form-control-sm" style="width: 60px;">'
                    don_vi_name = hp.don_vi_quan_ly_goc.ten_don_vi if hp.don_vi_quan_ly_goc else "N/A"
                    mo_ta_text = hp.mo_ta_hoc_phan or ""
                    mo_ta_display = mo_ta_text[:100] + '...' if len(mo_ta_text) > 100 else mo_ta_text
                    data.append([
                        checkbox_html,
                        hp.ma_hoc_phan,
                        hp.ten_hoc_phan,
                        hp.tong_so_tin_chi_goc,
                        don_vi_name,
                        mo_ta_display,
                        hoc_ky_input_html
                    ])
                except Exception as e:
                    error_message = f"Lỗi xử lý HP ID {hp.pk}: {str(e)}"
                    data.append([
                        f'<input type="checkbox" disabled title="{error_message}">',
                        hp.ma_hoc_phan,
                        hp.ten_hoc_phan,
                        "Lỗi",
                        "Lỗi",
                        error_message
                    ])

            response_data = {
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": filtered_records,
                "data": data
            }
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({"error": str(e), "data": [], "recordsFiltered": 0, "recordsTotal": 0}, status=500)
    if request.method == 'POST':
        selected_hoc_phan_pks = request.POST.getlist('selected_hoc_phan')
        hoc_ky_du_kien_default = request.POST.get('hoc_ky_du_kien_default')
        la_bat_buoc_default_str = request.POST.get('la_bat_buoc_default')
        success_count = 0
        error_count = 0
        errors = []
        try:
            hoc_ky_du_kien_default = int(hoc_ky_du_kien_default) if hoc_ky_du_kien_default else None
        except (ValueError, TypeError):
            hoc_ky_du_kien_default = None
        la_bat_buoc_default = None
        if la_bat_buoc_default_str == 'True':
            la_bat_buoc_default = True
        elif la_bat_buoc_default_str == 'False':
            la_bat_buoc_default = False
        for hp_pk in selected_hoc_phan_pks:
            try:
                if ChiTietHocPhanTrongCTDT.objects.filter(chuong_trinh_dao_tao=ctdt, hoc_phan_id=hp_pk).exists():
                    errors.append(f"Học phần PK '{hp_pk}' đã tồn tại.")
                    error_count += 1
                    continue
                hoc_phan_obj = HocPhan.objects.get(pk=hp_pk)
                chi_tiet_hp_data = {
                    'chuong_trinh_dao_tao': ctdt.pk,
                    'hoc_phan': hoc_phan_obj.pk,
                    'tin_chi_ly_thuyet_apdung': hoc_phan_obj.tin_chi_ly_thuyet_goc,
                    'tin_chi_thuc_hanh_apdung': hoc_phan_obj.tin_chi_thuc_hanh_goc,
                }
                hoc_ky = request.POST.get(f'hoc_ky_{hp_pk}')
                if hoc_ky:
                    chi_tiet_hp_data['hoc_ky_du_kien'] = int(hoc_ky)
                elif hoc_ky_du_kien_default is not None:
                    chi_tiet_hp_data['hoc_ky_du_kien'] = hoc_ky_du_kien_default
                if la_bat_buoc_default is not None:
                    chi_tiet_hp_data['la_bat_buoc'] = la_bat_buoc_default

                # Pass the full queryset of HocPhan to the form for validation
                form_instance = ChiTietHocPhanTrongCTDTModelForm(
                    data=chi_tiet_hp_data,
                    hoc_phan_queryset=HocPhan.objects.all()
                )
                if form_instance.is_valid():
                    # Create the instance without saving to the DB
                    chi_tiet_instance = form_instance.save(commit=False)
                    # Set the excluded fields
                    chi_tiet_instance.chuong_trinh_dao_tao = ctdt
                    chi_tiet_instance.hoc_phan = hoc_phan_obj
                    # Save the instance to the DB
                    chi_tiet_instance.save()
                    success_count += 1
                else:
                    error_count += 1
                    errors.append(f"Lỗi HP PK '{hp_pk}': {form_instance.errors.as_text()}")
            except Exception as e:
                error_count += 1
                errors.append(f"Lỗi không xác định với HP PK '{hp_pk}': {e}")
        if success_count > 0:
            messages.success(request, f"Đã thêm thành công {success_count} học phần.")
        if error_count > 0:
            messages.error(request, f"Có {error_count} lỗi: " + " | ".join(errors))
        return redirect(f"{reverse('daotao:chi_tiet_ctdt', kwargs={'pk_ctdt': ctdt.pk})}#hocphan-tab-pane")
    if not HocPhan.objects.exists():
        messages.warning(request, "Thư viện học phần trống. Vui lòng thêm học phần vào thư viện trước khi thực hiện chức năng này.")
    
    don_vi_list = DonViDaoTao.objects.all()
    context = {
        'ctdt': ctdt,
        'page_title': f'Thêm Học Phần Hàng Loạt cho CTĐT: {ctdt.ten_nganh_ctdt}',
        'don_vi_list': don_vi_list
    }
    return render(request, 'daotao/them_hoc_phan_hang_loat.html', context)

@login_required
@permission_required('daotao.add_chitiethocphantrongctdt', raise_exception=True)
def upload_hoc_phan_ctdt(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    if ctdt.trang_thai != 'DRAFT':
        messages.error(request, "Chỉ có thể upload học phần khi CTĐT ở trạng thái 'Bản nháp'.")
        return redirect('daotao:chi_tiet_ctdt', pk_ctdt=pk_ctdt)
    if request.method == 'POST':
        form = UploadHocPhanCTDTForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = None
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(io.TextIOWrapper(file.file, encoding='utf-8'))
                elif file.name.endswith('.xlsx'):
                    df = pd.read_excel(file.file)
                else:
                    messages.error(request, "Định dạng tệp không được hỗ trợ. Vui lòng tải lên tệp .xlsx hoặc .csv.")
                    return redirect('daotao:upload_hoc_phan_ctdt', pk_ctdt=pk_ctdt)
            except Exception as e:
                messages.error(request, f"Lỗi đọc tệp: {e}. Vui lòng kiểm tra định dạng và nội dung tệp.")
                return redirect('daotao:upload_hoc_phan_ctdt', pk_ctdt=pk_ctdt)
            if df is not None:
                success_count = 0
                error_count = 0
                errors = []
                column_mapping = {
                    'Mã học phần': 'ma_hoc_phan', 'Tên học phần': 'ten_hoc_phan', 'Tên học phần (TA)': 'ten_hoc_phan_tieng_anh',
                    'Tổng TC': 'tong_so_tin_chi_goc', 'TC LT': 'tin_chi_ly_thuyet_goc', 'TC TH': 'tin_chi_thuc_hanh_goc',
                    'Số giờ LT': 'so_gio_ly_thuyet_goc', 'Số giờ TH': 'so_gio_thuc_hanh_goc', 'Số giờ Tự học': 'so_gio_tu_hoc_goc',
                    'Đơn vị QL': 'don_vi_quan_ly_goc_ma', 'Mô tả HP': 'mo_ta_hoc_phan', 'Tài liệu': 'tai_lieu_hoc_tap',
                    'Điều kiện tiên quyết': 'dieu_kien_tien_quyet', 'Điều kiện song hành': 'dieu_kien_song_hanh',
                    'Học phần tương đương': 'hoc_phan_tuong_duong', 'Học phần thay thế': 'hoc_phan_thay_the',
                    'Ghi chú HP': 'ghi_chu_hoc_phan', 'Học kỳ dự kiến': 'hoc_ky_du_kien', 'Là bắt buộc': 'la_bat_buoc',
                    'TC LT áp dụng': 'tin_chi_ly_thuyet_apdung', 'TC TH áp dụng': 'tin_chi_thuc_hanh_apdung',
                    'Số giờ LT áp dụng': 'so_gio_ly_thuyet_apdung', 'Số giờ TH áp dụng': 'so_gio_thuc_hanh_apdung',
                    'Số giờ Tự học áp dụng': 'so_gio_tu_hoc_apdung', 'Số tiết LT online': 'so_tiet_ly_thuyet_online',
                    'Ghi chú chi tiết HP': 'ghi_chu_chi_tiet_hp',
                }
                df.rename(columns=column_mapping, inplace=True)
                required_cols = ['ma_hoc_phan', 'ten_hoc_phan', 'tong_so_tin_chi_goc']
                if not all(col in df.columns for col in required_cols):
                    missing_cols = [col for col in required_cols if col not in df.columns]
                    messages.error(request, f"Tệp thiếu các cột bắt buộc: {', '.join(missing_cols)}. Vui lòng kiểm tra template.")
                    return redirect('daotao:upload_hoc_phan_ctdt', pk_ctdt=pk_ctdt)
                with transaction.atomic():
                    for index, row in df.iterrows():
                        try:
                            ma_hoc_phan = row.get('ma_hoc_phan')
                            ten_hoc_phan = row.get('ten_hoc_phan')
                            if not ma_hoc_phan or not ten_hoc_phan:
                                errors.append(f"Dòng {index+2}: Mã học phần hoặc Tên học phần trống. Bỏ qua.")
                                error_count += 1
                                continue
                            don_vi_ql_ma = row.get('don_vi_quan_ly_goc_ma')
                            don_vi_ql_obj = None
                            if pd.notna(don_vi_ql_ma):
                                try:
                                    don_vi_ql_obj = DonViDaoTao.objects.get(ma_don_vi=str(don_vi_ql_ma).strip())
                                except DonViDaoTao.DoesNotExist:
                                    errors.append(f"Dòng {index+2} (HP: {ma_hoc_phan}): Mã đơn vị quản lý '{don_vi_ql_ma}' không tồn tại. Bỏ qua.")
                                    error_count += 1
                                    continue
                            hoc_phan_data = {
                                'ma_hoc_phan': ma_hoc_phan, 'ten_hoc_phan': ten_hoc_phan, 'ten_hoc_phan_tieng_anh': row.get('ten_hoc_phan_tieng_anh'),
                                'tong_so_tin_chi_goc': row.get('tong_so_tin_chi_goc'), 'tin_chi_ly_thuyet_goc': row.get('tin_chi_ly_thuyet_goc'),
                                'tin_chi_thuc_hanh_goc': row.get('tin_chi_thuc_hanh_goc'), 'so_gio_ly_thuyet_goc': row.get('so_gio_ly_thuyet_goc'),
                                'so_gio_thuc_hanh_goc': row.get('so_gio_thuc_hanh_goc'), 'so_gio_tu_hoc_goc': row.get('so_gio_tu_hoc_goc'),
                                'don_vi_quan_ly_goc': don_vi_ql_obj, 'mo_ta_hoc_phan': row.get('mo_ta_hoc_phan'),
                                'tai_lieu_hoc_tap': row.get('tai_lieu_hoc_tap'), 'dieu_kien_tien_quyet': row.get('dieu_kien_tien_quyet'),
                                'dieu_kien_song_hanh': row.get('dieu_kien_song_hanh'), 'hoc_phan_tuong_duong': row.get('hoc_phan_tuong_duong'),
                                'hoc_phan_thay_the': row.get('hoc_phan_thay_the'), 'ghi_chu_hoc_phan': row.get('ghi_chu_hoc_phan'),
                            }
                            hoc_phan_data = {k: (v if pd.notna(v) else None) for k, v in hoc_phan_data.items()}
                            hoc_phan_obj, created = HocPhan.objects.update_or_create(ma_hoc_phan=ma_hoc_phan, defaults=hoc_phan_data)
                            if ChiTietHocPhanTrongCTDT.objects.filter(chuong_trinh_dao_tao=ctdt, hoc_phan=hoc_phan_obj).exists():
                                errors.append(f"Dòng {index+2} (HP: {ma_hoc_phan}): Học phần đã tồn tại trong CTĐT này. Bỏ qua.")
                                error_count += 1
                                continue
                            chi_tiet_hp_data = {
                                'chuong_trinh_dao_tao': ctdt, 'hoc_phan': hoc_phan_obj, 'hoc_ky_du_kien': row.get('hoc_ky_du_kien'),
                                'la_bat_buoc': row.get('la_bat_buoc', False), 'tin_chi_ly_thuyet_apdung': row.get('tin_chi_ly_thuyet_apdung'),
                                'tin_chi_thuc_hanh_apdung': row.get('tin_chi_thuc_hanh_apdung'), 'so_gio_ly_thuyet_apdung': row.get('so_gio_ly_thuyet_apdung'),
                                'so_gio_thuc_hanh_apdung': row.get('so_gio_thuc_hanh_apdung'), 'so_gio_tu_hoc_apdung': row.get('so_gio_tu_hoc_apdung'),
                                'so_tiet_ly_thuyet_online': row.get('so_tiet_ly_thuyet_online'), 'ghi_chu_chi_tiet_hp': row.get('ghi_chu_chi_tiet_hp'),
                            }
                            chi_tiet_hp_data = {k: (v if pd.notna(v) else None) for k, v in chi_tiet_hp_data.items()}
                            la_bat_buoc_val = chi_tiet_hp_data.get('la_bat_buoc')
                            if isinstance(la_bat_buoc_val, str):
                                chi_tiet_hp_data['la_bat_buoc'] = la_bat_buoc_val.lower() == 'true'
                            elif pd.isna(la_bat_buoc_val):
                                chi_tiet_hp_data['la_bat_buoc'] = False
                            ChiTietHocPhanTrongCTDT.objects.create(**chi_tiet_hp_data)
                            success_count += 1
                        except Exception as e:
                            errors.append(f"Dòng {index+2} (HP: {row.get('ma_hoc_phan', 'N/A')}): Lỗi - {e}")
                            error_count += 1
                if success_count > 0:
                    messages.success(request, f"Đã tải lên thành công {success_count} học phần vào CTĐT.")
                if error_count > 0:
                    messages.error(request, f"Có {error_count} lỗi khi tải lên: " + " | ".join(errors))
                return redirect('daotao:chi_tiet_ctdt', pk_ctdt=ctdt.pk)
        else:
            messages.error(request, "Vui lòng chọn một tệp hợp lệ.")
    else:
        form = UploadHocPhanCTDTForm()
    return render(request, 'daotao/upload_hoc_phan_ctdt.html', {'form': form, 'ctdt': ctdt})

@login_required
@permission_required('daotao.add_muctieudaotao', raise_exception=True)
def them_muc_tieu_dao_tao(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    if ctdt.trang_thai != 'DRAFT':
        messages.error(request, "Chỉ có thể thêm Mục tiêu đào tạo cho CTĐT ở trạng thái 'Bản nháp'.")
        return redirect('daotao:chi_tiet_ctdt', pk_ctdt=pk_ctdt)
    if request.method == 'POST':
        form = MucTieuDaoTaoForm(request.POST)
        if form.is_valid():
            mt = form.save(commit=False)
            mt.chuong_trinh_dao_tao = ctdt
            mt.save()
            messages.success(request, "Đã thêm Mục tiêu đào tạo thành công!")
            return redirect(f"{reverse('daotao:chi_tiet_ctdt', kwargs={'pk_ctdt': ctdt.pk})}#po-tab-pane")
        else:
            messages.error(request, "Có lỗi xảy ra khi thêm Mục tiêu đào tạo. Vui lòng kiểm tra lại các trường.")
    else:
        form = MucTieuDaoTaoForm()
    context = {
        'form': form,
        'ctdt': ctdt,
        'page_title': f'Thêm Mục tiêu Đào tạo cho CTĐT: {ctdt.ten_nganh_ctdt}'
    }
    return render(request, 'daotao/them_muc_tieu_dao_tao.html', context)

# --- PLACEHOLDER FUNCTIONS START ---

@login_required
@permission_required('daotao.can_submit_for_approval', raise_exception=True)
def gui_duyet_ctdt(request, pk_ctdt):
    if request.method != 'POST':
        messages.error(request, "Yêu cầu không hợp lệ.")
        return redirect('daotao:danh_sach_ctdt')
    
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    if ctdt.trang_thai == 'DRAFT':
        ctdt.trang_thai = 'PENDING_APPROVAL'
        ctdt.save()
        messages.success(request, f"Đã gửi duyệt chương trình '{ctdt.ten_nganh_ctdt}'.")
    else:
        messages.warning(request, "Chỉ có thể gửi duyệt các chương trình ở trạng thái 'Bản nháp'.")
        
    return redirect('daotao:chi_tiet_ctdt', pk_ctdt=pk_ctdt)

@login_required
@require_http_methods(["POST"])
def xu_ly_duyet_ctdt(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    action = request.POST.get('action')

    if ctdt.trang_thai != 'PENDING_APPROVAL':
        messages.warning(request, "Chỉ có thể xử lý các chương trình đang chờ duyệt.")
        return redirect('daotao:chi_tiet_ctdt', pk_ctdt=pk_ctdt)

    if action == 'approve' and request.user.has_perm('daotao.can_approve_ctdt'):
        with transaction.atomic():
            ctdt.trang_thai = 'APPROVED'
            ctdt.ghi_chu_ctdt = f"Được phê duyệt bởi {request.user.username} vào lúc {timezone.now().strftime('%H:%M:%S %d/%m/%Y')}."
            ctdt.save()

            LichSuThayDoiCTDT.objects.create(
                chuong_trinh_dao_tao=ctdt,
                nguoi_thuc_hien=request.user,
                hanh_dong="Phê duyệt",
                chi_tiet_thay_doi="Chương trình đào tạo đã được phê duyệt."
            )
            
            if ctdt.phien_ban_goc:
                original_ctdt = ctdt.phien_ban_goc
                original_ctdt.trang_thai = 'ARCHIVED'
                original_ctdt.save()
                messages.info(request, f"Phiên bản gốc '{original_ctdt.ten_nganh_ctdt}' đã được lưu trữ.")

        messages.success(request, f"Đã phê duyệt chương trình '{ctdt.ten_nganh_ctdt}'.")

    elif action == 'reject' and request.user.has_perm('daotao.can_reject_ctdt'):
        ly_do = request.POST.get('ly_do', '').strip()
        if not ly_do:
            messages.error(request, "Cần phải cung cấp lý do khi yêu cầu chỉnh sửa.")
            return redirect('daotao:chi_tiet_ctdt', pk_ctdt=pk_ctdt)
        
        with transaction.atomic():
            ctdt.trang_thai = 'DRAFT'
            ctdt.ghi_chu_ctdt = f"Yêu cầu chỉnh sửa bởi {request.user.username} vào lúc {timezone.now().strftime('%H:%M:%S %d/%m/%Y')}.\nLý do: {ly_do}"
            ctdt.save()

            LichSuThayDoiCTDT.objects.create(
                chuong_trinh_dao_tao=ctdt,
                nguoi_thuc_hien=request.user,
                hanh_dong="Yêu cầu chỉnh sửa",
                chi_tiet_thay_doi=f"Lý do: {ly_do}"
            )

        messages.warning(request, f"Đã gửi yêu cầu chỉnh sửa cho chương trình '{ctdt.ten_nganh_ctdt}'.")
    
    else:
        messages.error(request, "Hành động không hợp lệ hoặc bạn không có quyền thực hiện.")

    return redirect('daotao:chi_tiet_ctdt', pk_ctdt=pk_ctdt)

@login_required
@permission_required('daotao.add_chuongtrinhdaotao', raise_exception=True)
def tao_phien_ban_moi_ctdt(request, pk_ctdt):
    """
    Tạo một phiên bản mới (clone) từ một CTĐT đã có.
    Bao gồm việc sao chép CTĐT, các PO, PLO, và các chi tiết học phần liên quan.
    """
    if request.method != 'POST':
        messages.error(request, "Yêu cầu không hợp lệ.")
        return redirect('daotao:danh_sach_ctdt')

    original_ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    
    try:
        with transaction.atomic():
            # 1. Clone the ChuongTrinhDaoTao object
            new_ctdt = ChuongTrinhDaoTao.objects.get(pk=pk_ctdt)
            new_ctdt.pk = None
            new_ctdt.id = None
            new_ctdt.trang_thai = 'DRAFT'
            new_ctdt.phien_ban_goc = original_ctdt
            # Simple versioning: append a timestamp or a count
            version_count = ChuongTrinhDaoTao.objects.filter(phien_ban_goc=original_ctdt).count()
            new_ctdt.version = f"{original_ctdt.version}.{version_count + 1}"
            new_ctdt.ten_nganh_ctdt = f"{original_ctdt.ten_nganh_ctdt} (Phiên bản {new_ctdt.version})"
            new_ctdt.ma_nganh_ctdt = f"{original_ctdt.ma_nganh_ctdt}-v{new_ctdt.version}"
            new_ctdt.ly_do_thay_doi = f"Phiên bản mới tạo từ CTĐT '{original_ctdt.ten_nganh_ctdt}'"
            new_ctdt.save()

            # 2. Clone related MucTieuDaoTao (POs)
            old_pos = original_ctdt.muc_tieu_dao_tao_ctdt.all()
            po_map = {} # old_pk -> new_instance
            for po in old_pos:
                new_po = MucTieuDaoTao(
                    chuong_trinh_dao_tao=new_ctdt,
                    ma_muc_tieu=po.ma_muc_tieu,
                    noi_dung=po.noi_dung
                )
                new_po.save()
                po_map[po.pk] = new_po

            # 3. Clone related ChuanDauRa (PLOs) and their M2M with new POs
            old_plos = original_ctdt.chuan_dau_ra_ctdt.all()
            for plo in old_plos:
                old_related_pos = plo.dap_ung_muc_tieu.all()
                
                new_plo = ChuanDauRa(
                    chuong_trinh_dao_tao=new_ctdt,
                    ma_cdr=plo.ma_cdr,
                    noi_dung=plo.noi_dung,
                    loai_cdr=plo.loai_cdr
                )
                new_plo.save()
                
                # Map old POs to new POs for the M2M relationship
                new_related_pos_pks = [po_map[old_po.pk].pk for old_po in old_related_pos if old_po.pk in po_map]
                if new_related_pos_pks:
                    new_plo.dap_ung_muc_tieu.set(new_related_pos_pks)

            # 4. Clone ChiTietHocPhanTrongCTDT (course details)
            old_details = original_ctdt.chitiethocphantrongctdt_set.all()
            detail_map = {} # old_pk -> new_instance
            for detail in old_details:
                new_detail = ChiTietHocPhanTrongCTDT.objects.get(pk=detail.pk)
                new_detail.pk = None
                new_detail.id = None
                new_detail.chuong_trinh_dao_tao = new_ctdt
                new_detail.save() # Save to get a PK for M2M relationships
                detail_map[detail.pk] = new_detail

            # 5. Re-establish M2M relationships within ChiTietHocPhanTrongCTDT (prerequisites, etc.)
            for old_detail_pk, new_detail in detail_map.items():
                original_detail = ChiTietHocPhanTrongCTDT.objects.get(pk=old_detail_pk)
                
                # Prerequisites
                prereq_pks = original_detail.hoc_phan_tien_quyet.values_list('pk', flat=True)
                new_prereq_pks = [detail_map[pk].pk for pk in prereq_pks if pk in detail_map]
                if new_prereq_pks:
                    new_detail.hoc_phan_tien_quyet.set(new_prereq_pks)

                # Concurrent courses
                concurrent_pks = original_detail.hoc_phan_song_hanh.values_list('pk', flat=True)
                new_concurrent_pks = [detail_map[pk].pk for pk in concurrent_pks if pk in detail_map]
                if new_concurrent_pks:
                    new_detail.hoc_phan_song_hanh.set(new_concurrent_pks)

            messages.success(request, f"Đã tạo phiên bản mới '{new_ctdt.ten_nganh_ctdt}' thành công.")
            return redirect('daotao:chi_tiet_ctdt', pk_ctdt=new_ctdt.pk)

    except Exception as e:
        messages.error(request, f"Đã có lỗi xảy ra trong quá trình tạo phiên bản mới: {e}")
        return redirect('daotao:chi_tiet_ctdt', pk_ctdt=pk_ctdt)

@login_required
@permission_required('daotao.can_archive_ctdt', raise_exception=True)
def luu_tru_ctdt(request, pk_ctdt):
    return HttpResponse(f"Chức năng lưu trữ CTĐT {pk_ctdt} chưa được triển khai.")

@login_required
@permission_required('daotao.change_hocphan', raise_exception=True)
def sua_hoc_phan(request, pk_hoc_phan):
    hoc_phan = get_object_or_404(HocPhan, pk=pk_hoc_phan)
    if request.method == 'POST':
        form = HocPhanLibModelForm(request.POST, instance=hoc_phan)
        if form.is_valid():
            form.save()
            messages.success(request, f"Đã cập nhật học phần '{hoc_phan.ten_hoc_phan}' thành công!")
            return redirect('daotao:danh_sach_hoc_phan')
        else:
            messages.error(request, "Có lỗi xảy ra khi cập nhật học phần. Vui lòng kiểm tra lại các trường.")
    else:
        form = HocPhanLibModelForm(instance=hoc_phan)
    context = {
        'form': form,
        'hoc_phan': hoc_phan,
        'page_title': f'Cập nhật Học phần: {hoc_phan.ten_hoc_phan}'
    }
    return render(request, 'daotao/sua_hoc_phan.html', context)

@login_required
@permission_required('daotao.delete_hocphan', raise_exception=True)
def xoa_hoc_phan(request, pk_hoc_phan):
    hoc_phan_can_xoa = get_object_or_404(HocPhan, pk=pk_hoc_phan)
    if request.method == 'POST':
        hoc_phan_can_xoa.delete()
        messages.success(request, f"Đã xóa học phần '{hoc_phan_can_xoa.ten_hoc_phan}' thành công.")
        return redirect('daotao:danh_sach_hoc_phan')
    context = {
        'hoc_phan': hoc_phan_can_xoa,
        'page_title': f'Xác nhận Xóa Học phần: {hoc_phan_can_xoa.ten_hoc_phan}'
    }
    return render(request, 'daotao/xoa_hoc_phan_confirm.html', context)

@login_required
def download_hoc_phan_ctdt_template(request):
    return HttpResponse(f"Chức năng download template chưa được triển khai.")

@login_required
def danh_sach_hoc_phan_theo_ctdt(request, pk_ctdt):
    return HttpResponse(f"Chức năng danh sách học phần theo ctdt {pk_ctdt} chưa được triển khai.")

@login_required
@permission_required('daotao.add_chitiethocphantrongctdt', raise_exception=True)
def them_hoc_phan_vao_ctdt(request, pk_ctdt):
    """
    View để thêm một học phần (đã có trong thư viện) vào một CTĐT cụ thể.
    """
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    
    if ctdt.trang_thai != 'DRAFT':
        messages.error(request, "Chỉ có thể thêm học phần khi CTĐT ở trạng thái 'Bản nháp'.")
        return redirect('daotao:chi_tiet_ctdt', pk_ctdt=pk_ctdt)

    if request.method == 'POST':
        form = ChiTietHocPhanTrongCTDTModelForm(request.POST, ctdt=ctdt)
        if form.is_valid():
            chi_tiet_hp = form.save(commit=False)
            chi_tiet_hp.chuong_trinh_dao_tao = ctdt
            
            if ChiTietHocPhanTrongCTDT.objects.filter(chuong_trinh_dao_tao=ctdt, hoc_phan=chi_tiet_hp.hoc_phan).exists():
                messages.error(request, f"Học phần '{chi_tiet_hp.hoc_phan.ten_hoc_phan}' đã tồn tại trong chương trình đào tạo này.")
            else:
                chi_tiet_hp.save()
                form.save_m2m()
                messages.success(request, f"Đã thêm học phần '{chi_tiet_hp.hoc_phan.ten_hoc_phan}' vào chương trình đào tạo thành công.")
                return redirect(f"{reverse('daotao:chi_tiet_ctdt', kwargs={'pk_ctdt': ctdt.pk})}#hocphan-tab-pane")
        else:
            messages.error(request, "Có lỗi xảy ra khi thêm học phần. Vui lòng kiểm tra lại các trường được đánh dấu.")
    else:
        form = ChiTietHocPhanTrongCTDTModelForm(ctdt=ctdt)

    context = {
        'form': form,
        'ctdt': ctdt,
        'page_title': f'Thêm Học phần vào CTĐT: {ctdt.ten_nganh_ctdt}'
    }
    return render(request, 'daotao/them_hoc_phan_vao_ctdt.html', context)

@login_required
@permission_required('daotao.view_chitiethocphantrongctdt', raise_exception=True)
def chi_tiet_hoc_phan_trong_ctdt(request, pk_chi_tiet_hp):
    chi_tiet_hp = get_object_or_404(ChiTietHocPhanTrongCTDT.objects.select_related(
        'hoc_phan', 
        'chuong_trinh_dao_tao', 
        'hoc_phan__don_vi_quan_ly_goc'
    ), pk=pk_chi_tiet_hp)
    
    context = {
        'chi_tiet_hp': chi_tiet_hp,
        'page_title': f'Chi tiết HP: {chi_tiet_hp.hoc_phan.ten_hoc_phan}'
    }
    return render(request, 'daotao/chi_tiet_hoc_phan_trong_ctdt.html', context)

@login_required
@permission_required('daotao.can_manage_program_structure', raise_exception=True)
def sua_chi_tiet_hp_trong_ctdt(request, pk_chi_tiet_hp):
    chi_tiet_hp = get_object_or_404(ChiTietHocPhanTrongCTDT, pk=pk_chi_tiet_hp)
    ctdt = chi_tiet_hp.chuong_trinh_dao_tao

    if ctdt.trang_thai != 'DRAFT':
        messages.error(request, "Chỉ có thể sửa chi tiết học phần khi CTĐT ở trạng thái 'Bản nháp'.")
        return redirect('daotao:chi_tiet_ctdt', pk_ctdt=ctdt.pk)

    if request.method == 'POST':
        form = ChiTietHocPhanTrongCTDTModelForm(request.POST, instance=chi_tiet_hp, ctdt=ctdt)
        if form.is_valid():
            form.save()
            messages.success(request, f"Đã cập nhật chi tiết cho học phần '{chi_tiet_hp.hoc_phan.ten_hoc_phan}' thành công.")
            return redirect(f"{reverse('daotao:chi_tiet_ctdt', kwargs={'pk_ctdt': ctdt.pk})}#hocphan-tab-pane")
        else:
            messages.error(request, "Dữ liệu không hợp lệ. Vui lòng kiểm tra lại các trường.")
    else:
        form = ChiTietHocPhanTrongCTDTModelForm(instance=chi_tiet_hp, ctdt=ctdt)

    context = {
        'form': form,
        'chi_tiet_hp': chi_tiet_hp,
        'ctdt': ctdt,
        'page_title': f'Cập nhật chi tiết HP: {chi_tiet_hp.hoc_phan.ten_hoc_phan}'
    }
    return render(request, 'daotao/sua_chi_tiet_hp_trong_ctdt.html', context)

@login_required
@permission_required('daotao.change_chitiethocphantrongctdt', raise_exception=True)
def sua_hoc_phan_ctdt(request, pk_chi_tiet_hp):
    chi_tiet = get_object_or_404(ChiTietHocPhanTrongCTDT, pk=pk_chi_tiet_hp)
    ctdt = chi_tiet.chuong_trinh_dao_tao

    if ctdt.trang_thai != 'DRAFT':
        messages.error(request, "Chỉ có thể sửa chi tiết học phần cho CTĐT ở trạng thái 'Bản nháp'.")
        return redirect('daotao:danh_sach_hoc_phan_theo_ctdt', pk_ctdt=ctdt.pk)

    if request.method == 'POST':
        form = ChiTietHocPhanTrongCTDTModelForm(request.POST, instance=chi_tiet)
        if form.is_valid():
            form.save()
            messages.success(request, f"Đã cập nhật chi tiết cho học phần: {chi_tiet.hoc_phan.ten_hoc_phan}")
            return redirect('daotao:danh_sach_hoc_phan_theo_ctdt', pk_ctdt=ctdt.pk)
        else:
            messages.error(request, "Có lỗi xảy ra khi cập nhật. Vui lòng kiểm tra lại các trường.")
    else:
        form = ChiTietHocPhanTrongCTDTModelForm(instance=chi_tiet)

    context = {
        'form': form,
        'ctdt': ctdt,
        'chi_tiet': chi_tiet,
        'page_title': f'Cập nhật Chi tiết Học phần: {chi_tiet.hoc_phan.ten_hoc_phan}'
    }
    return render(request, 'daotao/sua_hoc_phan_ctdt.html', context)
@login_required
@permission_required('daotao.delete_chitiethocphantrongctdt', raise_exception=True)
def xoa_chi_tiet_hp_trong_ctdt(request, pk_chi_tiet_hp):
    chi_tiet = get_object_or_404(ChiTietHocPhanTrongCTDT, pk=pk_chi_tiet_hp)
    ctdt = chi_tiet.chuong_trinh_dao_tao

    if ctdt.trang_thai != 'DRAFT':
        messages.error(request, "Chỉ có thể xóa học phần khỏi CTĐT ở trạng thái 'Bản nháp'.")
        return redirect('daotao:chi_tiet_ctdt', pk_ctdt=ctdt.pk)

    if request.method == 'POST':
        hoc_phan_ten = chi_tiet.hoc_phan.ten_hoc_phan
        chi_tiet.delete()
        messages.success(request, f"Đã xóa học phần '{hoc_phan_ten}' khỏi chương trình đào tạo.")
        return redirect(f"{reverse('daotao:chi_tiet_ctdt', kwargs={'pk_ctdt': ctdt.pk})}#hocphan-tab-pane")

    context = {
        'chi_tiet': chi_tiet,
        'ctdt': ctdt,
        'page_title': f'Xác nhận Xóa Học phần: {chi_tiet.hoc_phan.ten_hoc_phan}'
    }
    return render(request, 'daotao/xoa_chi_tiet_hp_trong_ctdt_confirm.html', context)

@login_required
@permission_required('daotao.delete_chitiethocphantrongctdt', raise_exception=True)
def xoa_hoc_phan_ctdt(request, pk_chi_tiet_hp):
    chi_tiet = get_object_or_404(ChiTietHocPhanTrongCTDT, pk=pk_chi_tiet_hp)
    ctdt = chi_tiet.chuong_trinh_dao_tao

    if ctdt.trang_thai != 'DRAFT':
        messages.error(request, "Chỉ có thể xóa học phần khỏi CTĐT ở trạng thái 'Bản nháp'.")
        return redirect('daotao:danh_sach_hoc_phan_theo_ctdt', pk_ctdt=ctdt.pk)

    if request.method == 'POST':
        hoc_phan_ten = chi_tiet.hoc_phan.ten_hoc_phan
        chi_tiet.delete()
        messages.success(request, f"Đã xóa học phần '{hoc_phan_ten}' khỏi chương trình đào tạo.")
        return redirect('daotao:danh_sach_hoc_phan_theo_ctdt', pk_ctdt=ctdt.pk)

    context = {
        'chi_tiet': chi_tiet,
        'ctdt': ctdt,
        'page_title': f'Xác nhận Xóa Học phần: {chi_tiet.hoc_phan.ten_hoc_phan}'
    }
    return render(request, 'daotao/xoa_hoc_phan_ctdt_confirm.html', context)
@login_required
@require_http_methods(["POST"])
def update_chi_tiet_hoc_phan_inline(request):
    return JsonResponse({'status': 'error', 'message': 'Chức năng chưa được triển khai.'})

@login_required
@require_http_methods(["POST"])
def update_muc_tieu_dao_tao_inline(request):
    pk = request.POST.get('pk')
    field = request.POST.get('field')
    value = request.POST.get('value')

    try:
        po = get_object_or_404(MucTieuDaoTao, pk=pk)
        
        # Security check: only allow updating specific fields
        allowed_fields = ['ma_muc_tieu', 'noi_dung']
        if field not in allowed_fields:
            return JsonResponse({'status': 'error', 'message': 'Trường không được phép chỉnh sửa.'})

        # Check if CTDT is in DRAFT status
        if po.chuong_trinh_dao_tao.trang_thai != 'DRAFT':
            return JsonResponse({'status': 'error', 'message': 'Chỉ có thể sửa khi CTĐT ở trạng thái "Bản nháp".'})

        setattr(po, field, value)
        po.save(update_fields=[field])
        
        return JsonResponse({'status': 'success', 'message': 'Cập nhật thành công!', 'new_value': value})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
def danh_sach_don_vi(request):
    return HttpResponse(f"Chức năng danh sách đơn vị chưa được triển khai.")

@login_required
def them_don_vi(request):
    return HttpResponse(f"Chức năng thêm đơn vị chưa được triển khai.")

@login_required
def sua_don_vi(request, pk_don_vi):
    return HttpResponse(f"Chức năng sửa đơn vị {pk_don_vi} chưa được triển khai.")

@login_required
def xoa_don_vi(request, pk_don_vi):
    return HttpResponse(f"Chức năng xóa đơn vị {pk_don_vi} chưa được triển khai.")

@login_required
@permission_required('daotao.add_chuandaura', raise_exception=True)
def them_chuan_dau_ra(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    if ctdt.trang_thai != 'DRAFT':
        messages.error(request, "Chỉ có thể thêm Chuẩn đầu ra cho CTĐT ở trạng thái 'Bản nháp'.")
        return redirect('daotao:chi_tiet_ctdt', pk_ctdt=pk_ctdt)

    if request.method == 'POST':
        form = ChuanDauRaForm(request.POST, chuong_trinh_dao_tao=ctdt)
        if form.is_valid():
            cdr = form.save(commit=False)
            cdr.chuong_trinh_dao_tao = ctdt
            cdr.save()
            form.save_m2m() # Needed for ManyToMany fields like 'dap_ung_muc_tieu'
            messages.success(request, "Đã thêm Chuẩn đầu ra thành công!")
            return redirect(f"{reverse('daotao:chi_tiet_ctdt', kwargs={'pk_ctdt': ctdt.pk})}#cdr-tab-pane")
        else:
            messages.error(request, "Có lỗi xảy ra khi thêm. Vui lòng kiểm tra lại các trường.")
    else:
        form = ChuanDauRaForm(chuong_trinh_dao_tao=ctdt)

    context = {
        'form': form,
        'ctdt': ctdt,
        'page_title': f'Thêm Chuẩn Đầu Ra cho CTĐT: {ctdt.ten_nganh_ctdt}'
    }
    return render(request, 'daotao/them_chuan_dau_ra.html', context)

@login_required
@permission_required('daotao.change_chuandaura', raise_exception=True)
def sua_chuan_dau_ra(request, pk_cdr):
    cdr = get_object_or_404(ChuanDauRa, pk=pk_cdr)
    ctdt = cdr.chuong_trinh_dao_tao

    if ctdt.trang_thai != 'DRAFT':
        messages.error(request, "Chỉ có thể sửa Chuẩn đầu ra cho CTĐT ở trạng thái 'Bản nháp'.")
        return redirect('daotao:chi_tiet_ctdt', pk_ctdt=ctdt.pk)

    if request.method == 'POST':
        form = ChuanDauRaForm(request.POST, instance=cdr, chuong_trinh_dao_tao=ctdt)
        if form.is_valid():
            form.save()
            messages.success(request, "Đã cập nhật Chuẩn đầu ra thành công!")
            return redirect(f"{reverse('daotao:chi_tiet_ctdt', kwargs={'pk_ctdt': ctdt.pk})}#cdr-tab-pane")
        else:
            messages.error(request, "Có lỗi xảy ra khi cập nhật. Vui lòng kiểm tra lại các trường.")
    else:
        form = ChuanDauRaForm(instance=cdr, chuong_trinh_dao_tao=ctdt)

    context = {
        'form': form,
        'ctdt': ctdt,
        'cdr': cdr,
        'page_title': f'Cập nhật Chuẩn Đầu Ra: {cdr.ma_cdr}'
    }
    return render(request, 'daotao/sua_chuan_dau_ra.html', context)

@login_required
@permission_required('daotao.delete_chuandaura', raise_exception=True)
@require_http_methods(["POST"])
def xoa_chuan_dau_ra(request, pk_cdr):
    plo = get_object_or_404(ChuanDauRa, pk=pk_cdr)
    if plo.chuong_trinh_dao_tao.trang_thai != 'DRAFT':
        return JsonResponse({'status': 'error', 'message': 'Chỉ có thể xóa khi CTĐT ở trạng thái "Bản nháp".'}, status=403)
    
    plo.delete()
    return JsonResponse({'status': 'success', 'message': 'Đã xóa Chuẩn Đầu Ra.'})

@login_required
@permission_required('daotao.change_muctieudaotao', raise_exception=True)
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
@permission_required('daotao.delete_muctieudaotao', raise_exception=True)
@require_http_methods(["POST"])
def xoa_muc_tieu_dao_tao(request, pk_po):
    po = get_object_or_404(MucTieuDaoTao, pk=pk_po)
    if po.chuong_trinh_dao_tao.trang_thai != 'DRAFT':
        return JsonResponse({'status': 'error', 'message': 'Chỉ có thể xóa khi CTĐT ở trạng thái "Bản nháp".'}, status=403)
    
    po.delete()
    return JsonResponse({'status': 'success', 'message': 'Đã xóa Mục tiêu Đào tạo.'})

@login_required
def get_nganh_dao_tao_options(request):
    return JsonResponse([], safe=False)

@login_required
def get_don_vi_dao_tao_options(request):
    return JsonResponse([], safe=False)

@login_required
def get_hoc_phan_details(request, pk_hoc_phan):
    """
    API endpoint to get default details for a specific HocPhan.
    """
    try:
        hoc_phan = get_object_or_404(HocPhan, pk=pk_hoc_phan)
        data = {
            'tin_chi_ly_thuyet_apdung': hoc_phan.tin_chi_ly_thuyet_goc,
            'tin_chi_thuc_hanh_apdung': hoc_phan.tin_chi_thuc_hanh_goc,
            'so_gio_ly_thuyet_apdung': hoc_phan.so_gio_ly_thuyet_goc,
            'so_gio_thuc_hanh_apdung': hoc_phan.so_gio_thuc_hanh_goc,
            'so_gio_tu_hoc_apdung': hoc_phan.so_gio_tu_hoc_goc,
            # Add any other fields you want to auto-populate
        }
        return JsonResponse(data)
    except Http404:
        return JsonResponse({'error': 'HocPhan not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def search_hoc_phan_in_ctdt_api(request, pk_ctdt):
    """
    API endpoint for Select2 to search for courses (ChiTietHocPhanTrongCTDT)
    within a specific curriculum (CTDT).
    """
    search_term = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    
    try:
        ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
        
        # Query ChiTietHocPhanTrongCTDT objects related to the specific CTDT
        queryset = ChiTietHocPhanTrongCTDT.objects.filter(
            chuong_trinh_dao_tao=ctdt
        ).select_related('hoc_phan').order_by('hoc_phan__ma_hoc_phan')
        
        if search_term:
            queryset = queryset.filter(
                Q(hoc_phan__ma_hoc_phan__icontains=search_term) |
                Q(hoc_phan__ten_hoc_phan__icontains=search_term)
            )
            
        # Exclude the current course being edited, if its PK is provided
        exclude_pk = request.GET.get('exclude_pk')
        if exclude_pk:
            queryset = queryset.exclude(pk=exclude_pk)

        paginator = Paginator(queryset, 30)
        try:
            results_page = paginator.page(page)
        except (EmptyPage, PageNotAnInteger):
            results_page = paginator.page(paginator.num_pages)

        results = [
            {
                'id': chi_tiet.pk,
                'text': f"{chi_tiet.hoc_phan.ma_hoc_phan} - {chi_tiet.hoc_phan.ten_hoc_phan}"
            }
            for chi_tiet in results_page
        ]

        return JsonResponse({
            'results': results,
            'pagination': {'more': results_page.has_next()}
        })

    except ChuongTrinhDaoTao.DoesNotExist:
        return JsonResponse({'results': [], 'pagination': {'more': False}}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# --- PLACEHOLDER FUNCTIONS END ---

#region Đơn vị Đào tạo
@login_required
@permission_required('daotao.view_donvidaotao', raise_exception=True)
def danh_sach_don_vi(request):
    query = request.GET.get('q', '')
    don_vi_list = DonViDaoTao.objects.all()
    if query:
        don_vi_list = don_vi_list.filter(
            Q(ma_don_vi__icontains=query) | Q(ten_don_vi__icontains=query)
        )
    context = {
        'don_vi_list': don_vi_list,
        'page_title': 'Quản lý Đơn vị Đào tạo',
        'query': query
    }
    return render(request, 'daotao/danh_sach_don_vi.html', context)

@login_required
@permission_required('daotao.add_donvidaotao', raise_exception=True)
def them_don_vi(request):
    if request.method == 'POST':
        form = DonViDaoTaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã thêm đơn vị đào tạo thành công!')
            return redirect('daotao:danh_sach_don_vi')
        else:
            messages.error(request, 'Vui lòng sửa các lỗi bên dưới.')
    else:
        form = DonViDaoTaoForm()
    context = {
        'form': form,
        'page_title': 'Thêm Đơn vị Đào tạo'
    }
    return render(request, 'daotao/don_vi_form.html', context)

@login_required
@permission_required('daotao.change_donvidaotao', raise_exception=True)
def sua_don_vi(request, pk):
    don_vi = get_object_or_404(DonViDaoTao, pk=pk)
    if request.method == 'POST':
        form = DonViDaoTaoForm(request.POST, instance=don_vi)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã cập nhật đơn vị đào tạo thành công!')
            return redirect('daotao:danh_sach_don_vi')
        else:
            messages.error(request, 'Vui lòng sửa các lỗi bên dưới.')
    else:
        form = DonViDaoTaoForm(instance=don_vi)
    context = {
        'form': form,
        'page_title': f'Sửa Đơn vị: {don_vi.ten_don_vi}'
    }
    return render(request, 'daotao/don_vi_form.html', context)

@login_required
@permission_required('daotao.delete_donvidaotao', raise_exception=True)
def xoa_don_vi(request, pk):
    don_vi = get_object_or_404(DonViDaoTao, pk=pk)
    if request.method == 'POST':
        don_vi.delete()
        messages.success(request, 'Đã xóa đơn vị đào tạo thành công!')
        return redirect('daotao:danh_sach_don_vi')
    context = {
        'don_vi': don_vi,
        'page_title': f'Xác nhận xóa: {don_vi.ten_don_vi}'
    }
    return render(request, 'daotao/xoa_don_vi_confirm.html', context)
#endregion


# Danh Muc Kien Thuc
@login_required
@permission_required('daotao.view_danhmuckienthuc', raise_exception=True)
def danh_sach_danh_muc_kien_thuc(request):
    danh_muc_list = DanhMucKienThuc.objects.all()
    context = {
        'page_obj': danh_muc_list,
        'page_title': 'Danh mục Kiến thức',
    }
    return render(request, 'daotao/danh_sach_danh_muc_kien_thuc.html', context)

@login_required
@permission_required('daotao.add_danhmuckienthuc', raise_exception=True)
def them_danh_muc_kien_thuc(request):
    if request.method == 'POST':
        form = DanhMucKienThucForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã thêm Danh mục kiến thức thành công!')
            return redirect('daotao:danh_sach_danh_muc_kien_thuc')
    else:
        form = DanhMucKienThucForm()
    context = {
        'form': form,
        'page_title': 'Thêm Danh mục Kiến thức',
    }
    return render(request, 'daotao/them_danh_muc_kien_thuc.html', context)

@login_required
@permission_required('daotao.change_danhmuckienthuc', raise_exception=True)
def sua_danh_muc_kien_thuc(request, pk):
    danh_muc = get_object_or_404(DanhMucKienThuc, pk=pk)
    if request.method == 'POST':
        form = DanhMucKienThucForm(request.POST, instance=danh_muc)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã cập nhật Danh mục kiến thức thành công!')
            return redirect('daotao:danh_sach_danh_muc_kien_thuc')
    else:
        form = DanhMucKienThucForm(instance=danh_muc)
    context = {
        'form': form,
        'page_title': 'Sửa Danh mục Kiến thức',
    }
    return render(request, 'daotao/them_danh_muc_kien_thuc.html', context)

@login_required
@permission_required('daotao.delete_danhmuckienthuc', raise_exception=True)
def xoa_danh_muc_kien_thuc(request, pk):
    danh_muc = get_object_or_404(DanhMucKienThuc, pk=pk)
    if request.method == 'POST':
        danh_muc.delete()
        messages.success(request, f"Đã xóa Danh mục kiến thức '{danh_muc.ten_danh_muc}' thành công.")
        return redirect('daotao:danh_sach_danh_muc_kien_thuc')
    context = {
        'object': danh_muc,
        'page_title': 'Xác nhận xóa Danh mục kiến thức',
        'confirm_message': f"Bạn có chắc chắn muốn xóa danh mục '{danh_muc.ten_danh_muc}' không?"
    }
    return render(request, 'daotao/confirm_delete.html', context)


#region DeCuongHocPhan
@login_required
@permission_required('daotao.view_decuonghocphan', raise_exception=True)
def danh_sach_de_cuong(request, pk_hoc_phan):
    hoc_phan = get_object_or_404(HocPhan, pk=pk_hoc_phan)
    de_cuong_list = DeCuongHocPhan.objects.filter(hoc_phan=hoc_phan).order_by('-ngay_ban_hanh')
    context = {
        'hoc_phan': hoc_phan,
        'de_cuong_list': de_cuong_list,
        'page_title': f'Các phiên bản Đề cương cho HP: {hoc_phan.ten_hoc_phan}'
    }
    return render(request, 'daotao/danh_sach_de_cuong.html', context)

@login_required
@permission_required('daotao.add_decuonghocphan', raise_exception=True)
def them_de_cuong(request, pk_hoc_phan):
    hoc_phan = get_object_or_404(HocPhan, pk=pk_hoc_phan)
    if request.method == 'POST':
        form = DeCuongHocPhanForm(request.POST)
        clo_formset = ChuanDauRaHocPhanFormSet(request.POST, prefix='clo')
        noi_dung_formset = NoiDungChiTietDeCuongFormSet(request.POST, prefix='noidung')
        danh_gia_formset = HinhThucDanhGiaFormSet(request.POST, prefix='danhgia')

        if form.is_valid() and clo_formset.is_valid() and noi_dung_formset.is_valid() and danh_gia_formset.is_valid():
            with transaction.atomic():
                de_cuong = form.save(commit=False)
                de_cuong.hoc_phan = hoc_phan
                de_cuong.save()
                
                clo_formset.instance = de_cuong
                clo_formset.save()

                noi_dung_formset.instance = de_cuong
                noi_dung_formset.save()

                danh_gia_formset.instance = de_cuong
                danh_gia_formset.save()

            messages.success(request, "Đã thêm phiên bản đề cương mới thành công.")
            return redirect('daotao:sua_de_cuong', pk_de_cuong=de_cuong.pk)
        else:
            messages.error(request, "Có lỗi xảy ra, vui lòng kiểm tra lại thông tin.")
    else:
        form = DeCuongHocPhanForm()
        clo_formset = ChuanDauRaHocPhanFormSet(prefix='clo', queryset=ChuanDauRaHocPhan.objects.none())
        noi_dung_formset = NoiDungChiTietDeCuongFormSet(prefix='noidung', queryset=NoiDungChiTietDeCuong.objects.none())
        danh_gia_formset = HinhThucDanhGiaFormSet(prefix='danhgia', queryset=HinhThucDanhGia.objects.none())
        
    context = {
        'form': form,
        'clo_formset': clo_formset,
        'noi_dung_formset': noi_dung_formset,
        'danh_gia_formset': danh_gia_formset,
        'hoc_phan': hoc_phan,
        'page_title': f'Thêm Đề cương mới cho HP: {hoc_phan.ten_hoc_phan}'
    }
    return render(request, 'daotao/de_cuong_form.html', context)

@login_required
@permission_required('daotao.change_decuonghocphan', raise_exception=True)
def sua_de_cuong(request, pk_de_cuong):
    de_cuong = get_object_or_404(DeCuongHocPhan, pk=pk_de_cuong)
    hoc_phan = de_cuong.hoc_phan
    if request.method == 'POST':
        form = DeCuongHocPhanForm(request.POST, instance=de_cuong)
        clo_formset = ChuanDauRaHocPhanFormSet(request.POST, instance=de_cuong, prefix='clo')
        noi_dung_formset = NoiDungChiTietDeCuongFormSet(request.POST, instance=de_cuong, prefix='noidung')
        danh_gia_formset = HinhThucDanhGiaFormSet(request.POST, instance=de_cuong, prefix='danhgia')

        if form.is_valid() and clo_formset.is_valid() and noi_dung_formset.is_valid() and danh_gia_formset.is_valid():
            with transaction.atomic():
                form.save()
                clo_formset.save()
                noi_dung_formset.save()
                danh_gia_formset.save()
            messages.success(request, "Đã cập nhật đề cương và các mục liên quan thành công!")
            return redirect('daotao:danh_sach_de_cuong', pk_hoc_phan=hoc_phan.pk)
        else:
            messages.error(request, "Vui lòng kiểm tra lại các lỗi bên dưới.")
    else:
        form = DeCuongHocPhanForm(instance=de_cuong)
        clo_formset = ChuanDauRaHocPhanFormSet(instance=de_cuong, prefix='clo')
        noi_dung_formset = NoiDungChiTietDeCuongFormSet(instance=de_cuong, prefix='noidung')
        danh_gia_formset = HinhThucDanhGiaFormSet(instance=de_cuong, prefix='danhgia')

    context = {
        'form': form,
        'clo_formset': clo_formset,
        'noi_dung_formset': noi_dung_formset,
        'danh_gia_formset': danh_gia_formset,
        'hoc_phan': hoc_phan,
        'page_title': f'Sửa Đề cương: {de_cuong.ten_de_cuong_phien_ban}'
    }
    return render(request, 'daotao/de_cuong_form.html', context)

@login_required
@permission_required('daotao.delete_decuonghocphan', raise_exception=True)
def xoa_de_cuong(request, pk_de_cuong):
    de_cuong = get_object_or_404(DeCuongHocPhan, pk=pk_de_cuong)
    hoc_phan_pk = de_cuong.hoc_phan.pk
    if request.method == 'POST':
        de_cuong.delete()
        messages.success(request, "Đã xóa phiên bản đề cương thành công.")
        return redirect('daotao:danh_sach_de_cuong', pk_hoc_phan=hoc_phan_pk)
    
    context = {
        'object': de_cuong,
        'page_title': 'Xác nhận xóa Đề cương',
        'confirm_message': f"Bạn có chắc chắn muốn xóa phiên bản đề cương '{de_cuong.ten_de_cuong_phien_ban}' không?",
        'cancel_url': reverse('daotao:danh_sach_de_cuong', kwargs={'pk_hoc_phan': hoc_phan_pk})
    }
    return render(request, 'daotao/confirm_delete.html', context)

@login_required
@permission_required('daotao.delete_decuonghocphan', raise_exception=True)
def xoa_de_cuong(request, pk_de_cuong):
    de_cuong = get_object_or_404(DeCuongHocPhan, pk=pk_de_cuong)
    hoc_phan_pk = de_cuong.hoc_phan.pk
    if request.method == 'POST':
        de_cuong.delete()
        messages.success(request, "Đã xóa phiên bản đề cương thành công.")
        return redirect('daotao:danh_sach_de_cuong', pk_hoc_phan=hoc_phan_pk)
    context = {
        'object': de_cuong,
        'page_title': f'Xác nhận xóa Đề cương: {de_cuong.ten_de_cuong_phien_ban}'
    }
    return render(request, 'daotao/de_cuong_confirm_delete.html', context)
#endregion

def doi_sanh_ctdt(request):
    if request.method == 'POST':
        form = DoiSanhCTDTForm(request.POST)
        if form.is_valid():
            ctdt1 = form.cleaned_data['ctdt1']
            ctdt2 = form.cleaned_data['ctdt2']

            # 1. Compare general info
            info_fields = [
                'ten_nganh_ctdt', 'ma_nganh_ctdt', 'ten_tieng_anh', 'trinh_do_dao_tao',
                'hinh_thuc_dao_tao', 'so_tin_chi_yeu_cau', 'thoi_gian_dao_tao',
                'van_bang_tot_nghiep', 'don_vi_quan_ly'
            ]
            info_comparison = {}
            for field in info_fields:
                val1 = getattr(ctdt1, field)
                val2 = getattr(ctdt2, field)
                info_comparison[ctdt1._meta.get_field(field).verbose_name] = {
                    'value1': val1,
                    'value2': val2,
                    'is_different': val1 != val2
                }

            # 2. Compare courses (HocPhan)
            hp1_qs = ChiTietHocPhanTrongCTDT.objects.filter(chuong_trinh_dao_tao=ctdt1).select_related('hoc_phan')
            hp2_qs = ChiTietHocPhanTrongCTDT.objects.filter(chuong_trinh_dao_tao=ctdt2).select_related('hoc_phan')
            
            hp1_dict = {hp.hoc_phan.ma_hoc_phan: hp for hp in hp1_qs}
            hp2_dict = {hp.hoc_phan.ma_hoc_phan: hp for hp in hp2_qs}

            common_hp_codes = set(hp1_dict.keys()) & set(hp2_dict.keys())
            unique_to_1_codes = set(hp1_dict.keys()) - set(hp2_dict.keys())
            unique_to_2_codes = set(hp2_dict.keys()) - set(hp1_dict.keys())

            common_hps_comparison = []
            for code in sorted(list(common_hp_codes)):
                detail1 = hp1_dict[code]
                detail2 = hp2_dict[code]
                is_diff = (detail1.la_bat_buoc != detail2.la_bat_buoc or
                           detail1.hoc_ky_du_kien != detail2.hoc_ky_du_kien or
                           detail1.get_tong_tin_chi_apdung() != detail2.get_tong_tin_chi_apdung())
                common_hps_comparison.append({
                    'ma_hp': code,
                    'ten_hp': detail1.hoc_phan.ten_hoc_phan,
                    'detail1': detail1,
                    'detail2': detail2,
                    'is_different': is_diff
                })

            unique_to_1 = [hp1_dict[code] for code in sorted(list(unique_to_1_codes))]
            unique_to_2 = [hp2_dict[code] for code in sorted(list(unique_to_2_codes))]

            # 3. Compare Program Objectives (MucTieuDaoTao)
            po1_qs = MucTieuDaoTao.objects.filter(chuong_trinh_dao_tao=ctdt1)
            po2_qs = MucTieuDaoTao.objects.filter(chuong_trinh_dao_tao=ctdt2)
            po1_dict = {po.ma_muc_tieu: po for po in po1_qs}
            po2_dict = {po.ma_muc_tieu: po for po in po2_qs}
            common_po_codes = set(po1_dict.keys()) & set(po2_dict.keys())
            unique_po_1_codes = set(po1_dict.keys()) - set(po2_dict.keys())
            unique_po_2_codes = set(po2_dict.keys()) - set(po1_dict.keys())
            
            common_pos_comparison = []
            for code in sorted(list(common_po_codes)):
                po1 = po1_dict[code]
                po2 = po2_dict[code]
                common_pos_comparison.append({
                    'ma': code,
                    'noi_dung1': po1.noi_dung,
                    'noi_dung2': po2.noi_dung,
                    'is_different': po1.noi_dung != po2.noi_dung
                })

            # 4. Compare Program Learning Outcomes (ChuanDauRa)
            plo1_qs = ChuanDauRa.objects.filter(chuong_trinh_dao_tao=ctdt1)
            plo2_qs = ChuanDauRa.objects.filter(chuong_trinh_dao_tao=ctdt2)
            plo1_dict = {plo.ma_cdr: plo for plo in plo1_qs}
            plo2_dict = {plo.ma_cdr: plo for plo in plo2_qs}
            common_plo_codes = set(plo1_dict.keys()) & set(plo2_dict.keys())
            unique_plo_1_codes = set(plo1_dict.keys()) - set(plo2_dict.keys())
            unique_plo_2_codes = set(plo2_dict.keys()) - set(plo1_dict.keys())

            common_plos_comparison = []
            for code in sorted(list(common_plo_codes)):
                plo1 = plo1_dict[code]
                plo2 = plo2_dict[code]
                common_plos_comparison.append({
                    'ma': code,
                    'noi_dung1': plo1.noi_dung,
                    'noi_dung2': plo2.noi_dung,
                    'is_different': plo1.noi_dung != plo2.noi_dung
                })

            context = {
                'ctdt1': ctdt1,
                'ctdt2': ctdt2,
                'info_comparison': info_comparison,
                'common_hps': common_hps_comparison,
                'unique_to_1': unique_to_1,
                'unique_to_2': unique_to_2,
                'common_pos': common_pos_comparison,
                'unique_po_1': [po1_dict[code] for code in sorted(list(unique_po_1_codes))],
                'unique_po_2': [po2_dict[code] for code in sorted(list(unique_po_2_codes))],
                'common_plos': common_plos_comparison,
                'unique_plo_1': [plo1_dict[code] for code in sorted(list(unique_plo_1_codes))],
                'unique_plo_2': [plo2_dict[code] for code in sorted(list(unique_plo_2_codes))],
                'page_title': f'Đối sánh: {ctdt1.ten_nganh_ctdt} vs {ctdt2.ten_nganh_ctdt}'
            }
            return render(request, 'daotao/ket_qua_doi_sanh_ctdt.html', context)
    else:
        form = DoiSanhCTDTForm()

    context = {
        'form': form,
        'page_title': 'Đối sánh Chương trình Đào tạo'
    }
    return render(request, 'daotao/doi_sanh_ctdt.html', context)

@login_required
@require_http_methods(["POST"])
@permission_required('daotao.add_muctieudaotao', raise_exception=True)
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
def api_get_po_details(request, pk_po):
    """
    API endpoint to get details of a specific MucTieuDaoTao (PO) as JSON.
    """
    po = get_object_or_404(MucTieuDaoTao, pk=pk_po)
    data = {
        'pk': po.pk,
        'ma_muc_tieu': po.ma_muc_tieu,
        'noi_dung': po.noi_dung,
    }
    return JsonResponse(data)

@login_required
@require_http_methods(["POST"])
@permission_required('daotao.add_chuandaura', raise_exception=True)
def api_them_plo(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    if ctdt.trang_thai != 'DRAFT':
        return JsonResponse({'status': 'error', 'message': "Chỉ có thể thêm khi CTĐT ở trạng thái 'Bản nháp'."}, status=403)
    
    form = ChuanDauRaForm(request.POST, ctdt=ctdt)
    if form.is_valid():
        plo = form.save(commit=False)
        plo.chuong_trinh_dao_tao = ctdt
        plo.save()
        form.save_m2m()
        return JsonResponse({'status': 'success', 'message': 'Đã thêm Chuẩn Đầu ra thành công!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Dữ liệu không hợp lệ.', 'errors': form.errors}, status=400)

@login_required
def api_get_plo_details(request, pk_cdr):
    """
    API endpoint to get details of a specific ChuanDauRa (PLO) as JSON.
    """
    plo = get_object_or_404(ChuanDauRa, pk=pk_cdr)
    data = {
        'pk': plo.pk,
        'ma_cdr': plo.ma_cdr,
        'noi_dung': plo.noi_dung,
        'loai_cdr': plo.loai_cdr,
        'dap_ung_muc_tieu': list(plo.dap_ung_muc_tieu.values_list('pk', flat=True))
    }
    return JsonResponse(data)

@login_required
def api_get_de_cuong_chi_tiet(request, pk_hoc_phan):
    """
    API endpoint to get the detailed content of the active syllabus for a course.
    """
    # Find the active syllabus for the given course
    de_cuong = get_object_or_404(
        DeCuongHocPhan.objects.select_related('hoc_phan', 'hoc_phan__don_vi_quan_ly_goc'), 
        hoc_phan__pk=pk_hoc_phan, 
        la_phien_ban_hien_hanh=True
    )
    
    hoc_phan = de_cuong.hoc_phan

    # Serialize the main syllabus data
    data = {
        'ten_hoc_phan': hoc_phan.ten_hoc_phan,
        'ma_hoc_phan': hoc_phan.ma_hoc_phan,
        'so_tin_chi': hoc_phan.tong_so_tin_chi_goc,
        'don_vi_quan_ly': hoc_phan.don_vi_quan_ly_goc.ten_don_vi if hoc_phan.don_vi_quan_ly_goc else "N/A",
        'ten_de_cuong_phien_ban': de_cuong.ten_de_cuong_phien_ban,
        'ngay_ban_hanh': de_cuong.ngay_ban_hanh.strftime('%d/%m/%Y'),
        'muc_tieu_hoc_phan': de_cuong.muc_tieu_hoc_phan,
        'tom_tat_noi_dung': de_cuong.tom_tat_noi_dung,
        'phuong_phap_day_hoc': de_cuong.phuong_phap_day_hoc,
        'nhiem_vu_sinh_vien': de_cuong.nhiem_vu_sinh_vien,
        'thang_diem_danh_gia': de_cuong.thang_diem_danh_gia,
        'tai_lieu_hoc_tap': de_cuong.tai_lieu_hoc_tap,
        'cac_yeu_cau_khac': de_cuong.cac_yeu_cau_khac,
        'chuan_dau_ra': [],
        'noi_dung_chi_tiet': [],
        'hinh_thuc_danh_gia': []
    }

    # Serialize related CLOs (ChuanDauRaHocPhan)
    clos = de_cuong.chuan_dau_ra_cua_de_cuong.all().order_by('ma_clo')
    for clo in clos:
        data['chuan_dau_ra'].append({
            'ma_clo': clo.ma_clo,
            'noi_dung': clo.noi_dung,
            'muc_do_bloom': clo.get_muc_do_bloom_display()
        })

    # Serialize detailed content (NoiDungChiTietDeCuong)
    noi_dungs = de_cuong.noi_dung_chi_tiet.prefetch_related('chuan_dau_ra_lien_quan').order_by('tuan_hoc_hoac_chu_de')
    for nd in noi_dungs:
        data['noi_dung_chi_tiet'].append({
            'tuan_hoc_hoac_chu_de': nd.tuan_hoc_hoac_chu_de,
            'noi_dung_giang_day': nd.noi_dung_giang_day,
            'so_gio_ly_thuyet': nd.so_gio_ly_thuyet,
            'so_gio_thuc_hanh': nd.so_gio_thuc_hanh,
            'so_gio_tu_hoc': nd.so_gio_tu_hoc,
            'chuan_dau_ra_lien_quan': [clo.ma_clo for clo in nd.chuan_dau_ra_lien_quan.all()]
        })

    # Serialize evaluation methods (HinhThucDanhGia)
    danh_gias = de_cuong.hinh_thuc_danh_gia.prefetch_related('chuan_dau_ra_danh_gia').order_by('loai_danh_gia')
    for dg in danh_gias:
        data['hinh_thuc_danh_gia'].append({
            'ten_hinh_thuc': dg.ten_hinh_thuc,
            'loai_danh_gia': dg.get_loai_danh_gia_display(),
            'ty_le_diem': dg.ty_le_diem,
            'chuan_dau_ra_danh_gia': [clo.ma_clo for clo in dg.chuan_dau_ra_danh_gia.all()]
        })

    return JsonResponse(data)

import re

@login_required
def api_program_flowchart_data(request, pk_ctdt):
    """
    API endpoint to provide data for the Mermaid.js program flowchart.
    """
    def clean_mermaid_id(text):
        # Remove any character that is not a letter, number, or underscore
        return re.sub(r'[^a-zA-Z0-9_]', '', text)

    try:
        ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
        details = ChiTietHocPhanTrongCTDT.objects.filter(
            chuong_trinh_dao_tao=ctdt
        ).select_related('hoc_phan', 'danh_muc_kien_thuc').prefetch_related(
            'hoc_phan_tien_quyet__hoc_phan', 'hoc_phan_song_hanh__hoc_phan'
        )

        nodes = []
        edges = []
        
        # Use a set to keep track of added nodes to avoid duplicates
        added_nodes = set()

        for detail in details:
            # Use the original ma_hoc_phan for mapping, but a cleaned version for Mermaid ID
            original_hp_id = detail.hoc_phan.ma_hoc_phan
            hp_mermaid_id = clean_mermaid_id(original_hp_id)
            
            if hp_mermaid_id not in added_nodes:
                nodes.append({
                    'id': hp_mermaid_id,
                    'original_id': original_hp_id,
                    'name': detail.hoc_phan.ten_hoc_phan,
                    'tin_chi': detail.tong_so_tin_chi_apdung,
                    'khoi_kien_thuc': detail.danh_muc_kien_thuc.ten_danh_muc if detail.danh_muc_kien_thuc else "Chưa phân loại"
                })
                added_nodes.add(hp_mermaid_id)

            # Add prerequisite edges
            for tien_quyet_detail in detail.hoc_phan_tien_quyet.all():
                source_id = clean_mermaid_id(tien_quyet_detail.hoc_phan.ma_hoc_phan)
                edges.append({
                    'source': source_id,
                    'target': hp_mermaid_id,
                    'type': 'tienquyet'
                })

            # Add concurrent edges
            for song_hanh_detail in detail.hoc_phan_song_hanh.all():
                source_id = clean_mermaid_id(song_hanh_detail.hoc_phan.ma_hoc_phan)
                edges.append({
                    'source': source_id,
                    'target': hp_mermaid_id,
                    'type': 'songhanh'
                })

        return JsonResponse({'nodes': nodes, 'edges': edges})

    except ChuongTrinhDaoTao.DoesNotExist:
        return JsonResponse({'error': 'Program not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

#region Giảng viên
@login_required
@permission_required('daotao.view_giangvien', raise_exception=True)
def danh_sach_giang_vien(request):
    giang_vien_list = GiangVien.objects.annotate(
        so_ctdt_tham_gia=Count('chuong_trinh_tham_gia')
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
    
    giang_vien_list = GiangVien.objects.annotate(
        is_in_ctdt=Exists(ctdt.giang_vien_tham_gia.filter(pk=OuterRef('pk')))
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
        # This action is now optimistic on the frontend. 
        # We don't create a dummy assignment anymore.
        # The lecturer will be formally linked when an actual assignment is made.
        message = f"Đã chuyển giảng viên {giang_vien.ho_ten} sang cột đã tham gia. Vui lòng phân công cụ thể."
        
        # Manually add the attribute that the template expects
        giang_vien.phan_cong_trong_ctdt = []

        # Render the HTML for the newly assigned lecturer
        context = {
            'giang_vien_da_tham_gia': [giang_vien], 
            'ctdt': ctdt,
            'is_draft': is_draft
        }
        lecturer_html = render_to_string('daotao/partials/_giang_vien_da_tham_gia_list.html', context)

    elif action == 'remove':
        # This action will remove all assignments for this lecturer in this CTDT
        PhanCongGiangDay.objects.filter(
            giang_vien=giang_vien,
            chi_tiet_hoc_phan__chuong_trinh_dao_tao=ctdt
        ).delete()
        message = f"Đã xóa tất cả phân công của giảng viên {giang_vien.ho_ten} khỏi chương trình."
        
        # Render the HTML for the newly available lecturer
        context = {
            'giang_vien_chua_tham_gia': [giang_vien], 
            'is_draft': is_draft,
            'ctdt': ctdt
        }
        lecturer_html = render_to_string('daotao/partials/_giang_vien_chua_tham_gia_list.html', context)

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

@login_required
def api_search_giang_vien_chua_tham_gia(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    query = request.GET.get('q', '')

    # Find lecturers who have an assignment in this CTDT
    giang_vien_da_tham_gia_pks = PhanCongGiangDay.objects.filter(
        chi_tiet_hoc_phan__chuong_trinh_dao_tao=ctdt
    ).values_list('giang_vien__pk', flat=True).distinct()

    results = GiangVien.objects.exclude(pk__in=giang_vien_da_tham_gia_pks)
    
    if query:
        results = results.filter(
            Q(ho__icontains=query) | Q(ten__icontains=query) | Q(ma_can_bo__icontains=query)
        )
    
    results = results.order_by('ten', 'ho')[:50] # Limit results for performance

    context = {
        'giang_vien_chua_tham_gia': results,
        'ctdt': ctdt,
        'is_draft': ctdt.trang_thai == 'DRAFT'
    }
    return render(request, 'daotao/partials/_giang_vien_chua_tham_gia_list.html', context)

@login_required
def api_get_giang_vien_da_tham_gia(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    query = request.GET.get('q', '')

    # Get all lecturers who have at least one assignment in this CTDT
    assigned_lecturers = GiangVien.objects.filter(
        cac_phan_cong__chi_tiet_hoc_phan__chuong_trinh_dao_tao=ctdt
    ).distinct().prefetch_related(
        # Prefetch only the assignments relevant to the current CTDT
        models.Prefetch(
            'cac_phan_cong',
            queryset=PhanCongGiangDay.objects.filter(chi_tiet_hoc_phan__chuong_trinh_dao_tao=ctdt)
                                               .select_related('chi_tiet_hoc_phan__hoc_phan'),
            to_attr='phan_cong_trong_ctdt'
        )
    )

    if query:
        assigned_lecturers = assigned_lecturers.filter(
            Q(ho__icontains=query) | Q(ten__icontains=query) | Q(ma_can_bo__icontains=query)
        )

    assigned_lecturers = assigned_lecturers.order_by('ten', 'ho')

    context = {
        'giang_vien_da_tham_gia': assigned_lecturers,
        'ctdt': ctdt,
        'is_draft': ctdt.trang_thai == 'DRAFT'
    }
    return render(request, 'daotao/partials/_giang_vien_da_tham_gia_list.html', context)

@login_required
def api_get_phan_cong_form(request, pk_ctdt, pk_gv):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    giang_vien = get_object_or_404(GiangVien, pk=pk_gv)
    
    hoc_phan_list = ChiTietHocPhanTrongCTDT.objects.filter(chuong_trinh_dao_tao=ctdt).select_related('hoc_phan').order_by('hoc_phan__ma_hoc_phan')
    
    current_assignments = PhanCongGiangDay.objects.filter(
        giang_vien=giang_vien,
        chi_tiet_hoc_phan__chuong_trinh_dao_tao=ctdt
    ).values_list('chi_tiet_hoc_phan__pk', 'vai_tro')
    
    current_assignments_dict = {pk: vai_tro for pk, vai_tro in current_assignments}

    context = {
        'giang_vien': giang_vien,
        'hoc_phan_list': hoc_phan_list,
        'current_assignments': current_assignments_dict,
        'vai_tro_choices': PhanCongGiangDay.VAI_TRO_CHOICES,
    }
    return render(request, 'daotao/partials/_phan_cong_giang_day_modal.html', context)

@login_required
@require_http_methods(["POST"])
@permission_required('daotao.change_chuongtrinhdaotao', raise_exception=True)
def api_luu_phan_cong(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    giang_vien_pk = request.POST.get('giang_vien_pk')
    selected_hoc_phan_pks = request.POST.getlist('hoc_phan')

    if not giang_vien_pk:
        return JsonResponse({'status': 'error', 'message': 'Thiếu thông tin giảng viên.'}, status=400)

    giang_vien = get_object_or_404(GiangVien, pk=giang_vien_pk)

    try:
        with transaction.atomic():
            # First, remove all existing assignments for this lecturer in this CTDT
            PhanCongGiangDay.objects.filter(
                giang_vien=giang_vien,
                chi_tiet_hoc_phan__chuong_trinh_dao_tao=ctdt
            ).delete()

            # Then, create new assignments for the selected courses
            for hp_ctdt_pk in selected_hoc_phan_pks:
                vai_tro = request.POST.get(f'vai_tro_{hp_ctdt_pk}')
                chi_tiet_hp = get_object_or_404(ChiTietHocPhanTrongCTDT, pk=hp_ctdt_pk)
                
                if chi_tiet_hp.chuong_trinh_dao_tao != ctdt:
                    # Security check
                    continue

                PhanCongGiangDay.objects.create(
                    giang_vien=giang_vien,
                    chi_tiet_hoc_phan=chi_tiet_hp,
                    vai_tro=vai_tro
                )
        
        # After saving, re-fetch the lecturer with updated assignments to render the partial
        giang_vien_updated = GiangVien.objects.prefetch_related(
            models.Prefetch(
                'cac_phan_cong',
                queryset=PhanCongGiangDay.objects.filter(chi_tiet_hoc_phan__chuong_trinh_dao_tao=ctdt)
                                                   .select_related('chi_tiet_hoc_phan__hoc_phan'),
                to_attr='phan_cong_trong_ctdt'
            )
        ).get(pk=giang_vien_pk)

        # Render just the course list part for this lecturer
        updated_courses_html = render_to_string(
            'daotao/partials/_assigned_courses_list.html', 
            {'gv': giang_vien_updated}
        )

        return JsonResponse({
            'status': 'success', 
            'message': 'Đã cập nhật phân công thành công!',
            'updated_courses_html': updated_courses_html,
            'giang_vien_pk': giang_vien_pk
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Đã có lỗi xảy ra: {str(e)}'}, status=500)

#endregion
