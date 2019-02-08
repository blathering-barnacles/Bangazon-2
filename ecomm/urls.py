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
    # path('search/', views.searchProduct, name='search')
    url(r'^search$', views.search, name='searchIt'),
]