# from django import views
from django.urls import path

from .views import CategoryDetailView, HomeView, UserProfileView,CategoryListView,RegisterUser,get_cities

handler404 = 'sizzle.views.page_not_found_view'

urlpatterns = [
    path('', HomeView.as_view(), name='main'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('get-cities/', get_cities, name='get_cities'),
    path('register/',RegisterUser.as_view(),name = 'register_user'),
    path('categories/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('<str:slug>/', UserProfileView.as_view(), name='user_profile'),
]
# handler404 = "sizzle.views.page_not_found_view"