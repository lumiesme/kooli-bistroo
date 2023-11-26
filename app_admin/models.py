import django.forms
from django.db import models
from django.contrib import admin
import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import (MinLengthValidator, MinValueValidator, MaxValueValidator)
from django.urls import reverse


class Category(models.Model):
    number = models.IntegerField(null=True, blank=True, default=0)  # Add a default value here
    name = models.CharField(max_length=255, unique=True, verbose_name="Uue kategooria nimetus")

    def __str__(self):
        """ Admin page show info """
        return self.name

    #class Meta:
        #""" Default result ordering """
        #ordering = ['name']
        #verbose_name_plural = 'categories'
#category_choices = (name)


#class MenuCategoryChoices(models.Model):
    #choices = models.CharField(max_length=255, choices=category_choices, default="vali nimi")
class menuDate(models.Model):
    kuupaev =models.DateTimeField(null=False, blank=False)

class MenuCategory(models.Model):
    teema_paev = models.CharField(max_length=255,null=True, blank=True, unique=True, verbose_name="Teemapäeva nimetus")
    peakokk = models.CharField(max_length=500, null=True, blank=True, unique=True, verbose_name="Peakokk soovitab")
    kes_tegid = models.CharField(max_length=1000, null=True, blank=True, unique=True, verbose_name="Toidud tegid")
    #kuupaeva peaks ka sisaldama. see kuup peaksolema ka menuu kuupaevaga seotud
    date = models.ForeignKey(menuDate, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']


    def get_absolute_url(self):
        return reverse('app_admin:todays_menu_list')

    #def __str__(self):
        #return f'{self.date.strftime("%d.%m.%Y")}'
# toidu lisamine
class FoodsListing(models.Model):
    toidu_nimetus = models.CharField(max_length=255, verbose_name="Sisesta toidu nimetus")
    taishind = models.FloatField(null=False, blank=False)
    poolhind = models.FloatField(null=True, blank=True)
    kategooria = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, verbose_name="Kategooria")


# lisasin 22.11 kuni jarka def osani
    def get_absolute_url(self):
        return reverse('app_admin:foods_name_listing', kwargs={'pk':self.pk})
    def __str__(self):
        """ Admin page show info """
        return self.toidu_nimetus



class Menus(models.Model):
    date = models.ForeignKey(menuDate, on_delete=models.CASCADE) #see ongi seotud teemapaeva blokis oleva kuupaevaga
    # kategooria peaks ka olema siin, seotud kategooria tabeliga
    kategooria = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategooria")

    class Meta:
        ordering = ['date', 'kategooria']
    def __str__(self):
        return f'{self.date} - {self.kategooria}'

class Menu(models.Model):
    #esimese kahe valja asemel peaks olema date ja see date on forginkeyga Menus classist
    menuu = models.ForeignKey(Menus, on_delete=models.CASCADE, related_name='menuu')
    foods = models.ForeignKey(FoodsListing, on_delete=models.CASCADE)
    date = models.ForeignKey(Menus, on_delete=models.CASCADE, verbose_name="Valige menu kuupaev")
    toit = models.CharField(max_length=255, verbose_name="Sisesta toidu nimetus")
    t_hind = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)  #kumnendkohtade arv peaks olema kasutuses, mitte floatfield, vt pilte chatist
    p_hind = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    naita_menuus = models.BooleanField(default=True)


    class Meta:
        ordering = ['toit']

    def __str__(self):
        return f'{self.toit}'

