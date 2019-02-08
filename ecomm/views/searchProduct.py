from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from ..models import Product

# def search(request):
    # print(request.POST['product'])
    # return print("scoop")
    # return render(request, 'ecomm/index.html')
    # template_name = 'index.html'
    # return HttpResponseRedirect(reverse('ecomm:index'), )
    # return render(request, template_name, {})
    # template_name = 'index.html'
    # return render(request, template_name, {})
    # return HttpResponseRedirect(reverse('ecomm:index'))

def woop(request):
    # print("woop")
    # print("REQUEST: ", request)
    # print("r", request.POST['product'])

    productName = request.POST['product']

    product_list = Product.objects.raw('''SELECT ep.* FROM ecomm_product ep WHERE ep.title = %s''', [productName])
    # woop = product_list.title()


    print("products: ", product_list)
    context = {'product_list': product_list}
    template_name = 'index.html'
    print("context: ", context.values())
    # print("SEARCH: ", productSearch)
    # template_name = 'index.html'
    # return render(request, template_name, {})
    return render(request, template_name, context)

    # return HttpResponseRedirect(reverse('ecomm:index'))
