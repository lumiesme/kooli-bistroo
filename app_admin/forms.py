from django import forms
from django.forms import DateInput
from django.forms.models import inlineformset_factory
from .models import MenuItem, Menu, Heading



class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['date', 'category']



class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['food', 'full_price', 'half_price', 'show_in_menu']


MenuFormset = inlineformset_factory(parent_model=Menu, model=MenuItem, fields=('food', 'full_price', 'half_price', 'show_in_menu'))


class HeadingForm(forms.ModelForm):
    class Meta:
        model = Heading
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
