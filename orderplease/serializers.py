from rest_framework import serializers
from .models import *


class OrderPleaseSerializers(serializers.ModelSerializer) :
    class Meta :
        model = OrderPlease
        exclude = (
            "user",
            "product",
            "quantity",
            "total_price",
            "active"
        )