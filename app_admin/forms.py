from django.forms.models import inlineformset_factory
from .models import MenuItem, Menu

MenuFormset = inlineformset_factory(parent_model=Menu, model=MenuItem, fields=('menu', 'full_price', 'half_price'))
