from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import connection
from ..models import Order, ProductOrder, Customer
# from django.contrib.auth.models import User

@login_required
def cart_items_list(request, order_id):
    # order =
    print("user id:", request.__dict__['user'])
    print("user id:", request.user.id)
    user = request.user.id
    customer = Customer.objects.raw('''SELECT c.id FROM ecomm_customer c WHERE c.id = %s''', [user])[0]
    print("customer: ", customer)
    order = Order.objects.raw('''SELECT o.id FROM ecomm_order o WHERE o.buyer_id = %s''', [order_id])[0]
    orderId = order_id
    print("ORDER: ", orderId)
    print("ORDER ID: ", order_id)

    # cartItems = ProductOrder.objects.raw('''SELECT epo.* FROM ecomm_productorder as epo WHERE epo.order_id = %s''', (order, ))
    # print("CART ITEMS: ", cartItems)

    # conn = sqlite3.connect('db.sqlite3')
    # cur = conn.cursor()
    # cur.execute("SELECT * FROM users WHERE EmployeeNumber=?", ('12345', ))
    # users = cur.fetchall()

    # with connection.cursor() as cursor:
        # cart_list = cursor.execute("SELECT epo.* FROM ecomm_productorder as epo WHERE epo.order_id = %s", (order, ))[0]
        # cursor.fetchall()
        # cart_list.fetchall()
        # print("CART_LIST: ", cart_list)

    context = { 'customers': customer}
    # context = { 'cart_items': cartItems }
    # template_name = 'shoppingCart.html'
    print("context: ", context)

    return render(request, 'shoppingCart.html' , context)

