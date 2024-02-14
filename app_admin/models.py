from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

class Category(models.Model):
    number = models.PositiveIntegerField(verbose_name="Number")
    name = models.CharField(max_length=255, unique=True, verbose_name="Uue kategooria nimetus")

    def __str__(self):
        return self.name

class Heading(models.Model):
    date = models.DateField(blank=False, null=False, unique=True, verbose_name="Kuupäev")
    topic = models.CharField(max_length=100, null=True, blank=True, verbose_name="Teemapäev")
    chef = models.CharField(max_length=100, null=True, blank=True, verbose_name="Peakokk soovitab:")
    student = models.CharField(max_length=100, null=True, blank=True, verbose_name="Kes tegid:")

    def __str__(self):
        """ Admin page show info """
        #return f'{self.date}, {self.teema}, {self.soovitab}, {self.valmistas}'
        return f'{self.date.strftime("%d.%m.%Y")}'

    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse('app_admin:heading_list')

    def clean(self):
        if(self.topic is None and self.chef is not None) or (self.topic is not None and self.chef is None):
            raise ValidationError('Teemapaeva ja peakoka lahter peavad olema molemad taidetud!')


    def __str__(self):
        return f'{self.date.strftime("%d.%m.%Y")}'


class Menu(models.Model):
    date = models.ForeignKey(Heading, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date', 'category']

    def get_absolute_url(self):
        return reverse('app_admin:menu_update', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.date} {self.category}'


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menu_menuitem')
    food = models.CharField(max_length=255, verbose_name="Toit")
    full_price = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False, verbose_name="Suure hind")
    half_price = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Väikese hind")
    show_in_menu = models.BooleanField(default=True, verbose_name="Näita menüüs")

    class Meta:
        ordering = ['menu']

    def __str__(self):
        return f'{self.menu}'

