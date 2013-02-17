from django import template

from tempus.utils import tempus_dumps


register = template.Library()


@register.simple_tag
def tempus(data, param_key='tempus', salt='tempus'):
    encrypted_data = tempus_dumps(data, salt=salt)
    return '%s=%s' % (param_key, encrypted_data)
