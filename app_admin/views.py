from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from django.contrib import messages
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView, DetailView
from .models import *
from .forms import MenuFormset, MenuForm, HeadingForm
from .models import MenuItem, Heading, Menu



class HomeView(TemplateView):
    template_name = 'app_admin/index.html'

class CategoryListView(ListView):
    template_name = 'app_admin/category_list.html'
    model = Category
    queryset = Category.objects.order_by('number')
    context_object_name = 'categories'
    paginate_by = 10

class CategoryCreateView(CreateView):
    template_name = 'app_admin/category_create.html'
    fields = "__all__"
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
    model = Heading
    form_class = HeadingForm
    template_name = 'app_admin/heading_create.html'
    success_url = reverse_lazy('app_admin:heading_list')
    #queryset = MenuItem.objects.order_by('menu__date_id')


class HeadingListView(ListView):
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


class HeadingDetailView(DetailView):
    template_name = 'app_admin/heading_detail.html'
    model = Heading
    context_object_name = 'heading'

class HeadingUpdateView(UpdateView):
    model = Heading
    form_class = HeadingForm
    template_name = 'app_admin/heading_update.html'
    success_url = reverse_lazy('app_admin:heading_list')


class HeadingDeleteView(DeleteView):
    model = Heading
    template_name = 'app_admin/heading_delete.html'
    success_url = reverse_lazy('app_admin:heading_list')


class MenuCreateView(CreateView):
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

class MenuListView(ListView):
    template_name = 'app_admin/menu_list.html'
    model = Menu  # Change the model to Menu
    context_object_name = 'menu_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context variables here if needed
        return context




class MenuDetailView(DetailView):
    model = Menu
    template_name = 'app_admin/menu_detail.html'
    context_object_name = 'menu'


class MenuUpdateView(UpdateView):
    model = Menu
    template_name = 'app_admin/menu_update.html'
    form_class = MenuForm
    success_url = reverse_lazy('app_admin:menu_list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menuitem_formset'] = MenuFormset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        menuitem_formset = context['menuitem_formset']

        if menuitem_formset.is_valid():
            form.save()
            menuitem_formset.save()

            messages.success(self.request, 'Menu and menu items were updated successfully.')
            return super().form_valid(form)

        return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Menu, pk=pk)


class MenuItemUpdateView(FormView):
    template_name = 'app_admin/menu_update.html'
    form_class = MenuFormset
    success_url = reverse_lazy('app_admin:heading_list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Menu items were updated successfully.')
        return super().form_valid(form)

    def get_initial(self):
        menu_id = self.kwargs.get('pk')
        menu = get_object_or_404(Menu, pk=menu_id)
        self.initial = {'menu': menu}
        return self.initial


class MenuDeleteView(DeleteView):
    model = Menu
    template_name = 'app_admin/menu_delete.html'
    success_url = reverse_lazy('app_admin:menu_list')