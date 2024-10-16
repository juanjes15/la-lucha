from django import template
import locale

register = template.Library()

@register.filter(name='format_number')
def format_number(value):
    try:
        locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')  # Ajusta esto según tu configuración regional
        return locale.format_string("%d", value, grouping=True)
    except:
        return value