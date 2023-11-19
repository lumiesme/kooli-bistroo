import urllib.parse
from urllib.request import urlopen
import json

from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.conf import settings
from django.core.paginator import Paginator
from .models import *


class HomeView(TemplateView):
    template_name = 'app_public/index.html'

#class FoodCategory(models.Model):
    #categoryname = models.CharField(max_length=100)
    #categorydetails = models.CharField(max_length=1000)
    #categoryimage = models.ImageField(default='cat_def.jpg',
    #upload_to='catimg')

    class Meta:
        verbose_name = 'Food Category'

    def __str__(self):
        return self.categoryname