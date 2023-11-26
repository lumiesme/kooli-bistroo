from django.forms.models import inlineformset_factory

from .models import FoodsListing, Menu

FoodMenuFormset = inlineformset_factory(FoodsListing, Menu, fields=('toit', 't_hind', 'p_hind', 'naita_menuus'))
