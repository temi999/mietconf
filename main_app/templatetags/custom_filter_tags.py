from django import template

register = template.Library()

@register.filter
def show_on_materials(value):
    return value.filter(show_on_materials_page=True)