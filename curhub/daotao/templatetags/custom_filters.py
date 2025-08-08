from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def sum_attribute(value, arg):
    """
    Sum an attribute of a list of objects.
    Usage: {{ my_list|sum_attribute:'my_attribute' }}
    """
    try:
        return sum(getattr(obj, arg) for obj in value)
    except (AttributeError, TypeError):
        return 0

@register.filter(name='trang_thai_to_badge')
def trang_thai_to_badge(trang_thai):
    if trang_thai == 'Đã có kế hoạch':
        return 'badge-success'
    elif trang_thai == 'Chưa có kế hoạch':
        return 'badge-warning'
    elif trang_thai == 'Không còn áp dụng':
        return 'badge-danger'
    else:
        return 'badge-secondary'

@register.filter(name='sum_credits')
def sum_credits(hoc_phan_list):
    """
    Sums the 'tong_so_tin_chi_apdung' for a list of ChiTietHocPhanTrongCTDT objects.
    """
    total = 0
    for hp in hoc_phan_list:
        total += hp.tong_so_tin_chi_apdung or 0
    return total
