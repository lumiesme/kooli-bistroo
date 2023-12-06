from django.urls import path
from . import views

app_name = 'app_admin'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('category_list/', views.CategoryListView.as_view(), name= 'category_list'),
    path('category_create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category_update/<int:pk>', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category_delete/<int:pk>', views.CategoryDeleteView.as_view(), name='category_delete'),


    #path('/', views.MenuCategories.as_view(), name='menu_header'),

    path('heading_create/', views.HeadingCreateView.as_view(), name='heading_create'),
    path('heading_list/', views.HeadingListView.as_view(), name='heading_list'),
    path('heading_update/<int:pk>', views.HeadingUpdateView.as_view(), name='heading_update'),
    path('heading_delete/<int:pk>', views.HeadingDeleteView.as_view(), name='heading_delete'),


    path('menu_add/', views.MenuCreateView.as_view(), name='menu_add'),
    #path('todays_menu_list/', views.TodaysMenuListView.as_view(), name='todays_menu_list'),
    #path('todays_menu_detail/<int:pk>/', views.TodaysMenuDetailView.as_view(), name='todays_menu_detail'),
    path('menu_update/<int:pk>', views.MenuUpdateView.as_view(), name='menu_update'),
    #path('todays_menu_delete/<int:pk>', views.TodaysMenuDeleteView.as_view(), name='todays_menu_delete'),

]