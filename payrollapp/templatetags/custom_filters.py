# custom_filters.py

from django import template

register = template.Library()


@register.filter(name='is_hr_admin_or_founder')
def is_hr_admin_or_founder(user):
    return user.groups.filter(name__in=['HR Admin', 'Founder']).exists()
