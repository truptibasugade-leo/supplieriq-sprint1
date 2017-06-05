from django.conf.urls import patterns, url

from supplieriqApi import views


urlpatterns = [
    url(r'^vendor', views.VendorsAPI.as_view(),
        name='vendor'),
    url(r'^item', views.ItemsAPI.as_view(),
        name='item'),
    url(r'^runmatch', views.RunMatchAPI.as_view(),
        name='runmatch'),
    url(r'^signin', views.SigninApi.as_view(),
        name='signin'),
]
