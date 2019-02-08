from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from ..models import Order
from ..models import ProductOrder
# from django.contrib.auth.models import User

@login_required
def cart_items_list(request):
    # order =
    print("user id:", request.__dict__['user'])
    print("user id:", request.user.id)
    # user = User.username
    cartItems = ProductOrder.objects.raw('''SELECT epo.* FROM ecomm_productorder epo''')

    context = { 'cart_items': cartItems }
    # template_name = 'shoppingCart.html'
    # print("context: ", context)

    return render(request, 'shoppingCart.html' , context)

