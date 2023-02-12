from django.db import models
from products.models import Product

from orders.models import *
# Create your models here.

class CartProcessOrders(models.Model) :
    order                = models.ForeignKey(Order, on_delete=models.CASCADE)
    id_nub_product       = models.IntegerField(blank=True, null=True)
    id_cart              = models.IntegerField(blank=True, null=True)
    product              = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_price          = models.DecimalField(blank=True, null=True, max_digits=100, decimal_places=2)
    orderd               = models.BooleanField(default=False)
    quantity             = models.IntegerField(default=0, blank=True, null=True)
    active               = models.BooleanField(default=True)

    def __str__(self) :
        return f"Product name {str(self.product)} Cart ID {self.pk}"

    def save(self, *args, **kwargs) :
        self.total_price  =  self.product.new_price_after_discound * self.quantity
        return super().save(*args, **kwargs)

ADDRESS_TYPES = (
    ('billing', 'Billing address'),
    ('shipping', 'Shipping address'),
)

class Invoice(models.Model) :
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    orders              = models.ManyToManyField(CartProcessOrders, null=True, blank=True)
    total_price         = models.DecimalField(blank=True, null=True, max_digits=100, decimal_places=2)
    total_quantity      = models.IntegerField(blank=True, null=True)
    active              = models.BooleanField(default=True)
    updated             = models.DateTimeField(auto_now=True)
    timestamp           = models.DateTimeField(auto_now_add=True)
    name                = models.CharField(max_length=120, null=True, blank=True, help_text='Shipping to? Who is it for?')
    nickname            = models.CharField(max_length=120, null=True, blank=True, help_text='Internal Reference Nickname')
    address_type        = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line_1      = models.CharField(max_length=120)
    address_line_2      = models.CharField(max_length=120, null=True, blank=True)
    city                = models.CharField(max_length=120)
    country             = models.CharField(max_length=120, default='Sudan')
    state               = models.CharField(max_length=120)
    postal_code         = models.CharField(max_length=120)
    updated             = models.DateTimeField(auto_now=True)
    timestamp           = models.DateTimeField(auto_now_add=True)
    def __str__(self) :
        return f"invoice Order {self.pk} for {str(self.user.username)}"