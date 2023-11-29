from django.forms.models import inlineformset_factory
from .models import Menu, MenuCategory

FoodMenuFormset = inlineformset_factory(MenuCategory, fields=('andmed','toit', 't_hind', 'p_hind', 'naita_menuus'), model=Menu)
