from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ..models import Customer, ProductType, Product, ProductOrder, PaymentType, Order
from django.utils import timezone
from datetime import datetime, timedelta
from ecomm.forms import AddPayment
from django.db import connection
# from ..forms import UserSettings

@login_required
def editSettingsForm(request):
    """R Lancaster[Information from DB gets passed to the edit Settings Form]

    Arguments:
        request

    Returns:
        render sends info from the Customer table to the edit Settings form page.
    """
    categories = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat''')
    currentUserId = request.user.id
    customer = Customer.objects.raw('''SELECT * FROM ecomm_customer where user_id=%s''',[currentUserId])[0]
    context = {'customer' : customer, 'categories' : categories}
    return render(request, 'ecomm/editSettings.html', context)
    # userSettings = UserSettings()
    # return render(request, 'ecomm/editSettings.html', {"form": userSettings.as_p()})

@login_required
def editSettings(request):
    """R Lancaster[This method is executed when the user saves the updated user settings on the user settings update form page]

    Arguments:
        request

    Returns:
        User is redirected to main User Settings page.
    """

    currentUserId = request.user.id
    custSettings = Customer.objects.raw('''SELECT * FROM ecomm_customer where user_id=%s''',[currentUserId])[0]
    uSettings = User.objects.raw('''SELECT * FROM auth_user where id=%s''',[currentUserId])[0]
    uSettings.last_name = request.POST['lastName']
    custSettings.phone = request.POST['phone']
    custSettings.address = request.POST['address']
    custSettings.save()
    uSettings.save()
    return HttpResponseRedirect(reverse('ecomm:userSettings'))

def editPaymentsForm(request):
    """R Lancaster[method populates Edit Payment Methods form with existing payment options]

    Arguments:
        request

    Returns:
        render, context of existing payment options
    """

    currentUserId = request.user.id
    categories = ProductType.objects.raw('''SELECT cat.id, cat.name FROM ecomm_producttype cat''')
    payments = PaymentType.objects.raw('''
        SELECT * from ecomm_paymentType
        JOIN ecomm_customer
        ON ecomm_customer.user_id  = ecomm_paymentType.customer_id
        JOIN auth_user
        ON  auth_user.id = ecomm_customer.user_id
        WHERE auth_user.id =%s
        AND ecomm_paymentType.deletedOn = ''
    ''', [currentUserId])
    context = {'payments' : payments, 'categories': categories}
    return render(request, 'ecomm/editPayments.html', context)

def deletePayment(request, payment_id):
    """R Lancaster[method adds a deletedOn date to the PaymentType table, therefore "soft deleting" the payment option]

    Arguments:
        request
        payment_id

    Returns:
        redirects back to the Edit Payments form
    """

    todaysDate = datetime.now()
    formattedDate = str(todaysDate)[0:10]
    payment = PaymentType.objects.raw('''
        SELECT * FROM ecomm_paymentType
        WHERE id = %s
        ''', [payment_id])[0]
    payment.deletedOn = formattedDate
    payment.save()
    return HttpResponseRedirect(reverse('ecomm:editPaymentsForm'))

def addPaymentsForm(request):
    """R Lancaster[directs the user to the Add Payment template]

    Arguments:
        request

    Returns:
        render
    """

    form = AddPayment()
    return render(request, 'ecomm/addPayment.html', {"form" : form})

def addPayment(request):
    """R Lancaster[method takes values entered on Add Payment form and inserts a row into the PaymentType table]

    Arguments:
        request

    Returns:
        redirects user to the Edit Payments Form page
    """

    currentUserId = request.user.id
    name = request.POST['name']
    cardNum = request.POST['cardNum']
    # Creates a new payment type row
    payment_sql = ''' INSERT INTO ecomm_paymenttype VALUES (%s, %s, %s, %s, %s)'''
    with connection.cursor() as cursor:
        cursor.execute(payment_sql, [None, name, cardNum, '', currentUserId])
    return HttpResponseRedirect(reverse('ecomm:editPaymentsForm'))