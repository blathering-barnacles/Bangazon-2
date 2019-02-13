from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from datetime import datetime, timedelta

from ecomm.forms import UserForm, ProductForm

from ..models import Customer, ProductType, Product, ProductOrder, PaymentType, Order, ProductType

from django.db import connection




@login_required
def sell_product(request):
  '''[Creates a form for users to fill out.  Upon filling out the form correctly item will post to the database as a new product.  Only registered and logged in users may sell an item]

  Author: Andy Herring

  Arguments: request

  Returns:
      Rendered create product template for adding products to the market
  '''
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

    return HttpResponseRedirect(reverse('ecomm:productDetail', args=(newProductId,)))



@login_required
def userProducts(request):
    """[All of a users items that are up for sale can be viewed in the userProduct template.  View does not show items that have been removed or sold.  Only the logged in user will see their information]

    Author: Andy Herring

    Arguments: request

    Returns:
        Rendered create userProduct template for viewing items for sale
    """
    currentUser = request.user.id
    customer = Customer.objects.raw('''SELECT * FROM ecomm_customer where user_id=%s''',[currentUser])[0]
    selling = Product.objects.raw('''
      SELECT * from ecomm_product
      JOIN ecomm_customer
		  ON ecomm_product.seller_id = ecomm_customer.id
		  JOIN auth_user
      ON  auth_user.id = ecomm_customer.user_id
      WHERE auth_user.id = %s
      AND ecomm_product.deletedOn IS Null
    ''', [currentUser])

    categories = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat''')

    context = {'selling': selling, 'categories': categories}
    return render(request, "ecomm/userProducts.html", context)

@login_required
def removeProduct(request, product_id):
    '''[Adds a date to the Deleted On coloumn of a product so it will not appear in the list of products.  Function can only be used if the user is registered and logged in]

    Author: Andy Herring

    Arguments: request

    Returns:
        Items for sale template with the item deleted removed from the list
    '''
    todaysDate = datetime.now()
    formattedDate = str(todaysDate)[0:10]
    product = Product.objects.raw('''
      SELECT * FROM ecomm_product
      WHERE ecomm_product.id = %s
      ''',
      [product_id])[0]

    product.deletedOn = formattedDate
    product.save()

    return HttpResponseRedirect(reverse('ecomm:userProducts'))





