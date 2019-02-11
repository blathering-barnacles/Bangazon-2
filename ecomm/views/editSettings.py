from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ..models import Customer, ProductType, Product, ProductOrder, PaymentType, Order
# from ..forms import UserSettings

@login_required
def editSettingsForm(request):
    """R Lancaster[Information from DB gets passed to the edit Settings Form]

    Arguments:
        request

    Returns:
        render sends info from the Customer table to the edit Settings form page.
    """

    currentUserId = request.user.id
    customer = Customer.objects.raw('''SELECT * FROM ecomm_customer where user_id=%s''',[currentUserId])[0]
    context = {'customer' : customer}
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

