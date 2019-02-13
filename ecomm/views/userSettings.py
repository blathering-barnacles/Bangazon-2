from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from ..models import Customer, ProductType, Product, ProductOrder, PaymentType, Order, ProductType

@login_required
def userSettings(request):
    """R Lancaster[Method requests information from many tables in the DB and sends the context over to the User Settings template.  All information is related to the user ID of the logged in user.]

    Arguments:
        request

    Returns:
        render sends context from various tables to the user Settings template view.
    """

    # sql = '''
    #     SELECT * FROM ecomm_user WHERE id=%s
    #     '''
    # user = User.objects.raw(sql, [pk])[0]
    currentUserId = request.user.id
    categories = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat''')
    customer = Customer.objects.raw('''SELECT * FROM ecomm_customer where user_id=%s''',[currentUserId])[0]
    payments = PaymentType.objects.raw('''
        SELECT * from ecomm_paymentType
        JOIN ecomm_customer
        ON ecomm_customer.user_id  = ecomm_paymentType.customer_id
        JOIN auth_user
        ON  auth_user.id = ecomm_customer.user_id
        WHERE auth_user.id =%s
        AND ecomm_paymentType.deletedOn = ''
    ''', [currentUserId])
    history = ProductOrder.objects.raw('''
        SELECT * from ecomm_productorder
        JOIN ecomm_order
        ON ecomm_productorder.order_id  = ecomm_order.id
        JOIN ecomm_customer
        ON ecomm_customer.id = ecomm_order.buyer_id
        JOIN auth_user
        ON  auth_user.id = ecomm_customer.user_id
        JOIN ecomm_product
        ON ecomm_product.id = ecomm_productorder.product_id
        WHERE auth_user.id =%s
        AND ecomm_productOrder.deletedOn is null
    ''', [currentUserId])

    orders = Order.objects.raw(''' SELECT o.* from ecomm_order o WHERE o.buyer_id = %s AND o.paymentType_id is not null AND o.deletedOn is null ''',[currentUserId])

    ordersList = []
    for order in orders:
        ordersList.append(order)

    print("LIST: ", ordersList)
    if len(ordersList) == 0:
        print("woop")
    else:
        print("scoop")
        ordersList == orders[0]
        print(orders[0])

    print("ORDER LIST: ", ordersList)

    # print("ORDER IDDD: ", order[0].id)
    context = {'customer' : customer, 'payments' : payments, 'history' : history, 'categories': categories, 'orders': ordersList}
    return render(request, 'ecomm/userSettings.html', context)
    # order = ProductOrder.objects.raw('SELECT * from ecomm_order')
