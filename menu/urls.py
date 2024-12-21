from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),  # Menü kategorileri listesi
    path('<int:category_id>/', views.menu_detail, name='menu_detail'),  # Belirli kategori detayları
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/complete/', views.checkout_complete, name='checkout_complete'),
    path('order-history/', views.order_history, name='order_history'),
]
