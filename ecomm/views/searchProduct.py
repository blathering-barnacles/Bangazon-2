from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from ..models import Product


def search(request):

    productName = request.POST['product']
    print("typed: ", productName)
    productFormatted = str("%"+productName+"%")

    product_list = Product.objects.raw('''SELECT ep.* FROM ecomm_product ep WHERE ep.title LIKE %s''', [productFormatted])
    print("products: ", product_list)
    context = {'product_list': product_list}
    template_name = 'index.html'
    print("context: ", context.values())
    return render(request, template_name, context)
