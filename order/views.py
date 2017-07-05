# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from order.models import Order, OrderLines, Products
from order.serializers import OrderSerializer, OrderLineSerializer
from order.helpers.helper_jsonresponse import HJsonResponse

"""
    CRUD Operations for ORDERS
"""

@csrf_exempt
def orders(request):
    """
        INDEX view for orders
    """
    hjson = HJsonResponse()

    #Showing all orders
    if request.method == "GET":
        orders          = Order.objects.all()
        serializer      = OrderSerializer(orders, many=True)
        return hjson.getResponse(False, "OK", serializer.data)

    #Creating an order
    elif request.method == "POST":
        serializer = OrderSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return hjson.getResponse(False, "OK", serializer.data)
        return hjson.getResponse(True, "Error", None)

@csrf_exempt
def order(request, id):
    """
        Getting an order fr the current id
    """

    hjson = HJsonResponse()

    try:
        order = Order.objects.get(id=id)
    except:
        return hjson.getResponse(True, "No Found", None)

    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return hjson.getResponse(False, "OK", serializer.data)

    elif request.method == "DELETE":
            order.delete()
            return hjson.getResponse(False, "OK", None)
