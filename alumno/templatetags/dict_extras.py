from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    """Permite acceder a un diccionario por clave en el template: {{ dict|dict_get:clave }}"""
    if d is None:
        return None
    return d.get(key, [])
