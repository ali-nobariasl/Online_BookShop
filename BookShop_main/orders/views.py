from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpRequest, HttpResponse
import simplejson as json

from .models import Order, Payment
from .forms import OrderForm
from .utils import generate_order_numebr
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amounts
from accounts.utils import send_notification


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
    # if the request is AJAX request or not
    # store the payment details in the payment model
    # update the order model
    # move the cart items to order food
    # send order confirmation email to customer
    # send order received email to the vendor 
    #clear the cart if the payment is success
    # return back tp ajax with the satatus success oe failere
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')
        
        order = Order.objects.get(user=request.user, order_number=order_number)
        payment = Payment(
            user=request.user,
            transaction_id=transaction_id,
            payment_method=payment_method,
            status=status,
            amount = order.total,
        )
        payment.save()
        #
        order.payment = payment
        order.is_ordered = True
        order.save()
        #
        
        # email to customer
        mail_subject = 'thanks for your order from our website'
        mail_template = 'orders/order_confirmation_email.html'
        context = {
            'user': request.user,
            'order': order,
            'to_email':order.email,
        }
        send_notification(mail_subject, mail_template, context)
    return HttpResponse('Payments view')