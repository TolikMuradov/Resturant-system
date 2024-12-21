from django.urls import path
from . import views

urlpatterns = [
    path('make/', views.make_reservation, name='make_reservation'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
]
