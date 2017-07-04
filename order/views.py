# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from order.models import Order, OrderLines, Products
from order.serializers import OrderSerializer, OrderLineSerializer


"""
    CRUD Operations for ORDERS
"""

@csrf_exempt
def orders(request):
    """
        INDEX view for orders
    """
    #Showing all orders
    if request.method == "GET":
        orders          = Order.objects.all()
        serializer      = OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data, safe=False)

    #Creating an order
    elif request.method == "POST":
        serializer = OrderSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def order(request, id):
    """
        Getting an order fr the current id
    """

    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExists:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return JsonResponse(serializer.data)

    elif request.method == "DELETE":
            order.delete()
            return JsonResponse({ "response": 'deleted' }, safe=False)
