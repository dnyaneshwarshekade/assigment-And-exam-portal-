from django import template
from assignment.models import Assignment
from datetime import date

register = template.Library()
@register.filter
def isActive(last_date):
    if date.today() < last_date:
        return True
    else:
        return False 