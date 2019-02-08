from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext

from ecomm.models import Product

def productDetail(request, product_id):

    try:
        product_sql = 'SELECT * FROM ecomm_product WHERE ecomm_product.id=%s;'

        product = Product.objects.raw(product_sql, [product_id])[0]

        context = {"product": product}
        return render(request, 'ecomm/productDetail.html', context)

    except IndexError:
        raise Http404("That product doesn't exist")
