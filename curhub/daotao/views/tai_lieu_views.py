from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import TaiLieuHocTap
from ..forms import TaiLieuHocTapForm
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
# @permission_required('daotao.view_tailieuhoctap', raise_exception=True)
def danh_sach_tai_lieu(request):
    tai_lieu_list = TaiLieuHocTap.objects.all()
    
    query_search = request.GET.get('q', '')
    if query_search:
        tai_lieu_list = tai_lieu_list.filter(
            Q(nhan_de__icontains=query_search) |
            Q(tac_gia__icontains=query_search) |
            Q(tom_tat__icontains=query_search) |
            Q(nha_xuat_ban__icontains=query_search)
        )

    paginator = Paginator(tai_lieu_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'page_title': 'Thư viện Tài liệu học tập',
        'query_search': query_search,
    }
    return render(request, 'daotao/danh_sach_tai_lieu.html', context)

@login_required
# @permission_required('daotao.add_tailieuhoctap', raise_exception=True)
def them_tai_lieu(request):
    if request.method == 'POST':
        form = TaiLieuHocTapForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã thêm tài liệu thành công!')
            return redirect('daotao:danh_sach_tai_lieu')
    else:
        form = TaiLieuHocTapForm()
    context = {
        'form': form,
        'page_title': 'Thêm Tài liệu học tập',
    }
    return render(request, 'daotao/tai_lieu_form.html', context)

@login_required
# @permission_required('daotao.change_tailieuhoctap', raise_exception=True)
def sua_tai_lieu(request, pk):
    tai_lieu = get_object_or_404(TaiLieuHocTap, pk=pk)
    if request.method == 'POST':
        form = TaiLieuHocTapForm(request.POST, instance=tai_lieu)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã cập nhật tài liệu thành công!')
            return redirect('daotao:danh_sach_tai_lieu')
    else:
        form = TaiLieuHocTapForm(instance=tai_lieu)
    context = {
        'form': form,
        'page_title': 'Sửa Tài liệu học tập',
    }
    return render(request, 'daotao/tai_lieu_form.html', context)

@login_required
# @permission_required('daotao.delete_tailieuhoctap', raise_exception=True)
def xoa_tai_lieu(request, pk):
    tai_lieu = get_object_or_404(TaiLieuHocTap, pk=pk)
    if request.method == 'POST':
        tai_lieu.delete()
        messages.success(request, f"Đã xóa tài liệu '{tai_lieu.nhan_de}' thành công.")
        return redirect('daotao:danh_sach_tai_lieu')
    context = {
        'object': tai_lieu,
        'page_title': 'Xác nhận xóa Tài liệu',
        'confirm_message': f"Bạn có chắc chắn muốn xóa tài liệu '{tai_lieu.nhan_de}' không?"
    }
    return render(request, 'daotao/confirm_delete.html', context)
