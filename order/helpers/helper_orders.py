from order.models import Order, OrderLines
from order.serializers import OrderSerializer, OrderLineSerializer
from order.helpers.helper_products import HProducts
from order.helpers.helper_orderlines import HOrderLines
import xml.etree.ElementTree as ET
from urllib.request import urlopen

class HOrder():
    def __init__(self):
        self.lengowOrderApiUrl = "http://test.lengow.io/orders-test.xml"


    """
        Gets all order objects
    """
    def getAllOrders(self):
        orders = Order.objects.all()
        return orders
    """
        Gets an order by ID
    """
    def getOrderById(self, id):
        order = Order.objects.get(id=id)
        return order

    """"
            Return a set of orders from a query
    
    """
    def getOrders(self, order_id, customer_first_name, marketplace):
        # setting up the filters
        order_id_filter             = {} if order_id            == None else { "order_id__icontains" : order_id }
        customer_first_name_filter  = {} if customer_first_name == None else { "customer_first_name__icontains" : customer_first_name }
        marketplace_filter          = {} if marketplace         == None else { "marketplace__icontains" : marketplace}

        # gettings the filtered results
        orders = Order.objects\
            .filter(**order_id_filter)\
            .filter(**customer_first_name_filter)\
            .filter(**marketplace_filter)

        return orders

    """"
            Return a serialized set of orders from a query
    
    """
    def getSerializedOrders(self, order_id, customer_first_name, marketplace):
        orders = self.getOrders(order_id, customer_first_name, marketplace)
        serializer = OrderSerializer(orders, many=True)
        return serializer.data

    """
        gets a serialized object for all orders
    """
    def getSerializedAllOrders(self):
        orders      = self.getAllOrders()
        serializer  = OrderSerializer(orders, many=True)
        return serializer.data

    """
        gets a serialized object for an order by id
    """
    def getSerializedOrderById(self, id):
        order       = h_order.getOrderById(id)
        serializer  = OrderSerializer(order, many=True)
        return serializer.data

    """
        Returns a serialized Order object
    """

    def getSerializedOrder(selfself, order):
        return OrderSerializer(order, many=True)

    """"
        Delete all orders
    """
    def deleteAllOrders(self):
        Order.objects.all().delete()

    """
        Replace the order records with the ones provided
        in the lengow XML api
    """
    def replaceOrderWithXMLData(self):
        # getting a helper for products handling
        h_products      = HProducts()
        h_orderlines    = HOrderLines()

        self.deleteAllOrders()

        #Reading the XML FILE from URL
        xml     = urlopen(self.lengowOrderApiUrl)
        xmlTree = ET.ElementTree(file=xml)
        root    = xmlTree.getroot()

        #iterating through all the "order" elements
        for xmlOrder in root.iter("order"):
            # getting an Order object from the XML Element
            order = self.createOrderObjectFromXMLElement(xmlOrder)

            # getting all the products and creating the OrderLines
            for xmlProduct in xmlOrder.iter("product"):
                # gets the product from the DB
                product     = h_products.getProductFromXml(xmlProduct)
                #record a new OrderLine
                quantity    = xmlProduct.find("quantity").text
                price_unit  = xmlProduct.find("price_unit").text

                h_orderlines.recordNewOrderLine(order, product, quantity, price_unit)

        return True



    """
        Creates an order from an XML tree element
    """
    def createOrderObjectFromXMLElement(self, xmlOrder):
        # fetching the infos from the XML
        if xmlOrder.find("marketplace").text:
            marketplace         = xmlOrder.find("marketplace").text
        else:
            marketplace         = "Unknown"

        if xmlOrder.find("order_id").text:
            order_id            = xmlOrder.find("order_id").text
        else:
            order_id            = "Unknown"

        if xmlOrder.find("order_status").find("marketplace").text:
            mp_order_status     = xmlOrder.find("order_status").find("marketplace").text
        else:
            mp_order_status     = "Unknown"

        if xmlOrder.find("order_status").find("lengow").text:
            lg_order_status     = xmlOrder.find("order_status").find("lengow").text
        else:
            lg_order_status     = "Unknown"

        if xmlOrder.find("order_amount").text:
            order_amount        = xmlOrder.find("order_amount").text
        else:
            order_amount        = 0

        if xmlOrder.find("billing_address").find("billing_lastname").text:
            customer_first_name = xmlOrder.find("billing_address").find("billing_lastname").text
        else:
            customer_first_name = "Unknown"


        # creating an Order
        order = Order.objects.create(
                        marketplace         = marketplace,
                        order_id            = order_id,
                        mp_order_status     = mp_order_status,
                        lg_order_status     = lg_order_status,
                        order_amount        = order_amount,
                        customer_first_name = customer_first_name
                    )

        order.save()

        return order



