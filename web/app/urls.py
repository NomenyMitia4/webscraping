from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('create/', views.pays_create_view, name="pays_create"),
    path('list/', views.pays_list_view, name="pays_list")
]