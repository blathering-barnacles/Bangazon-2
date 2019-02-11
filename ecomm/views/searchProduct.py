from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from ..models import Product, ProductType


def search(request):
    '''
    Summary:
        This method allows the search for any product in the database.

    Author:
        Alfonso Miranda

    Arguments:
        request: Contains the value, which is a string, of the product the user is looking for.

    Returns:
        renders the request, the template and injects the context into the template.
    '''
    productName = request.POST['product']
    print("typed: ", productName)
    productFormatted = str("%"+productName+"%")
    categories = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat''')
    product_list = Product.objects.raw('''SELECT ep.* FROM ecomm_product ep WHERE ep.title LIKE %s''', [productFormatted])
    print("products: ", product_list)
    context = {'product_list': product_list, 'categories': categories}
    print("context: ", context.values())
    return render(request, 'ecomm/index.html', context)

def choose(request, category_id):
    '''

    Summary:
    This method is in charge of rendering a drop down where you can select multiple categories or all, if you select all it then goes into
    an if statement that will render all of the categories, if you select a single category then it will render only
    a template with single category.

    Also, once inside if they selected "all" then if they click on a category, they will be able to see all of the products
    of that category.

    Author:
    Alfonso Miranda

    Arguments:
    request: Contains the user, the post, and other elements.

    Returns:
    If its a post and "all" was selected then it renders all of the categories, if a single category was selected then
    it renders just a single category.

    '''

    extraDays = timedelta(days=1)
    todaysDate = datetime.now()
    print("TODAY: ", todaysDate)
    formattedDate = str(todaysDate-extraDays)[0:10]
    print("FORMATTED DATE: ", formattedDate)


    if request.method == 'POST':

        # USE THIS IF YOU WANT TO ADD THE DASHES AS THE DEFAULT SELECT
        # IF THEY SELECTED -------
            # if request.POST['categoryOption'] == "-------":
            #     print("OH NOES!")
            #     categories = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat''')
            #     context = {'categories': categories}
            #     return render(request, 'ecomm/index.html', context)

        # IF THEY SELECTED ALL
        if request.POST['categoryOption'] == "all":
            categories = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat''')

            itemList = []
            categoryIdList = []


            for category in categories:
                # this for loop is going inside the list of all the categories, and is taking the id of a single one and executing
                # an sql query to find the join table where the productType id from product is same as the id of the product Type itself
                # and where the product type id itself matches with the ones from the category list.
                categoryId = category.id
                countedIds = Product.objects.raw('''SELECT count(p.id) as id, ept.* FROM ecomm_product p
                    JOIN ecomm_producttype ept WHERE p.productType_id = ept.id
                    AND ept.id = %s
                    ORDER by ept.name''', [categoryId])
                categoryIdList.append(countedIds)

                allItems = Product.objects.raw('''SELECT p.*, ept.* FROM ecomm_product p
                JOIN ecomm_producttype ept WHERE p.productType_id = ept.id
                AND p.dateAdded >= %s
                AND ept.id = %s
                LIMIT 3''', [formattedDate, categoryId])
                itemList.append(allItems)

            context = {'categories': categories, 'items': itemList, 'countedIds': categoryIdList}
            return render(request, 'ecomm/allCategories.html', context)


        # IF THEY SELECTED A CATEGORY
        else:
            print("woop")
            categoryId = request.POST['categoryOption']
            products = Product.objects.raw('''SELECT ep.* FROM ecomm_product ep WHERE ep.productType_id = %s''', [categoryId])
            countedIds = Product.objects.raw('''SELECT count(ep.id) as id FROM ecomm_product ep WHERE ep.productType_id = %s''', [categoryId])
            singleCategory = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat WHERE cat.id = %s''', [categoryId])
            categories = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat''')
            context = {'products': products, 'currentCategory': singleCategory, 'categories': categories, 'countedIds': countedIds }
            return render(request, 'ecomm/singleCategory.html', context)

    # WHEN THEY CLICK ON A CATEGORY NAME A TAG
    else:

        categories = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat''')
        categoryId = category_id
        products = Product.objects.raw('''SELECT ep.* FROM ecomm_product ep WHERE ep.productType_id = %s''', [categoryId])
        countedIds = Product.objects.raw('''SELECT count(ep.id) as id FROM ecomm_product ep WHERE ep.productType_id = %s''', [categoryId])
        singleCategory = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat WHERE cat.id = %s''', [categoryId])
        context = {'products': products, 'currentCategory': singleCategory, 'categories': categories, 'countedIds': countedIds }
        return render(request, 'ecomm/singleCategory.html', context)
