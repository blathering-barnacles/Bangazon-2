from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from ..models import Customer, Order
from datetime import datetime, timedelta

from ecomm.forms import UserForm, ProductForm

from ..models import Customer, Order
from ecomm.models import Product, ProductType

from django.db import connection




@login_required
def sell_product(request):
    if request.method == 'GET':
        product_form = ProductForm()
        template_name = 'ecomm/createProduct.html'
        return render(request, template_name, {'product_form': product_form})

    if request.method == 'POST':
        # form_data = request.POST
        seller_id = request.user.id
        location = request.POST["location"]
        title = request.POST["title"] 
        productType_id = request.POST["productType"]
        description = request.POST["description"] 
        price = request.POST["price"] 
        quantity = request.POST["quantity"]
        dateAdded = datetime.now()
        formattedDate = str(dateAdded)[0:10]
        


        with connection.cursor() as cursor:
          cursor.execute("INSERT into ecomm_product VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [None, title, location, description, price, quantity, formattedDate, None, productType_id, seller_id])
          return HttpResponseRedirect(reverse('ecomm:list_products'))


