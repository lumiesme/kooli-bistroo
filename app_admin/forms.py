from django import forms
from django.core.exceptions import ValidationError
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
        fields = ['date', 'topic', 'chef', 'student']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean(self):
        super(HeadingForm, self).clean()
        topic = self.cleaned_data['topic']
        chef = self.cleaned_data['chef']
        if (topic is None and chef is not None) or (topic is not None and chef is None):
            self.add_error('topic', ValidationError('Teemapaev ja peakokk molemad peavad olema taidetud ja mitte ainult uks kahest'))

        return self.cleaned_data