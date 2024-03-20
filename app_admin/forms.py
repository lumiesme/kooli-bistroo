from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput
from django.forms.models import inlineformset_factory
from django.template.backends import django
import datetime
from .models import MenuItem, Menu, Heading, Category
from datetime import datetime

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['number', 'name']

        widgets = {
            'number': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control', 'placeholder': 'Sisesta ID'}),
            'name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Sisesta kategooria nimetus'}),

        }



class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['date', 'category']

    def clean(self):
        cleaned_data = super(MenuForm, self).clean()
        date = self.cleaned_data['date']
        category = self.cleaned_data['category']
        if Menu.objects.filter(date=date, category=category).exists():
            raise ValidationError(
                f"Selle' {category}' kategooriaga menüü antud kuupäevaga juba eksiteerib. Lisage toitusid juurde menüüd uuendades. "
            )

        return cleaned_data
# MenuItemFormSet = inlineformset_factory(Menu, MenuItem, form=MenuForm, extra=1, can_delete=False)
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['food', 'full_price', 'half_price', 'show_in_menu']

MenuFormset = inlineformset_factory(parent_model=Menu, model=MenuItem, fields=('food', 'full_price', 'half_price', 'show_in_menu'))


class HeadingForm(forms.ModelForm):
    class Meta:
        model = Heading
        fields = ('date', 'topic', 'chef', 'student')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'text',  'id': 'date', 'class': 'form-control',
                            'placeholder': 'Kliki kuupäeva valimiseks', 'readonly': 'readonly'}, format='%d.%m.%Y'),
            'topic': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': ''}),
            'chef': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'student': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        }
class HeadingUpdateForm(forms.ModelForm):
    class Meta:
        model = Heading
        fields = ['date', 'topic', 'chef', 'student']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'text', 'id': 'date', 'class': 'form-control', 'placeholder': 'Kliki kuupäeva valimiseks', 'autocomplete': 'off'}, format='%d.%m.%Y'),
            'topic': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': ''}),
            'chef': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'student': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        }

