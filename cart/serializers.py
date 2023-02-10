from rest_framework import serializers
from .models import Invoice


class CheckOutSerializers(serializers.ModelSerializer) :
    class Meta :
        model = Invoice
        exclude = (
            "user",
            "orders",
            "total_quantity",
            "total_price",
            "active"
        )