from django.urls import path
from . import views

app_name = 'app_admin'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('category_list/', views.CategoryListView.as_view(), name= 'category_list'),
    path('category_create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category_update/<int:pk>', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category_delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),


    path('heading_create/', views.HeadingCreateView.as_view(), name='heading_create'),
    path('heading_detail/<int:pk>', views.HeadingDetailView.as_view(), name='heading_detail'),
    path('heading_list/', views.HeadingListView.as_view(), name='heading_list'),
    path('heading_update/<int:pk>', views.HeadingUpdateView.as_view(), name='heading_update'),
    path('heading_delete/<int:pk>', views.HeadingDeleteView.as_view(), name='heading_delete'),


    path('menu_add/', views.MenuCreateView.as_view(), name='menu_add'),
    path('menu_list/', views.MenuListView.as_view(), name='menu_list'),
    path('menu_detail/<int:pk>/', views.MenuDetailView.as_view(), name='menu_detail'),
    path('menu_update/<int:pk>', views.MenuUpdateView.as_view(), name='menu_update'),
    path('menu_delete/<int:pk>', views.MenuDeleteView.as_view(), name='menu_delete'),

    path('archive/', views.ArchivePage.as_view(), name='archive_page'),
    path('archive_search/', views.SearchResultPage.as_view(), name='archive_search'),
    path('archive_menu/', views.OldMenuPage.as_view(), name='archive_menu'),

]