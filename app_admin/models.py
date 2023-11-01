import django.forms
from django.db import models
from django.contrib import admin

import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import (MinLengthValidator, MinValueValidator, MaxValueValidator)


class Category(models.Model):
    number = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, unique=True, verbose_name="Uue kategooria nimetus")

    def __str__(self):
        """ Admin page show info """
        return self.name

    class Meta:
        """ Default result ordering """
        ordering = ['name']
        verbose_name_plural = 'categories'


class MenuCategory(models.Model):
    teema_paev = models.CharField(max_length=1000,null=True, blank=True, unique=True, verbose_name="Teemapäeva nimetus")
    peakokk = models.CharField(max_length=500, null=True, blank=True, unique=True, verbose_name="Peakokk soovitab")
    kes_tegid = models.CharField(max_length=1000, null=True, blank=True, unique=True, verbose_name="Toidud tegid")
    def __str__(self):
        """ Admin page show info """
        return self.teema_paev

    class Meta:
        """ Default result ordering """
        fields = ('date', 'topic', 'chef', 'student')
        widgets = {
            'date':django.forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),}

class Foods_listing(models.Model):
    kuupaev = datetime.date.today().year
    toidu_nimetus = models.CharField(max_length=1000,null=True, blank=True, unique=True, verbose_name="Sisesta toidu nimetus")
    taishind = models.IntegerField(null=False, blank=True)
    poolhind = models.IntegerField(null=False, blank=True)
    on_menuus = True

