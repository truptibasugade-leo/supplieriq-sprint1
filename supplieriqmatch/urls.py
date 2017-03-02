from django.conf.urls import patterns, url

from supplieriqmatch import views


urlpatterns = [
    url(r'^cost_parameter', views.MatchAPI.as_view(),
        name='cost_parameter'),
]
