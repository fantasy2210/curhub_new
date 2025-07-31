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
        # Filter out None values before summing
        return sum(getattr(obj, arg) or 0 for obj in value)
    except (AttributeError, TypeError):
        return 0

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Returns the value of a dictionary key.
    Usage: {{ my_dict|get_item:my_key }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
