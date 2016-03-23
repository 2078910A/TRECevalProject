from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@stringfilter
def upper(value):
    return value.upper()

register.filter('upper', upper, is_safe=True)