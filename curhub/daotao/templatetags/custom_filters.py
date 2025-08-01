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
