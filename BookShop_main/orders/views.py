from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
import simplejson as json
from django.contrib.auth.decorators import login_required

from .models import Order, Payment, OrderedBook
from .forms import OrderForm
from .utils import generate_order_numebr
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amounts
from accounts.utils import send_notification

@login_required(login_url='login')
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



@login_required(login_url='login')
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
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_book = OrderedBook()
            ordered_book.order = order
            ordered_book.payment = payment
            ordered_book.user = request.user
            ordered_book.Bookitem = item.bookitem
            ordered_book.quantity = item.quantity
            ordered_book.price = item.bookitem.price
            ordered_book.amount = item.bookitem.price * item.quantity
            ordered_book.save()
            
        # email to customer
        mail_subject = 'thanks for your order from our website'
        mail_template = 'orders/order_confirmation_email.html'
        context = {
            'user': request.user,
            'order': order,
            'to_email':order.email,
        }
        send_notification(mail_subject, mail_template, context)
        
        #
        mail_subject = 'You have new order'
        mail_template = 'orders/new_order_received.html'
        to_emails =[]
        for i in cart_items:
            if i.bookitem.vendor.user.email not in to_emails:
                to_emails.append(i.bookitem.vendor.user.email)
        context = {
            'user': request.user,
            'order': order,
            'to_email':to_emails,
        }
        send_notification(mail_subject, mail_template, context)
        
        # clear the cart
        #cart_items.delete()
        
        # return back to ajax
        response = {
            'order_number': order_number,
            'transaction_id': transaction_id,
        }
        return JsonResponse(response)
    return HttpResponse('Payments view')



def order_complete(request):
    order_number= request.GET.get('order_no')
    transaction_id= request.GET.get('trans_id')


    order = Order.objects.get(order_number=order_number ,payment__transaction_id=transaction_id, is_ordered=True)
    ordered_book = OrderedBook.objects.filter(order=order)
    subtotal = 0
        
    for item in ordered_book:
        subtotal += (item.price * item.quantity)
            
    tax_data = json.loads(order.tax_data)
    context ={
            'order':order,
            'ordered_book':ordered_book,
            'subtotal':subtotal,
            'tax_data':tax_data,
        }
    return render(request, 'orders/order_complete.html', context=context)


def ali(request):
    
    if request.method == 'POST':
        pass
    else:
        return False
    context = {}
    return HttpResponse("I am ali")
        
