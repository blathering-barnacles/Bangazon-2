from django.conf.urls import url
from django.urls import path

from . import views

app_name = "ecomm"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login_user, name='login'),
    url(r'^logout$', views.user_logout, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^sell$', views.sell_product, name='sell'),
    url(r'^products$', views.list_products, name='list_products'),
    path('userSettings', views.userSettings, name='userSettings'),
    path('products/<int:product_id>/', views.productDetail, name='productDetail'),
    path('userSettings', views.userSettings, name='userSettings'),
    path('editPaymentsForm', views.editPaymentsForm, name='editPaymentsForm'),
    path('addPaymentsForm', views.addPaymentsForm, name='addPaymentsForm'),
    path('addPayment', views.addPayment, name='addPayment'),
    path('deletePayment/<int:payment_id>/', views.deletePayment, name='deletePayment'),
    path('editSettingsForm', views.editSettingsForm, name='editSettingsForm'),
    url(r'^search$', views.search, name='searchIt'),
    url(r'^categories/(?P<category_id>\d+)/$', views.choose, name='chooseIt'),
    path('userSettings', views.userSettings, name='userSettings'),
    url(r'^shoppingCart/(?P<user_id>\d+)/$', views.cart_items_list, name='list_cart_items'),
    url(r'^deleteItem/(?P<item_id>\d+)/$', views.deleteOrderItem, name='deleteOrderItem'),
    url(r'^deleteOrder/(?P<order_id>\d+)/$', views.deleteOrder, name='deleteOrder'),
]