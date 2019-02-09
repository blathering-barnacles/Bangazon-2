from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from ..models import Product, ProductType


def search(request):

    productName = request.POST['product']
    print("typed: ", productName)
    productFormatted = str("%"+productName+"%")
    categories = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat''')
    product_list = Product.objects.raw('''SELECT ep.* FROM ecomm_product ep WHERE ep.title LIKE %s''', [productFormatted])
    print("products: ", product_list)
    context = {'product_list': product_list, 'categories': categories}
    # template_name = 'index.html'
    print("context: ", context.values())
    return render(request, 'ecomm/index.html', context)

def choose(request, category_id):
    print("woop")
    categoryId = request.POST['categoryOption']
    products = Product.objects.raw('''SELECT ep.* FROM ecomm_product ep WHERE ep.productType_id = %s''', [categoryId])
    countedIds = Product.objects.raw('''SELECT count(ep.id) as id FROM ecomm_product ep WHERE ep.productType_id = %s''', [categoryId])
    singleCategory = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat WHERE cat.id = %s''', [categoryId])
    # template_name = 'index.html'
    categories = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat''')
    context = {'products': products, 'currentCategory': singleCategory, 'categories': categories, 'countedIds': countedIds }
    return render(request, 'ecomm/singleCategory.html', context)