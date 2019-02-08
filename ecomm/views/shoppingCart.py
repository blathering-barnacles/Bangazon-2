from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from ..models import Order, ProductOrder, Customer
# from django.contrib.auth.models import User

@login_required
def cart_items_list(request):
    # order =
    print("user id:", request.__dict__['user'])
    print("user id:", request.user.id)
    user = request.user.id
    customer = Customer.objects.raw('''SELECT c.id FROM ecomm_customer c WHERE c.id = %s''', [user])
    print("customer: ", (customer))
    order = Order.objects.raw('''SELECT o.id FROM ecomm_order o WHERE o.buyer_id = %s''', [user])

    cartItems = ProductOrder.objects.raw('''SELECT epo.* FROM ecomm_productorder epo WHERE epo.order_id = %s''', (str(order), ))

    context = { 'customers': customer, 'orders': order }
    # context = { 'cart_items': cartItems }
    # template_name = 'shoppingCart.html'
    print("context: ", context)

    return render(request, 'shoppingCart.html' , context)

