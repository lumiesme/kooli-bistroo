from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput, TextInput
from django.forms.models import inlineformset_factory
from .models import MenuItem, Menu, Heading, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['number', 'name']

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
                f"Selle' {category}' kategooriaga menüü antud kuupäevaga juba eksiteerib. Lisage toitusid uuendades menüüd. "
            )

        return cleaned_data
# MenuItemFormSet = inlineformset_factory(Menu, MenuItem, form=MenuForm, extra=1, can_delete=False)
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['food', 'full_price', 'half_price', 'show_in_menu']

MenuFormset = inlineformset_factory(parent_model=Menu, model=MenuItem, fields=('food', 'full_price', 'half_price', 'show_in_menu'))

class HeadingForm(forms.ModelForm):
    class CustomDateInput(DateInput):
        input_type = 'date'

        def __init__(self, *args, **kwargs):
            kwargs['format'] = '%d.%m.%Y'  # Estonian date format
            super().__init__(*args, **kwargs)
    class Meta:
        model = Heading
        fields = ['date', 'topic', 'chef', 'student']
        widgets = {
            #'date': forms.DateInput(attrs={'class': 'form-control', 'id': 'date'}),- ei tööta
            'date': DateInput(attrs={'type': 'date'}, format='%d.%m.%Y'), # vale vorming
            #'date': TextInput(attrs={'type': 'text', 'id': 'date', 'class': 'form-control', 'placeholder': 'Vali kuupaev'}),- ei tööta
        }
    def clean(self):
        super(HeadingForm, self).clean()
        topic = self.cleaned_data['topic']
        chef = self.cleaned_data['chef']
        if (topic is None and chef is not None) or (topic is not None and chef is None):
            self.add_error('topic', ValidationError('Teemapaev ja peakokk molemad peavad olema taidetud ja mitte ainult uks kahest'))

        return self.cleaned_data