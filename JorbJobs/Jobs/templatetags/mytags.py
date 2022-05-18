import re

from humanize import intcomma
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def num_space(value):
    return intcomma(value)


@register.filter
def get_skills(value):
    value = re.sub(r"\s+", u",", value)
    skills = value.split(',')
    return skills


@register.filter
def count_items(value):
    return len(value)
