from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
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

    extraDays = timedelta(days=1)
    todaysDate = datetime.now()
    print("TODAY: ", todaysDate)
    formattedDate = str(todaysDate-extraDays)[0:10]
    print("FORMATTED DATE: ", formattedDate)

    if request.POST['categoryOption'] == "-------":
        categories = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat''')
        context = {'categories': categories}
        return render(request, 'ecomm/index.html', context)

    elif request.POST['categoryOption'] == "all":
        categories = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat''')

        allItems = Product.objects.raw('''SELECT p.*, ept.* FROM ecomm_product p
            JOIN ecomm_producttype ept WHERE p.productType_id = ept.id
            AND p.dateAdded >= %s
            ORDER by ept.name''', [formattedDate])

        # itemsList = allItems[0:3]

        categoryIdList = []


        for category in categories:
            # this for loop is going inside the list of all the categories, and is taking the id of a single one and executing
            # an sql query to find the join table where the productType id from product is same as the id of the product Type itself
            # and where the product type id itself matches with the ones from the category list.
            categoryId = category.id
            # print("CATEGORY IDS: ", categoryId)
            countedIds = Product.objects.raw('''SELECT count(p.id) as id, ept.* FROM ecomm_product p
                JOIN ecomm_producttype ept WHERE p.productType_id = ept.id
                AND ept.id = %s
                ORDER by ept.name''', [categoryId])
            categoryIdList.append(countedIds)

        context = {'categories': categories, 'items': allItems, 'countedIds': categoryIdList}
        return render(request, 'ecomm/allCategories.html', context)

    else:
        # print("woop")
        categoryId = request.POST['categoryOption']
        products = Product.objects.raw('''SELECT ep.* FROM ecomm_product ep WHERE ep.productType_id = %s''', [categoryId])
        countedIds = Product.objects.raw('''SELECT count(ep.id) as id FROM ecomm_product ep WHERE ep.productType_id = %s''', [categoryId])
        singleCategory = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat WHERE cat.id = %s''', [categoryId])
        # template_name = 'index.html'
        categories = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat''')
        context = {'products': products, 'currentCategory': singleCategory, 'categories': categories, 'countedIds': countedIds }
        return render(request, 'ecomm/singleCategory.html', context)