from django.shortcuts import render
from order.helpers.helper_orders import HOrder

h_order = HOrder()

def index(request):
    return render(request, 'orders.html', locals())

def order(request, id):
    order = h_order.getOrderById(id)
    return render(request, 'order-detail.html', locals())

def new(request):
    return render(request, 'new_order.html', locals())
