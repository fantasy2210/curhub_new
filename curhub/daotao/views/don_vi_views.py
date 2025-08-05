from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import DonViDaoTao
from ..forms import DonViDaoTaoForm

from django.db.models import Q

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
