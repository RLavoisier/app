from django.conf.urls import url
from . import views

urlpatterns = [
    # Index View
    url(r'^$', views.orders),
    url(r'^(\d+)$', views.order),
    url(r'^(\d+)/add_details$', views.orderDetails),
    url(r'^search$', views.search),
]