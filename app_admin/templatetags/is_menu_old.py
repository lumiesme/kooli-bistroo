from datetime import datetime, date
from django import template

register = template.Library()

@register.filter
def is_menu_old(menu_date):
    # Ensure menu_date is in the format 'd.m.Y'
    try:
        date_object = datetime.strptime(menu_date, '%d.%m.%Y').date()
        today = date.today()
        return date_object < today
    except ValueError:
        # Handle the case where the date format is incorrect
        return False