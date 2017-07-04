# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Products(models.Model):
    sku                 = models.CharField(max_length=30)
    title               = models.CharField(max_length=50)
    category            = models.CharField(max_length=30)
    image_url           = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Order(models.Model):
    marketplace         = models.CharField(max_length=30)
    order_id            = models.CharField(max_length=30)
    mp_order_status     = models.CharField(max_length=30)
    lg_order_status     = models.CharField(max_length=30)
    order_amount        = models.FloatField()
    order_date          = models.DateField(auto_now_add=True)
    customer_first_name = models.CharField(max_length=50)
    products            = models.ManyToManyField(Products, through='OrderLines')

    def __str__(self):
        return self.order_id

class OrderLines(models.Model):
    order               = models.ForeignKey(Order)
    product             = models.ForeignKey(Products)
    quantity            = models.IntegerField()
    price_unit          = models.FloatField()
