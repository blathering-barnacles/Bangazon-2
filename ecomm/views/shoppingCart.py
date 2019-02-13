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

    cartItemList = []
    for order in orders:
        orderId = order.id
        cartItems = ProductOrder.objects.raw('''SELECT epo.* FROM ecomm_productorder as epo WHERE epo.order_id = %s''', (orderId, ))
        cartItemList.append(cartItems)

    # print("ITEMS: ", cartItemList)
    # with connection.cursor() as cursor:
    #     cart_list = cursor.execute("SELECT epo.* FROM ecomm_productorder as epo WHERE epo.order_id = %s", (orderId, ))
    #     woop = cursor.fetchall()
        # cart_list.fetchall()
        # print("CART_LIST: ", cart_list)

    context = { 'customers': customer, 'cart_list': cartItemList, 'categories': categories, 'orders': orders }

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
    userId = request.user.id
    order = Order.objects.raw('''SELECT o.id FROM ecomm_order o WHERE o.buyer_id = %s''', [userId])
    one_orderId = order[0].__dict__['id']
    product = ProductOrder.objects.raw('''SELECT ecomm_productorder.* FROM ecomm_productorder WHERE ecomm_productorder.id = %s''', [item_id])[0]
    items = ProductOrder.objects.raw(''' SELECT ecomm_productorder.* FROM ecomm_productorder JOIN ecomm_order ON ecomm_productorder.order_id = ecomm_order.id
    AND ecomm_productorder.order_id = %s
    AND ecomm_productorder.deletedOn is null''', [one_orderId])

    itemList = []
    print("Items: ", items)
    for item in items:
        print("item: ", item)
        itemList.append(item)

    print("LIST: ", itemList)
    if len(itemList) <= 1:
        print("ITS less or equal to 2")
        order[0].deletedOn = formattedDate
        item.deletedOn = formattedDate
        item.save()
        order[0].save()
    else:
        print("ITs MORE than 1")
        product.deletedOn = formattedDate
        product.save()

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

    print("ID: ", order_id)
    todaysDate = datetime.now()
    formattedDate = str(todaysDate)[0:10]
    orderId = int(order_id)
    items = ProductOrder.objects.raw('''SELECT po.* FROM ecomm_productorder po WHERE po.order_id = %s''', [orderId])

    userId = request.user.id
    orders = Order.objects.raw('''SELECT o.id FROM ecomm_order o WHERE o.buyer_id = %s''', [userId])


    for order in orders:
        if  order.id == orderId:
            print("ORDER where ID matches: ", order)

            print("ORDER: ", order)
            order.deletedOn = formattedDate
            order.save()


    for item in items:
        item.deletedOn = formattedDate
        item.save()

    return HttpResponseRedirect(reverse('ecomm:list_cart_items', args=(1,)))