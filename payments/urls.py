from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.account_list, name="account_list"),
]