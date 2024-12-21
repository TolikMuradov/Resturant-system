from menu.models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        return {'cart_count': Cart.objects.filter(user=request.user).count()}
    return {'cart_count': 0}