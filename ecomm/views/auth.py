from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse

from ecomm.forms import UserForm, ProductForm

from ..models import Customer, Order
from ecomm.models import Product

from django.db import connection

def index(request):
    user = request.user.id
    template_name = 'ecomm/index.html'
    customer = Customer.objects.raw('''SELECT c.id FROM ecomm_customer c WHERE c.id = %s''', [user])[0]
    print("customer: ", (customer))
    order = Order.objects.raw('''SELECT o.id FROM ecomm_order o WHERE o.buyer_id = %s''', [user])[0]
    # return render(request, template_name, {})
    print("ORDER: ", order)
    context = { 'customers': customer, 'orders': order }
    return render(request, template_name , context)

# Create your views here.
def register(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        return login_user(request)

    elif request.method == 'GET':
        user_form = UserForm()
        template_name = 'ecomm/register.html'
        return render(request, template_name, {'user_form': user_form})


def login_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username=request.POST['username']
        password=request.POST['password']
        authenticated_user = authenticate(username=username, password=password)
        print(username, password)
        print("authenticate: ", authenticate(username=username, password=password))

        # If authentication was successful, log the user in
        if authenticated_user is not None:
            login(request=request, user=authenticated_user)
            return HttpResponseRedirect('/')

        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {}, {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")


    return render(request, 'ecomm/login.html', {}, context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage. Is there a way to not hard code
    # in the URL in redirects?????
    return HttpResponseRedirect('/')


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
        


        with connection.cursor() as cursor:
          cursor.execute("INSERT into ecomm_product VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", [None, title, location, description, price, quantity, None, productType_id, seller_id])
          return HttpResponseRedirect(reverse('ecomm:index'))





def list_products(request):
    all_products = Product.objects.all()
    template_name = 'ecomm/listProduct.html'
    return render(request, template_name, {'products': all_products})

