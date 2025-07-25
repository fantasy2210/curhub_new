from django import template

register = template.Library()

@register.filter(name='trang_thai_to_badge')
def trang_thai_to_badge(trang_thai):
    if trang_thai == 'DRAFT':
        return 'badge-secondary'
    elif trang_thai == 'PENDING_APPROVAL':
        return 'badge-warning'
    elif trang_thai == 'APPROVED':
        return 'badge-success'
    elif trang_thai == 'REJECTED':
        return 'badge-danger'
    elif trang_thai == 'ARCHIVED':
        return 'badge-info'
    return 'badge-light'

@register.filter(name='sum_attribute')
def sum_attribute(value, arg):
    """
    Sum the value of an attribute from a list of objects.
    Usage: {{ my_list|sum_attribute:'my_attribute' }}
    """
    try:
        return sum(getattr(obj, arg) for obj in value)
    except (AttributeError, TypeError):
        return 0
