from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservation_form, name='reservation_form'),
    path('success/', views.reservation_success, name='reservation_success'),
]
