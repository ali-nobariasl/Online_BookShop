from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpRequest, HttpResponse
import simplejson as json

from .models import Order
from .forms import OrderForm
from .utils import generate_order_numebr
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amounts



def place_order(request):
    
    
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    
    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['tax_dic']
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            
            order.save() # pk is created after saveing , so we should use it after save
            order.order_number = generate_order_numebr(order.id)
            order.save()
            context = {
                'order': order,
                'cart_items':cart_items,
            }
            return render(request, 'orders/place_order.html', context=context)
        else:
            print(form.errors)   
    return render(request, 'orders/place_order.html')


def payments(request):
    
    return HttpResponse('Payments view')