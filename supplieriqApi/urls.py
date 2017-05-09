from django.conf.urls import patterns, url

from supplieriqApi import views


urlpatterns = [
    url(r'^vendor', views.VendorsAPI.as_view(),
        name='vendor'),
    url(r'^item', views.ItemsAPI.as_view(),
        name='item'),
]
