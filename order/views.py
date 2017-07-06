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
from order.helpers.helper_orders import HOrder
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

"""
    CRUD Operations for ORDERS
"""

h_json   = HJsonResponse()
h_order  = HOrder()

@csrf_exempt
@api_view(['POST', 'GET', 'PUT'])
@parser_classes((FormParser, MultiPartParser, JSONParser,))
def orders(request, format=None):
    """
        INDEX view for orders
    """

    #Showing all orders
    if request.method == "GET":
        orders          = h_order.getSerializedAllOrders()
        return h_json.getResponse(False, "OK", orders)

    #Creating an order
    elif request.method == "POST":
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return h_json.getResponse(False, "OK", serializer.data)
        return h_json.getResponse(True, serializer.errors, None)

    # Not very "RESTFULLY" replacing the order list with the XML API
    elif request.method == "PUT":
        if(h_order.replaceOrderWithXMLData()):
            orders = h_order.getSerializedAllOrders()
            return h_json.getResponse(False, "OK", orders)
        else:
            return h_json.getResponse(True, "Error during xml parsing", None)

@csrf_exempt
def order(request, id):
    """
        Getting an order fr the current id
    """
    try:
        order               = h_order.getOrderById(id)
        serializedOrder     = h_order.getSerializedOrder(order)
    except:
        return h_json.getResponse(True, "Not Found", None)

    if request.method == 'GET':
        return h_json.getResponse(False, "OK", serializedOrder)

    elif request.method == "DELETE":
            order.delete()
            return h_json.getResponse(False, "OK", None)
