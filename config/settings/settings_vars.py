from django import template
from django.conf import settings
from config.settings.local import URL_FRONT

register = template.Library()



@register.simple_tag
def get_settings_var(name):
    return getattr(settings, name)
