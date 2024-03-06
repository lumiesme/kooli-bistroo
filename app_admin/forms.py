from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput
from django.forms.models import inlineformset_factory
from .models import MenuItem, Menu, Heading, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['number', 'name']

        widgets = {
            'number': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control', 'placeholder': 'Sisesta ID'}),
            'name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': ''}),

        }

        def clean(self):
            cleaned_data = super(CategoryForm, self).clean()
            number = self.cleaned_data['number']
            #category = self.cleaned_data['name']
            if Menu.objects.filter(number=number).exists():
                raise ValidationError(
                    f"Selle '{number}' id-ga kategooriaga on juba olemas! Palun lisage mingi teine ID "
                )

            return cleaned_data

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
        fields = ['date', 'topic', 'chef', 'student']
        widgets = {
            'date': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date', 'class': 'form-control', 'id': 'date'}),
            'topic': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': ''}),
            'chef': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'student': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            # Other widget definitions for other fields...
        }

    def clean(self):
        cleaned_data = super().clean()
        topic = cleaned_data.get('topic')
        chef = cleaned_data.get('chef')

        if (topic is None and chef is not None) or (topic is not None and chef is None):
            raise forms.ValidationError('Teemapaev ja peakokk molemad peavad olema taidetud ja mitte ainult uks kahest')

        return cleaned_data