from django.urls import path
from . import views
from .views import TodaysMenuCreateView, TodaysMenuListView, TodaysMenuDetailView, MenuAddView

app_name = 'app_admin'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('food_list/', views.FoodListView.as_view(), name= 'food_list'),
    path('category_create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('food_update/<int:pk>', views.FoodUpdateView.as_view(), name='food_update'),
    path('food_delete/<int:pk>', views.FoodDeleteView.as_view(), name='food_delete'),


    path('menu_header/', views.MenuCategories.as_view(), name='menu_header'),

    path('foods_name_listing/', views.FoodsList.as_view(), name='foods_name_listing'),
    path('food_create/', views.Foods.as_view(), name='food_create'),
    path('foods_name_listing_update/<int:pk>', views.FoodsUpdate.as_view(), name='foods_name_listing_update'),
    path('foods_name_listing_delete/<int:pk>', views.FoodsDelete.as_view(), name='foods_name_listing_delete'),


    path('todays_menu_create/', views.TodaysMenuCreateView.as_view(), name='todays_menu_create'),
    path('todays_menu_list/', views.TodaysMenuListView.as_view(), name='todays_menu_list'),
    path('todays_menu_detail/<int:pk>/', views.TodaysMenuDetailView.as_view(), name='todays_menu_detail'),
    path('todays_menu_update/<int:pk>', views.TodaysMenuUpdateView.as_view(), name='todays_menu_update'),
    path('todays_menu_delete/<int:pk>', views.TodaysMenuDeleteView.as_view(), name='todays_menu_delete'),

    path('menu_add/', views.MenuAddView.as_view(), name='menu_add')
]