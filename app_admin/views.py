import urllib.parse
from urllib.request import urlopen
import json
from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.urls import reverse

from .models import Category, Heading
from django.contrib import messages
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView, DetailView
from django.conf import settings
from django.core.paginator import Paginator
from .models import *
from .forms import MenuFormset

class HomeView(TemplateView):
    template_name = 'app_admin/index.html'

class CategoryListView(ListView):
    # model_list.html -> student_list.html
    template_name = 'app_admin/category_list.html'
    model = Category # Connected to Models Student-siit tuleb info
    queryset = Category.objects.order_by('name')  # nime jargi sorteeritud, result ordered by name
    context_object_name = 'categories'  # object_list is default
    paginate_by = 10  # 10 per page in ListView

class CategoryCreateView(CreateView):
    template_name = 'app_admin/category_create.html'
    fields = "__all__"
    #form_class = CategoryCreateForm
    model = Category
    success_url = reverse_lazy('app_admin:category_list')

class CategoryUpdateView(UpdateView):
    template_name = 'app_admin/category_update.html'
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('app_admin:category_list')

class CategoryDeleteView(DeleteView):
    template_name = 'app_admin/category_delete.html'
    model = Category
    success_url = reverse_lazy('app_admin:category_list')

class HeadingCreateView(CreateView):
    template_name = 'app_admin/heading_create.html'
    success_url = reverse_lazy('app_admin:heading_list')
    queryset = MenuItem.objects.order_by('menu__date_id')
    fields = "__all__"

class HeadingListView(ListView):
    template_name = 'app_admin/heading_list.html'
    model = Heading
    fields = '__all__'
    queryset = Heading.objects.order_by('date')

    #paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context variables here if needed
        return context

class HeadingUpdateView(UpdateView):
    model = Heading
    template_name = 'app_admin/heading_update.html'
    fields = '__all__'  # or fields = ['toidu_nimetus', 'taishind', 'poolhind', 'kategooria']
    success_url = reverse_lazy('app_admin:foods_name_listing')

class HeadingDeleteView(DeleteView):
    model = Heading
    template_name = 'app_admin/heading_delete.html'
    success_url = reverse_lazy('app_admin:foods_name_listing')


class MenuCreateView(CreateView):
    model = MenuItem
    template_name = 'app_admin/menu_add.html'
    fields = ['food', 'full_price', "half_price"]

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'The menu has been added'
        )
        return super().form_valid(form)


class MenuUpdateView(SingleObjectMixin, FormView):
    model = MenuItem
    template_name = 'app_admin/menu_update.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=MenuItem.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=MenuItem.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return MenuFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes were saved.'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('app_admin:heading_list', kwargs={'pk': self.object.pk})

