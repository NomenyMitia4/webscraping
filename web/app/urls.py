from django.urls import path
from . import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home_view, name="home"),
    path('create/', views.pays_create_view, name="pays_create"),
    path('list/', views.pays_list_view, name="pays_list"),
    path('detail/<str:pays>/', views.pays_details_view, name="pays_details")
]

urlpatterns += staticfiles_urlpatterns()