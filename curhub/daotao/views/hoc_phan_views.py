from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import HocPhan, DanhMucKienThuc, DeCuongHocPhan, DonViDaoTao, ChiTietHocPhanTrongCTDT
from ..forms import (
    HocPhanLibModelForm as HocPhanForm,
    DanhMucKienThucForm,
    DeCuongHocPhanForm,
    ChuanDauRaHocPhanFormSet,
    NoiDungChiTietDeCuongFormSet,
    HinhThucDanhGiaFormSet,
    DeCuongTaiLieuFormSet
)
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

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
@permission_required('daotao.change_hocphan', raise_exception=True)
def sua_hoc_phan(request, pk_hoc_phan):
    hoc_phan = get_object_or_404(HocPhan, pk=pk_hoc_phan)
    if request.method == 'POST':
        form = HocPhanForm(request.POST, instance=hoc_phan)
        if form.is_valid():
            form.save()
            messages.success(request, f"Đã cập nhật học phần '{hoc_phan.ten_hoc_phan}' thành công!")
            return redirect('daotao:danh_sach_hoc_phan')
        else:
            messages.error(request, "Có lỗi xảy ra khi cập nhật học phần. Vui lòng kiểm tra lại các trường.")
    else:
        form = HocPhanForm(instance=hoc_phan)
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

def download_hoc_phan_ctdt_template(request):
    pass

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

@login_required
@permission_required('daotao.view_decuonghocphan', raise_exception=True)
def danh_sach_de_cuong(request, pk_hoc_phan):
    hoc_phan = get_object_or_404(HocPhan, pk=pk_hoc_phan)
    de_cuong_list = DeCuongHocPhan.objects.filter(hoc_phan=hoc_phan).order_by('-ngay_ban_hanh')
    
    context = {
        'hoc_phan': hoc_phan,
        'de_cuong_list': de_cuong_list,
        'page_title': f'Đề cương học phần: {hoc_phan.ten_hoc_phan}'
    }
    return render(request, 'daotao/danh_sach_de_cuong.html', context)

@login_required
@permission_required('daotao.add_decuonghocphan', raise_exception=True)
def them_de_cuong(request, pk_hoc_phan):
    hoc_phan = get_object_or_404(HocPhan, pk=pk_hoc_phan)
    de_cuong = DeCuongHocPhan(hoc_phan=hoc_phan, nguoi_tao=request.user) # Create a new, unsaved instance

    if request.method == 'POST':
        form = DeCuongHocPhanForm(request.POST)
        # Pass a dummy queryset for the formsets to validate, but they won't be saved until the main object is.
        clo_formset = ChuanDauRaHocPhanFormSet(request.POST, instance=de_cuong, prefix='clos')
        noi_dung_formset = NoiDungChiTietDeCuongFormSet(request.POST, instance=de_cuong, prefix='noidungs')
        danh_gia_formset = HinhThucDanhGiaFormSet(request.POST, instance=de_cuong, prefix='danhgias')
        tai_lieu_formset = DeCuongTaiLieuFormSet(request.POST, instance=de_cuong, prefix='tailieus')

        if form.is_valid() and clo_formset.is_valid() and noi_dung_formset.is_valid() and danh_gia_formset.is_valid() and tai_lieu_formset.is_valid():
            # Save the main form first to get a PK
            de_cuong_instance = form.save(commit=False)
            de_cuong_instance.hoc_phan = hoc_phan
            de_cuong_instance.nguoi_tao = request.user
            de_cuong_instance.save()

            # Now, save the formsets with the newly created instance
            clo_formset.instance = de_cuong_instance
            clo_formset.save()
            
            noi_dung_formset.instance = de_cuong_instance
            noi_dung_formset.save()

            danh_gia_formset.instance = de_cuong_instance
            danh_gia_formset.save()

            tai_lieu_formset.instance = de_cuong_instance
            tai_lieu_formset.save()
            
            messages.success(request, f"Đã tạo đề cương '{de_cuong_instance.ten_de_cuong_phien_ban}' thành công!")
            return redirect('daotao:danh_sach_de_cuong', pk_hoc_phan=hoc_phan.pk)
        else:
            messages.error(request, "Có lỗi xảy ra khi thêm đề cương. Vui lòng kiểm tra lại các trường.")
    else:
        form = DeCuongHocPhanForm()
        clo_formset = ChuanDauRaHocPhanFormSet(instance=de_cuong, prefix='clos')
        noi_dung_formset = NoiDungChiTietDeCuongFormSet(instance=de_cuong, prefix='noidungs')
        danh_gia_formset = HinhThucDanhGiaFormSet(instance=de_cuong, prefix='danhgias')
        tai_lieu_formset = DeCuongTaiLieuFormSet(instance=de_cuong, prefix='tailieus')

    context = {
        'form': form,
        'clo_formset': clo_formset,
        'noi_dung_formset': noi_dung_formset,
        'danh_gia_formset': danh_gia_formset,
        'tai_lieu_formset': tai_lieu_formset,
        'hoc_phan': hoc_phan,
        'de_cuong': None, # No existing de_cuong object yet
        'page_title': f'Thêm Đề cương cho học phần: {hoc_phan.ten_hoc_phan}',
        'is_new': True
    }
    return render(request, 'daotao/de_cuong_form.html', context)

