from rest_framework import serializers
from order import models


class OrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderLines
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = '__all__'