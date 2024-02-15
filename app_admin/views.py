from datetime import datetime
from urllib import request

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView, DetailView
from django.db.models import Count, Q
from .forms import MenuFormset, MenuForm, HeadingForm
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class ManagerRequiredMixin(UserPassesTestMixin):
    """ Test: user in group Writer"""
    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()

class WriterRequiredMixin(UserPassesTestMixin):
    """ Test: user in group Writer"""
    def test_func(self):
        return self.request.user.groups.filter(name='Writer').exists()
class EditorRequiredMixin(UserPassesTestMixin):
    # delete view
    def test_func(self):
        return self.request.user.groups.filter(name='Editor').exists()

class HomeView(TemplateView):
    template_name = 'app_admin/index.html'

class CategoryListView(ListView):
    template_name = 'app_admin/category_list.html'
    model = Category
    queryset = Category.objects.order_by('number')
    context_object_name = 'categories'
    paginate_by = 10

class CategoryCreateView(ManagerRequiredMixin, WriterRequiredMixin,CreateView):
    template_name = 'app_admin/category_create.html'
    fields = "__all__"
    model = Category
    success_url = reverse_lazy('app_admin:category_list')


class CategoryUpdateView(ManagerRequiredMixin, EditorRequiredMixin, UpdateView):
    template_name = 'app_admin/category_update.html'
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('app_admin:category_list')


class CategoryDeleteView(ManagerRequiredMixin,EditorRequiredMixin, DeleteView):
    template_name = 'app_admin/category_delete.html'
    model = Category
    success_url = reverse_lazy('app_admin:category_list')


class HeadingCreateView(ManagerRequiredMixin, WriterRequiredMixin,CreateView):
    model = Heading
    form_class = HeadingForm
    template_name = 'app_admin/heading_create.html'
    success_url = reverse_lazy('app_admin:heading_list')
    #queryset = MenuItem.objects.order_by('menu__date_id')


class HeadingListView(ManagerRequiredMixin, ListView):
    template_name = 'app_admin/heading_list.html'
    model = Heading
    fields = '__all__'
    queryset = Heading.objects.order_by('date')
    context_object_name = 'heading'

    #paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context variables here if needed
        return context


class HeadingDetailView(ManagerRequiredMixin, DetailView):
    template_name = 'app_admin/heading_detail.html'
    model = Heading
    context_object_name = 'heading'

class HeadingUpdateView(ManagerRequiredMixin, UpdateView):
    model = Heading
    form_class = HeadingForm
    template_name = 'app_admin/heading_update.html'
    success_url = reverse_lazy('app_admin:heading_list')
    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f"{form.instance.date.strftime('%d.%m.%Y')} pealkirjad on uuendatud"
        )
        return super().form_valid(form)

class HeadingDeleteView(ManagerRequiredMixin, EditorRequiredMixin, DeleteView):
    model = Heading
    template_name = 'app_admin/heading_delete.html'
    success_url = reverse_lazy('app_admin:heading_list')


class MenuCreateView(ManagerRequiredMixin, WriterRequiredMixin, CreateView):
    model = Menu
    template_name = 'app_admin/menu_add.html'
    form_class = MenuForm
    success_url = reverse_lazy('app_admin:menu_list')

    def form_valid(self, form):
        # Create a Menu instance and associate it with the Heading
        menu = form.save()

        # Pass the instance argument to associate the formset with the created Menu instance
        formset = MenuFormset(self.request.POST, instance=menu)
        if formset.is_valid():
            formset.save()

            # Save the form and handle success messages
            response = super().form_valid(form)
            messages.success(self.request, 'The menu has been added')
            return response

        # If the formset is not valid, delete the menu instance
        menu.delete()
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menuformset'] = MenuFormset()
        return context

class MenuListView(ManagerRequiredMixin, ListView):
    template_name = 'app_admin/menu_list.html'
    model = Menu
    context_object_name = 'menu_list'

    def get_queryset(self):
        # Ensure that Menu objects are properly ordered by date or category
        queryset = super().get_queryset()
        queryset = queryset.order_by('date', 'category__name')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context




class MenuDetailView(ManagerRequiredMixin, DetailView):
    model = Menu
    template_name = 'app_admin/menu_detail.html'
    context_object_name = 'menu'


class MenuUpdateView(ManagerRequiredMixin, UpdateView):
    model = Menu
    template_name = 'app_admin/menu_update.html'
    form_class = MenuForm
    success_url = reverse_lazy('app_admin:menu_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Menu.objects.all())
        self.menuitem_formset = MenuFormset(instance=self.object)
        return super().get(request, *args, *kwargs)
    def post(self, request, *args, **kwargs):
        self.object= self.get_object(queryset=Menu.objects.all())
        self.menuitem_formset = MenuFormset(request.POST, instance=self.object)
        return super().post(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menuitem_formset'] = self.menuitem_formset
        return context

    def form_valid(self, form):

        form.save()
        self.menuitem_formset.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Muudatused on salvestatud"
        )

        return HttpResponseRedirect(self.get_success_url())
    def get_success_url(self):
        return reverse('app_admin:menu_detail', kwargs={'pk': self.object.pk})



class MenuDeleteView(ManagerRequiredMixin, EditorRequiredMixin, DeleteView):
    model = Menu
    template_name = 'app_admin/menu_delete.html'
    success_url = reverse_lazy('app_admin:menu_list')

class ArchivePage(ListView):
    model = Heading
    template_name = 'app_admin/archive.html'

    def get_context_data(self, **kwargs):
        context = super(ArchivePage, self).get_context_data(**kwargs)
        context['unique_dates'] = Heading.objects.all()
        return context

class SearchResultPage(ManagerRequiredMixin, ListView):
    model = MenuItem
    template_name = 'app_admin/archive_search.html'
    allow_empty = False  #tuhje paringuid ei lubata

    # https://labpys.com/how-to-implement-join-operations-in-django-orm/
    def get_queryset(self):
        query = self.request.GET.get('q')  # info from form - archive page
        object_list = None
        if len(query) > 2:
            object_list = MenuItem.objects.select_related('menu').filter(food__icontains=query)

        return object_list

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(SearchResultPage, self).dispatch(request, *args, **kwargs)
        except Http404:
            return redirect('app_admin:archive_page')

class OldMenuPage(ManagerRequiredMixin, ListView):
    model = Menu
    template_name = 'app_admin/archive_menu.html'

    def get_context_data(self, **kwargs):
        all_data = None
        query = self.request.GET.get('date')

        if not query:
            query = self.kwargs['date']

        parts = query.split('.')
        today_string = parts[2] + '-' + parts[1] + '-' + parts[0]
        #estonian_date = datetime.strptime(today_string, '%Y-%m-%d').strftime('%d.%m.%Y')
        estonian_date = query

        try:
            today_menu_id = Heading.objects.get(date=today_string)
            today_menuheadlines = Heading.objects.filter(date=today_string).values('date', 'topic', 'chef', 'student')

            today_all_categories = Menu.objects.filter(date_id=today_menu_id)

            all_data = (MenuItem.objects.filter(Q(menu_id__in=today_all_categories))
                        .values('menu_id', 'food', 'full_price', 'half_price', 'show_in_menu',
                                'menu__category__name', 'id', 'menu__category_id')
                        .annotate(dcount=Count('menu_id')).order_by('menu__category_id', 'id'))
        except Menu.DoesNotExist:
            today_menuheadlines = None

        context = {
            'object_list': all_data,
            'menuheadlines': today_menuheadlines,
            'estonian_date': estonian_date,
            'today_string': today_string
        }

        return context