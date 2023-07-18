
from .models import Cart
from stok.models import BookItem




def get_cart_counter(request):
    
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count =0
        except:
            cart_count =0

    return dict(cart_count=cart_count)


def get_cart_amounts(request):
    subtotal =0
    tax =0
    grand_total =0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            subtotal += (item.bookitem.price * item.quantity )
        
        grand_total = subtotal + tax
        
    
    print(subtotal)
    print(grand_total)
    return dict(subtotal=subtotal,
                grand_total=grand_total,
                tax=tax)