from django.db import models
from django.conf import settings
from orders.models import Cart
from products.models import Product

# Create your models here.

User = settings.AUTH_USER_MODEL

ADDRESS_TYPES = (
    ('billing', 'Billing address'),
    ('shipping', 'Shipping address'),
)

class OrderPlease(models.Model) :
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    product             = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity            = models.IntegerField(blank=True, null=True)
    total_price         = models.IntegerField(blank=True, null=True)
    active              = models.BooleanField(default=True)
    updated             = models.DateTimeField(auto_now=True)
    timestamp           = models.DateTimeField(auto_now_add=True)
    name                = models.CharField(max_length=120, null=True, blank=True, help_text='Shipping to? Who is it for?')
    nickname            = models.CharField(max_length=120, null=True, blank=True, help_text='Internal Reference Nickname')
    address_type        = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line_1      = models.CharField(max_length=120)
    address_line_2      = models.CharField(max_length=120, null=True, blank=True)
    city                = models.CharField(max_length=120)
    country             = models.CharField(max_length=120, default='Sudan', blank=True, null=True)
    state               = models.CharField(max_length=120)
    postal_code         = models.CharField(max_length=120)
    def __str__(self) :
        return f'{self.user}'