from django.shortcuts import render, get_object_or_404, redirect
from .models import MenuCategory, MenuItem, Cart, Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder

# Kategoriler listesi
def menu_list(request):
    categories = MenuCategory.objects.all()
    return render(request, 'menu/menu_list.html', {'categories': categories})

# Menü detayları (Belirli kategoriye ait ögeler)
def menu_detail(request, category_id):
    category = get_object_or_404(MenuCategory, id=category_id)
    items = MenuItem.objects.filter(category=category)
    return render(request, 'menu/menu_detail.html', {'category': category, 'items': items})

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'menu/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{item.name} sepete eklendi.")
    return redirect('menu_detail', category_id=item.category.id)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, user=request.user, item_id=item_id)
    cart_item.delete()
    return redirect('cart_view') 

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)

    if request.method == 'POST':
        # JSON serializable bir yapıya dönüştür
        order_items = [
            {"name": item.item.name, 
             "quantity": item.quantity, 
             "price": float(item.item.price)}  # Decimal'i float'a dönüştür
            for item in cart_items
        ]

        # Order kaydı oluştur
        Order.objects.create(
            user=request.user,
            items=json.dumps(order_items),  # JSON string olarak kaydet
            total_price=total_price  # Decimal alan, veritabanında saklanabilir
        )

        cart_items.delete()  # Sepeti temizle
        messages.success(request, "Sipariş başarıyla tamamlandı.")
        return redirect('checkout_complete')

    return render(request, 'menu/checkout.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def checkout_complete(request):
    return render(request, 'menu/checkout_complete.html')


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    for order in orders:
        order.parsed_items = json.loads(order.items)  # JSON'dan Python listesine çevirin
    return render(request, 'menu/order_history.html', {'orders': orders})
