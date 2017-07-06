from order.models import Products, Order, OrderLines
import xml.etree.ElementTree as ET

class HOrderLines():

    def recordNewOrderLine(self, order, product, quantity, price):
        orderLine = OrderLines.objects.create(
                        order       = order,
                        product     = product,
                        quantity    = quantity,
                        price_unit  = price
                    )
        orderLine.save()

        return orderLine