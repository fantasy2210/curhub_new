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
    HinhThucDanhGiaFormSet
)
from django.core.paginator import Paginator
from django.db.models import Q

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
    if request.method == 'POST':
        form = DeCuongHocPhanForm(request.POST)
        if form.is_valid():
            de_cuong = form.save(commit=False)
            de_cuong.hoc_phan = hoc_phan
            de_cuong.save()
            messages.success(request, f"Đã thêm đề cương '{de_cuong.ten_de_cuong_phien_ban}' thành công!")
            return redirect('daotao:danh_sach_de_cuong', pk_hoc_phan=hoc_phan.pk)
        else:
            messages.error(request, "Có lỗi xảy ra khi thêm đề cương. Vui lòng kiểm tra lại các trường.")
    else:
        form = DeCuongHocPhanForm()
    context = {
        'form': form,
        'hoc_phan': hoc_phan,
        'page_title': f'Thêm Đề cương cho học phần: {hoc_phan.ten_hoc_phan}'
    }
    return render(request, 'daotao/de_cuong_form.html', context)

@login_required
@permission_required('daotao.change_decuonghocphan', raise_exception=True)
def sua_de_cuong(request, pk_de_cuong):
    de_cuong = get_object_or_404(DeCuongHocPhan, pk=pk_de_cuong)
    hoc_phan = de_cuong.hoc_phan
    if request.method == 'POST':
        form = DeCuongHocPhanForm(request.POST, instance=de_cuong)
        if form.is_valid():
            form.save()
            messages.success(request, f"Đã cập nhật đề cương '{de_cuong.ten_de_cuong_phien_ban}' thành công!")
            return redirect('daotao:danh_sach_de_cuong', pk_hoc_phan=hoc_phan.pk)
        else:
            messages.error(request, "Có lỗi xảy ra khi cập nhật đề cương. Vui lòng kiểm tra lại các trường.")
    else:
        form = DeCuongHocPhanForm(instance=de_cuong)
    context = {
        'form': form,
        'hoc_phan': hoc_phan,
        'de_cuong': de_cuong,
        'page_title': f'Cập nhật Đề cương: {de_cuong.ten_de_cuong_phien_ban}'
    }
    return render(request, 'daotao/de_cuong_form.html', context)

def xoa_de_cuong(request, pk_de_cuong):
    pass
