from django.urls import path
from django.views.generic import TemplateView
from .views import contact_view

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('contact/', contact_view, name='contact_view'),
    
]
