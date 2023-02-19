from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import *
from .public_serializers import *
from products.public_serializers import *

class OrdersSerializers(serializers.ModelSerializer) :
    user = PublicUserSerializers(read_only=True)
    class Meta :
        model = Order
        fields = [
            "user",
            "created",
            "cart_total",
            "cart_items",
        ]


class CartsSerializers(serializers.ModelSerializer) :
    product = PublicProductSerializer(read_only=True)
    order = OrdersSerializers(read_only=True)
    checkout_url = serializers.SerializerMethodField(read_only=True)
    class Meta :
        model = Cart
        fields = [
            "pk",
            "order",
            "product",
            "quantity",
            "total_price_cart",
            "checkout_url",
        ]
    def get_product(self, obj) :
        return obj
    

    def get_checkout_url(self, obj) :
        request = self.context.get("request")
        return reverse("cart:checkout", request=request)