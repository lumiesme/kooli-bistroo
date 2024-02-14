from django.views.generic import TemplateView
from django.db.models import Q, Count
from app_admin.models import MenuItem, Menu, Heading
from datetime import datetime
from django.shortcuts import render



class HomeViewPublic(TemplateView):
    template_name = 'app_public/index.html'
    model = Heading
    def get_context_data(self, **kwargs):
        all_data = None  # sisaldab kogu menüü infot
        today_string = datetime.today().strftime('%Y-%m-%d')  # 2024-01-24
        # today_string = '2024-01-25'  # testimiseks
        estonian_date = datetime.strptime(today_string, '%Y-%m-%d').strftime('%d.%m.%Y')
        try:
            # https://stackoverflow.com/questions/1542878/what-to-do-when-django-query-returns-none-it-gives-me-error
            # Kui tekib error
            today_menu_id = Heading.objects.get(date=today_string)  # vastuseks üks kirje või error
            today_menuheadlines = Heading.objects.filter(Q(date=today_string)).values('date', 'topic', 'chef',
                                                                                            'student')
            today_all_categories = Menu.objects.filter(date_id=today_menu_id)
            # https://stackoverflow.com/questions/3397170/
            all_data = (MenuItem.objects.filter(Q(menu_id__in=today_all_categories))
                        .values('menu_id', 'food', 'full_price', 'half_price', 'show_in_menu',
                                'menu__category__name', 'id', 'menu__category_id')
                        .annotate(dcount=Count('menu_id')).order_by('menu__category_id', 'id'))
            # print(today_all_categories)
        except Heading.DoesNotExist:
            today_menuheadlines = None

        context = {
            'object_list': all_data,
            'menuheadlines': today_menuheadlines,
            'estonian_date': estonian_date,
            'today_string': today_string
        }
        return context

def error_404(request, exception):
    return render(request, '404.html', {})

def error_500(request):
    return render(request, '500.html', {})