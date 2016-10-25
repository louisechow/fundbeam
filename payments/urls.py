from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.account_list, name="account_list"),
    url(r'^pay', views.make_payment, name="payment_form"),
    url(r'^account_transactions', views.account_transactions, name="account_transactions")
]