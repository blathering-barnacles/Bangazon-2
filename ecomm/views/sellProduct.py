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
      # stores the sell form into a variable
      product_form = ProductForm()
      template_name = 'ecomm/createProduct.html'
      return render(request, template_name, {'product_form': product_form})

  if request.method == 'POST':
      # stores user form entries into variables
      seller_id = request.user.id
      location = request.POST["location"]
      title = request.POST["title"] 
      productType_id = request.POST["productType"]
      description = request.POST["description"] 
      price = request.POST["price"] 
      quantity = request.POST["quantity"]
      dateAdded = datetime.now()
      formattedDate = str(dateAdded)[0:10]
        

        # used to inject the raw SQL
      with connection.cursor() as cursor:
        # raw SQL - Variable names reference the database table columns
        cursor.execute("INSERT into ecomm_product VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [None, title, location, description, price, quantity, formattedDate, None, productType_id, seller_id])

        newProductId = cursor.lastrowid
        print("HEEEEEEEEY", newProductId)
        # after clicking the submit button, user is redirected to the products view
        # product = Product.objects.raw('SELECT * FROM ecomm_product WHERE id = %s', [product_id])
        # template_name = 'productDetail.html'
        return HttpResponseRedirect(reverse('ecomm:productDetail', args=(newProductId,)))


