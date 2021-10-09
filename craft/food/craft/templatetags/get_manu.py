from django import template
from craft.models import MenuCategory,Product


register = template.Library()

# @register.inclusion_tag('craft/menu.html')
# def get_menu_category():
#     menu = MenuCategory.objects.all()
#     return {'menu': menu}
