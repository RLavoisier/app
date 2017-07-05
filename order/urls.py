from django.conf.urls import url
from . import views

urlpatterns = [
    # Index View
    url(r'^$', views.orders),
    url(r'^(\d+)$', views.order),
]