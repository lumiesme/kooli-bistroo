import django.forms
from django.db import models
from django.contrib import admin
import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import (MinLengthValidator, MinValueValidator, MaxValueValidator)


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


class MenuCategory(models.Model):
    teema_paev = models.CharField(max_length=255,null=True, blank=True, unique=True, verbose_name="Teemapäeva nimetus")
    peakokk = models.CharField(max_length=500, null=True, blank=True, unique=True, verbose_name="Peakokk soovitab")
    kes_tegid = models.CharField(max_length=1000, null=True, blank=True, unique=True, verbose_name="Toidud tegid")

class FoodsListing(models.Model):
    toidu_nimetus = models.CharField(max_length=255, verbose_name="Sisesta toidu nimetus")
    taishind = models.FloatField(null=False, blank=True)
    poolhind = models.FloatField(null=False, blank=True)
    kategooria = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, verbose_name="Kategooria")
    def __str__(self):
        """ Admin page show info """
        return self.toidu_nimetus