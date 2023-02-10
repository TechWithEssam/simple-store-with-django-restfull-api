from django.db import models
from orderplease.models import OrderPlease
from django.conf import settings


User = settings.AUTH_USER_MODEL
# Create your models here.


# class Invoice(models.Model) :
#     orders           = models.ManyToManyField(OrderPlease, null=True)
#     user            = models.ForeignKey(User, on_delete=models.CASCADE)
#     total_price     = models.IntegerField(blank=True, null=True)
#     total_quantity  = models.IntegerField(blank=True, null=True)
#     updated         = models.DateTimeField(auto_now=True)
#     timestamp       = models.DateTimeField(auto_now_add=True)

#     def __str__(self) :
#         return f"invoice {str(self.user.username)}"
