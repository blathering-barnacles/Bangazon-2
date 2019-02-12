from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.db import connection
from ..models import Order, ProductOrder, Customer

@login_required
def add_product_to_order(request, product_id):

    buyer_id = request.user.id

    try:
        open_order = Order.objects.raw(''' SELECT * FROM ecomm_order
        WHERE ecomm_order.buyer_id = %s AND ecomm_order.paymentType_id IS NULL AND ecomm_order.deletedOn IS NULL;''', [buyer_id])[0]

        with connection.cursor() as cursor:
            cursor.execute("INSERT into ecomm_productorder VALUES (%s,%s,%s,%s);", [None, None, open_order.id, product_id])

    except IndexError:
        with connection.cursor() as cursor:
            cursor.execute("INSERT into ecomm_order VALUES (%s,%s,%s,%s);", [None, None, buyer_id, None])
            new_order_id = cursor.lastrowid
            cursor.execute("INSERT into ecomm_productorder VALUES (%s,%s,%s,%s)", [None, None, new_order_id, product_id])

    return HttpResponseRedirect(reverse('ecomm:index'))




