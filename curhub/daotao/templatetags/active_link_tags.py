from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.filter
def startswith_filter(value, arg):
    """
    Checks if the value starts with the argument.
    Usage: {{ request.path|startswith_filter:'/admin/' }}
    """
    return value.startswith(arg)

@register.simple_tag(takes_context=True)
def active_link(context, view_name, *args, **kwargs):
    request = context.get('request')
    if not request:
        return ""
    try:
        path = reverse(view_name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        # If reverse fails, assume it's a static path
        path = view_name
    
    if request.path == path:
        return 'active'
    return ''
