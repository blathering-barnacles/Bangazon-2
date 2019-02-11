from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ..models import Customer, ProductType, Product, ProductOrder, PaymentType, Order

@login_required
def editSettingsForm(request):
    currentUserId = request.user.id
    customer = Customer.objects.raw('''SELECT * FROM ecomm_customer where user_id=%s''',[currentUserId])[0]
    print(customer.phone)
    context = {'customer' : customer}
    return render(request, 'ecomm/editSettings.html', context)

@login_required
def editSettings(request):
    currentUserId = request.user.id
    custSettings = Customer.objects.raw('''SELECT * FROM ecomm_customer where user_id=%s''',[currentUserId])[0]
    uSettings = User.objects.raw('''SELECT * FROM auth_user where id=%s''',[currentUserId])[0]
    uSettings.last_name = request.POST['lastName']
    custSettings.phone = request.POST['phone']
    custSettings.address = request.POST['address']
    custSettings.save()
    uSettings.save()
    return HttpResponseRedirect(reverse('ecomm:userSettings'))