@login_required
@permission_required('daotao.change_decuonghocphan', raise_exception=True)
def sua_de_cuong(request, pk_de_cuong):
    de_cuong = get_object_or_404(DeCuongHocPhan, pk=pk_de_cuong)
    hoc_phan = de_cuong.hoc_phan

    # Chuẩn bị form_kwargs để truyền instance de_cuong vào ChuanDauRaHocPhanForm
    clo_form_kwargs = {'de_cuong': de_cuong}

    if request.method == 'POST':
        form = DeCuongHocPhanForm(request.POST, instance=de_cuong)
        # Truyền form_kwargs khi khởi tạo formset
        clo_formset = ChuanDauRaHocPhanFormSet(request.POST, instance=de_cuong, prefix='clos', form_kwargs=clo_form_kwargs)
        noi_dung_formset = NoiDungChiTietDeCuongFormSet(request.POST, instance=de_cuong, prefix='noidungs')
        hinh_thuc_danh_gia_formset = HinhThucDanhGiaFormSet(request.POST, instance=de_cuong, prefix='danhgias')

        # The tai_lieu_formset is no longer needed as its functionality is merged into the main form.
        if form.is_valid() and clo_formset.is_valid() and noi_dung_formset.is_valid() and hinh_thuc_danh_gia_formset.is_valid():
            # The custom save() method in DeCuongHocPhanForm now handles saving the document relations.
            form.save()
            clo_formset.save()
            noi_dung_formset.save()
            hinh_thuc_danh_gia_formset.save()
            
            messages.success(request, f"Đã cập nhật đề cương '{de_cuong.ten_de_cuong_phien_ban}' thành công!")
            return redirect('daotao:sua_de_cuong', pk_de_cuong=de_cuong.pk)
        else:
            # In ra lỗi để debug
            print("Form errors:", form.errors)
            print("CLO Formset errors:", clo_formset.errors)
            print("Noi Dung Formset errors:", noi_dung_formset.errors)
            print("Hinh Thuc Danh Gia Formset errors:", hinh_thuc_danh_gia_formset.errors)
            messages.error(request, "Có lỗi xảy ra khi cập nhật đề cương. Vui lòng kiểm tra lại các trường.")
    else:
        form = DeCuongHocPhanForm(instance=de_cuong)
        # Truyền form_kwargs khi khởi tạo formset
        clo_formset = ChuanDauRaHocPhanFormSet(instance=de_cuong, prefix='clos', form_kwargs=clo_form_kwargs)
        noi_dung_formset = NoiDungChiTietDeCuongFormSet(instance=de_cuong, prefix='noidungs')
        hinh_thuc_danh_gia_formset = HinhThucDanhGiaFormSet(instance=de_cuong, prefix='danhgias')

    clo_groups = {
        'KT': 'Về kiến thức',
        'KN': 'Về kỹ năng',
        'TD': 'Về thái độ',
    }

    # Set initial values for the form based on the JSON state provided
    if not form.initial.get('tom_tat_noi_dung'):
        form.initial['tom_tat_noi_dung'] = hoc_phan.mo_ta_hoc_phan or ''

    context = {
        'form': form,
        'clo_formset': clo_formset,
        # 'tai_lieu_formset' is removed as it's no longer used
        'noi_dung_formset': noi_dung_formset,
        'hinh_thuc_danh_gia_formset': hinh_thuc_danh_gia_formset,
        'hoc_phan': hoc_phan,
        'de_cuong': de_cuong,
        'page_title': f'Cập nhật Đề cương chi tiết: {hoc_phan.ten_hoc_phan}',
        'is_new': False,
        'clo_groups': clo_groups,
    }
    return render(request, 'daotao/de_cuong_form.html', context)

@login_required
@permission_required('daotao.change_decuonghocphan', raise_exception=True) # Or a more specific permission
def submit_for_approval(request, pk_de_cuong):
    de_cuong = get_object_or_404(DeCuongHocPhan, pk=pk_de_cuong)
    if de_cuong.trang_thai == 'DRAFT' or de_cuong.trang_thai == 'REJECTED':
        de_cuong.trang_thai = 'PENDING_APPROVAL'
        de_cuong.save()
        messages.success(request, f"Đã gửi duyệt đề cương '{de_cuong.ten_de_cuong_phien_ban}'.")
    else:
        messages.warning(request, "Đề cương không ở trạng thái có thể gửi duyệt.")
    return redirect('daotao:danh_sach_de_cuong', pk_hoc_phan=de_cuong.hoc_phan.pk)

@login_required
@permission_required('daotao.can_approve_decuong', raise_exception=True) # Custom permission
def approve_de_cuong(request, pk_de_cuong):
    de_cuong = get_object_or_404(DeCuongHocPhan, pk=pk_de_cuong)
    if de_cuong.trang_thai == 'PENDING_APPROVAL':
        de_cuong.trang_thai = 'APPROVED'
        de_cuong.nguoi_phe_duyet = request.user
        de_cuong.ngay_phe_duyet = timezone.now()
        de_cuong.save()
        messages.success(request, f"Đã phê duyệt đề cương '{de_cuong.ten_de_cuong_phien_ban}'.")
    else:
        messages.warning(request, "Đề cương không ở trạng thái chờ duyệt.")
    return redirect('daotao:danh_sach_de_cuong', pk_hoc_phan=de_cuong.hoc_phan.pk)

@login_required
@permission_required('daotao.can_approve_decuong', raise_exception=True) # Custom permission
def reject_de_cuong(request, pk_de_cuong):
    de_cuong = get_object_or_404(DeCuongHocPhan, pk=pk_de_cuong)
    if de_cuong.trang_thai == 'PENDING_APPROVAL':
        de_cuong.trang_thai = 'REJECTED'
        de_cuong.save()
        messages.info(request, f"Đã từ chối đề cương '{de_cuong.ten_de_cuong_phien_ban}'.")
    else:
        messages.warning(request, "Đề cương không ở trạng thái chờ duyệt.")
    return redirect('daotao:danh_sach_de_cuong', pk_hoc_phan=de_cuong.hoc_phan.pk)

def xoa_de_cuong(request, pk_de_cuong):
    pass
