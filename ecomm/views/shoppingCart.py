from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.db import connection
from ..models import Order, ProductOrder, Customer, ProductType

@login_required
def cart_items_list(request, user_id):
    '''
    Summary:
        This method lists the items in the product order table that have the user's id.

    Author:
        Alfonso Miranda

    Arguments:
        request: Contains the user and other elements.

    Returns:
        renders the request, the template and injects the context into the template.
    '''


    user = request.user.id
    categories = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat''')
    customer = Customer.objects.raw('''SELECT c.id FROM ecomm_customer c WHERE c.id = %s''', [user])[0]
    orders = Order.objects.raw('''SELECT o.id FROM ecomm_order o WHERE o.buyer_id = %s''', [user_id])
    orderId = user_id
    # cartItems = ProductOrder.objects.raw('''SELECT epo.* FROM ecomm_productorder as epo WHERE epo.order_id = %s''', (orderId, ))
    cartItemList = []
    for order in orders:
        orderId = order.id
        cartItems = ProductOrder.objects.raw('''SELECT epo.* FROM ecomm_productorder as epo WHERE epo.order_id = %s''', (orderId, ))
        print("ITEMS IN CART: ", cartItems)
        cartItemList.append(cartItems)

    print("ITEMS: ", cartItemList)
    # with connection.cursor() as cursor:
    #     cart_list = cursor.execute("SELECT epo.* FROM ecomm_productorder as epo WHERE epo.order_id = %s", (orderId, ))
    #     woop = cursor.fetchall()
        # cart_list.fetchall()
        # print("CART_LIST: ", cart_list)

    context = { 'customers': customer, 'cart_list': cartItemList, 'categories': categories, 'orders': orders }
    print("context: ", context)

    return render(request, 'ecomm/shoppingCart.html' , context)

def deleteOrderItem(request, item_id):
    '''
    Summary:
        This method updates the ProductOrder row that matches the item id.

    Author:
        Alfonso Miranda

    Arguments:
        request: Contains the user, the post, and other elements.

    Returns:
        After updating the deletedOn column in specific row it redirects to the shopping cart of that specific user.
    '''

    todaysDate = datetime.now()
    formattedDate = str(todaysDate)[0:10]
    print("DATE: ", formattedDate)
    userId = request.user.id
    item = ProductOrder.objects.raw('''SELECT ecomm_productorder.* FROM ecomm_productorder WHERE ecomm_productorder.id = %s''', [item_id])[0]
    print("ITEM: ", item)
    item.deletedOn = formattedDate
    item.save()

    return HttpResponseRedirect(reverse('ecomm:list_cart_items', args=(userId,)))

def deleteOrder(request, order_id):
    '''
    Summary:
        This method updates the Order row that matches the order_id, and ProductOrder rows that match the order_id.
        after that it proceeds to add todays date on their respective deletedOn columns.

    Author:
        Alfonso Miranda

    Arguments:
        request: Contains the user, and other elements.

    Returns:
        After updating the deletedOn column in specific row it redirects to the shopping cart of that specific user.
    '''
    todaysDate = datetime.now()
    formattedDate = str(todaysDate)[0:10]
    orderId = order_id
    order = Order.objects.raw('''SELECT o.id FROM ecomm_order o WHERE o.buyer_id = %s''', [orderId])[0]
    items = ProductOrder.objects.raw('''SELECT po.* FROM ecomm_productorder po WHERE po.order_id = %s''', [orderId])

    for item in items:
        item.deletedOn = formattedDate
        item.save()

    order.deletedOn = formattedDate
    order.save()
    print("WOOP")
    print("ORDER ID: ", order_id)

    return HttpResponseRedirect(reverse('ecomm:list_cart_items', args=(order_id,)))