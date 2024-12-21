from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_as_read, name='mark_as_read'),
    path('notifications/mark-as-read-and-delete/<int:notification_id>/', views.mark_as_read_and_delete, name='mark_as_read_and_delete'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('delete-account/', views.delete_account, name='delete_account'),
]

