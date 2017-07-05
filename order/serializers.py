from rest_framework import serializers
from order import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Products
        fields = '__all__'


class OrderLineSerializer(serializers.ModelSerializer):

    product = ProductSerializer()

    class Meta:
        model = models.OrderLines
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    products = OrderLineSerializer(source="orderlines_set", many=True, read_only=True)
    class Meta:
        model = models.Order
        fields = '__all__'