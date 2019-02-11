from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext
from django.db import connection

from ecomm.models import Product, ProductOrder


def productDetail(request, pk):
    '''[Gets the product details from the database and prints to the product detail template]

    Arguments:
        request
        product_id - from the url

    Raises:
        Http404 -- If the product id does not exist, an index error is raised and displays a 404 page

    Returns:
        Rendered product detail template
    '''


    try:
        product_sql = 'SELECT * FROM ecomm_product WHERE ecomm_product.id=%s;'

        product = Product.objects.raw(product_sql, [pk])[0]

        purchased_sql = ''' SELECT ecomm_product.id, COUNT(*) as total
            FROM ecomm_product
            JOIN ecomm_productorder
            ON ecomm_productorder.product_id= ecomm_product.id
            JOIN ecomm_order
            ON ecomm_productorder.order_id= ecomm_order.id
            WHERE ecomm_productorder.product_id =%s AND ecomm_order.paymentType_id IS NOT NULL;'''

        purchased_quantity = Product.objects.raw(purchased_sql, [pk])[0]

        inventory = product.quantity - purchased_quantity.total
        context = {"product": product, "inventory": inventory}
        return render(request, 'ecomm/productDetail.html', context)

    except IndexError:
        raise Http404("That product doesn't exist")