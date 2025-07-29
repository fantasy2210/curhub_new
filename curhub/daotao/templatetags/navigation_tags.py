from django import template
from daotao.navigation import get_menu_items

register = template.Library()

@register.inclusion_tag('daotao/partials/_sidebar_menu.html', takes_context=True)
def render_sidebar_menu(context):
    user = context['request'].user
    return {'menu_items': get_menu_items(user)}
