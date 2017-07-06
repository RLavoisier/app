# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from order.serializers import OrderSerializer
from order.models import Order
from order.helpers.helper_jsonresponse import HJsonResponse
from order.helpers.helper_orders import HOrder
from order.helpers.helper_products import HProducts
from order.helpers.helper_orderlines import HOrderLines
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
import json

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

"""
        Route for creating OrderLines
        //TODO Error fetching

"""
@csrf_exempt
@api_view(['POST'])
@parser_classes((FormParser, MultiPartParser, JSONParser,))
def orderDetails(request, id, format=None):
    # Getting the helpers
    h_products      = HProducts()
    h_orderlines    = HOrderLines()
    h_order         = HOrder()

    if request.method == "POST":
        # getting the order
        order = h_order.getOrderById(id)

        for product in request.data:
            #creating the product
            # converting the string to Json
            jsonStringProduct   = str(product).replace("'", '"')
            jsonProduct         = json.loads(jsonStringProduct)
            print(jsonProduct["product"]["sku"])

            #Creating the Products instance
            newProduct          = h_products.getProductsInstance(
                                                jsonProduct["product"]["sku"],
                                                jsonProduct["product"]["title"],
                                                jsonProduct["product"]["category"],
                                                jsonProduct["product"]["image_url"])
            dbProduct = h_products.getOrCreateProductBySku(newProduct)
            #creating the line
            h_orderlines.recordNewOrderLine(
                            order,
                            dbProduct,
                            jsonProduct["quantity"],
                            jsonProduct["price_unit"])

        return h_json.getResponse(False, "OK", None)


"""
        Route for order details

"""
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

@csrf_exempt
def search(request):
    if request.GET:
        # getting the params from the get request
        order_id            = request.GET.get("order_id")
        customer_first_name = request.GET.get("customer_first_name")
        marketplace         = request.GET.get("marketplace")

        orders = h_order.getSerializedOrders(order_id, customer_first_name, marketplace)
        return h_json.getResponse(False, "OK", orders)