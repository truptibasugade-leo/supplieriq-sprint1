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
    url(r'^items', views.ItemsAPI.as_view(),
        name='items'),
    url(r'^cost', views.CostAPI.as_view(),
        name='cost'),
    url(r'^runmatch', views.RunMatchAPI.as_view(),
        name='runmatch'),
    url(r'^quote', views.QuoteAPI.as_view(),
        name='quote'),
    url(r'^purchase_order', views.PurchaseOrderAPI.as_view(),
        name='purchase_order'),
    url(r'^item_receipt', views.ItemReceiptAPI.as_view(),
        name='item_receipt'),
]
