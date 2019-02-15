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




def viewOrder(request, user_id):

    userId = user_id
    # print("USER ID: ", userId)

    categories = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat''')
    orders = Order.objects.raw('''SELECT o.* FROM ecomm_order o WHERE o.buyer_id = %s''', [userId])
    orderItemList = []
    countedItems = ""


    for order in orders:
        # print("ORDER: ", order)
        orderId = order.id
        orderItems = ProductOrder.objects.raw('''SELECT po.*
        FROM ecomm_productorder po, ecomm_order eo
        WHERE eo.id = po.order_id
        AND eo.id = %s''', [order.id])
        print("ORDER ITEMS: ", orderItems)
        orderItemList.append(orderItems)

        countedItems = ProductOrder.objects.raw('''SELECT count(po.id) as id
            FROM ecomm_productorder po, ecomm_order eo
            WHERE eo.id = po.order_id
            AND eo.id = %s
            AND po.deletedOn is null''', [orderId])

    # print("COUNTED ITEMS: ", countedItems)

    # print("ORDER ITEM LIST: ", orderItemList)

    context = { 'orders': orders, 'orderItemList': orderItemList, 'countedItems': countedItems, 'categories': categories }

    return render(request, 'ecomm/orderHistory.html' , context)

def viewOrderDetail(request, order_id):

    orderId = order_id
    orderItems = ProductOrder.objects.raw('''SELECT po.*
        FROM ecomm_productorder po, ecomm_order eo
        WHERE eo.id = po.order_id
        AND eo.id = %s''', [orderId])

    categories = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat''')
    countedItems = ProductOrder.objects.raw('''SELECT count(po.id)
        FROM ecomm_productorder po, ecomm_order eo
        WHERE eo.id = po.order_id
        AND eo.id = %s
        AND po.deletedOn is null''',[orderId])

    # print("COUNTED ITEMS: ", countedItems)

    context = { 'orderItems': orderItems, 'countedItems': countedItems, 'categories': categories, "orderId": orderId }

    return render(request, 'ecomm/orderDetail.html' , context)

