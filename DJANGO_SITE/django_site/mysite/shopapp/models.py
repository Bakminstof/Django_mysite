from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):
    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'
        ordering = ['name']

    name = models.CharField(verbose_name='Item name', max_length=100)
    description = models.TextField(verbose_name='Description', null=False, blank=True)
    price_cent = models.DecimalField(verbose_name='Price', max_digits=10, decimal_places=0)  # In cents

    def price_usd(self):
        return self.price_cent / 100


class Tax(models.Model):
    class Meta:
        verbose_name = 'tax'
        verbose_name_plural = 'taxes'
        ordering = ['value']

    value = models.PositiveSmallIntegerField(verbose_name='Tax')


class Discount(models.Model):
    class Meta:
        verbose_name = 'discount'
        verbose_name_plural = 'discounts'
        ordering = ['value']

    value = models.PositiveSmallIntegerField(verbose_name='Discount')


class Order(models.Model):
    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ['name']

    name = models.CharField(verbose_name='Order name', max_length=100)
    total_price_cent = models.DecimalField(verbose_name='Total price', max_digits=10, decimal_places=0)  # In cents

    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, related_name='orders', null=True, default=None)
    items = models.ManyToManyField(Item, related_name='orders')
    tax = models.ForeignKey(Tax, on_delete=models.SET_DEFAULT, related_name='orders', default=1)
    discount = models.ForeignKey(Discount, on_delete=models.SET_DEFAULT, related_name='orders', default=1)

    def total_price_usd(self):
        return self.total_price_cent / 100
