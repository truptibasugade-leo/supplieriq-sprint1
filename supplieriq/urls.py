from django.conf.urls import patterns, url

from supplieriq import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    url(r'^$', views.ObtainAuthToken.as_view(),
        name='signin'),
    url(r'^signout', views.SignoutUser.as_view(),
        name='signout'),
    url(r'^vendors', views.VendorsAPI.as_view(),
        name='vendors'),
]