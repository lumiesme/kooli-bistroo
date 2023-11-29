import urllib.parse
from urllib.request import urlopen
import json
from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.urls import reverse

from .forms import FoodMenuFormset
from .models import Category, FoodsListing
from django.contrib import messages
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView, DetailView
from django.conf import settings
from django.core.paginator import Paginator
from .models import *

class HomeView(TemplateView):
    template_name = 'app_admin/index.html'

class FoodListView(ListView):
    # model_list.html -> student_list.html
    template_name = 'app_admin/food_list.html'
    model = Category # Connected to Models Student-siit tuleb info
    queryset = Category.objects.order_by('name')  # nime jargi sorteeritud, result ordered by name
    context_object_name = 'categories'  # object_list is default
    paginate_by = 10  # 10 per page in ListView

class CategoryCreateView(CreateView):
    template_name = 'app_admin/category_create.html'
    fields = "__all__"
    #form_class = CategoryCreateForm
    model = Category
    success_url = reverse_lazy('app_admin:food_list')

class FoodUpdateView(UpdateView):
    template_name = 'app_admin/food_update.html'
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('app_admin:food_list')

class FoodDeleteView(DeleteView):
    template_name = 'app_admin/food_delete.html'
    model = Category
    success_url = reverse_lazy('app_admin:food_list')

class MenuCategories(CreateView):
    template_name = 'app_admin/menu_header.html'
    success_url = reverse_lazy('app_admin:food_list')
    queryset = MenuCategory.objects.order_by('teema_paev')
    fields = "__all__"

class FoodsList(ListView):
    template_name = 'app_admin/foods_name_listing.html'
    model = FoodsListing
    #queryset = FoodsListing.objects.order_by('toidu_nimetus')
    context_object_name = 'foods'  # Update this line
    #paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context variables here if needed
        return context


class Foods(CreateView):
    template_name = 'app_admin/food_create.html'
    model = FoodsListing
    fields = '__all__'
    # context_object_name = FoodsListing
    success_url = reverse_lazy('app_admin:foods_name_listing')

class FoodsUpdate(UpdateView):
    model = FoodsListing
    template_name = 'app_admin/foods_name_listing_update.html'
    fields = '__all__'  # or fields = ['toidu_nimetus', 'taishind', 'poolhind', 'kategooria']
    success_url = reverse_lazy('app_admin:foods_name_listing')

class FoodsDelete(DeleteView):
    model = FoodsListing
    template_name = 'app_admin/foods_name_listing_delete.html'
    success_url = reverse_lazy('app_admin:foods_name_listing')


class TodaysMenuCreateView(CreateView):
    model = MenuCategory
    template_name = 'app_admin/todays_menu_create.html'
    success_url = reverse_lazy('app_admin:todays_menu_list')
    fields = '__all__'

class TodaysMenuListView(ListView):
    model = Menu
    template_name = 'app_admin/todays_menu_list.html'
    context_object_name = 'menucategory'  # object_list is default
    paginate_by = 10  # 10 per page in ListView

    def get_queryset(self):
        return Menu.objects.order_by('menuu__date')  # nime jargi sorteeritud, result ordered by name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dates'] = MenuData.objects.all()  # Assuming you want to display all dates
        return context
class TodaysMenuDetailView(DetailView):
    model = Menu
    template_name = 'app_admin/todays_menu_detail.html'

class TodaysMenuUpdateView(UpdateView):
    model = Menu
    template_name = 'app_admin/todays_menu_update.html'
    fields = '__all__'
    success_url = reverse_lazy('app_admin:todays_menu_list')
class TodaysMenuDeleteView(DeleteView):
    model = Menu
    template_name = 'app_admin/todays_menu_delete.html'
    fields = '__all__'
    success_url = reverse_lazy('app_admin:todays_menu_list')

class MenuAddView(CreateView):
    model = Menu
    template_name = 'app_admin/menu_add.html'
    fields = '__all__'
    success_url = reverse_lazy('app_admin:todays_menu_list')
