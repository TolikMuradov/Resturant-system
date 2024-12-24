from django.urls import path
from . import views

urlpatterns = [
    path('make/', views.make_reservation, name='make_reservation'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/<int:reservation_id>/update-status/', views.update_reservation_status, name='update_reservation_status'),
]
