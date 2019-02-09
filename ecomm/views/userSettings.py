from django.shortcuts import render
from django.urls import reverse
from ..models import Product, ProductType

def userSettings(request):
    print("hi")
    woop = "woop"
    categories = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat''')
    context ={ 'woop': woop, 'categories': categories }
    return render(request, 'ecomm/index.html', context)