from rest_framework import generics, status, permissions, authentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import *
from .serializers import *
from orders.models import *
from django.utils import timezone
from django.db.models import Q
from products.models import Product
# Create your views here.


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def order_please_view(request) :
    obj, _ = Order.objects.new_or_get(request)
    qs = obj.user.username
    cart = Cart.objects.filter(order__user__username=qs)
    user = obj.user
    serializer = OrderPleaseSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True) :
        name                = serializer._validated_data.get('name')
        nickname            = serializer._validated_data.get('nickname')
        address_type        = serializer._validated_data.get('address_type')
        address_line_1      = serializer._validated_data.get('address_line_1')
        address_line_2      = serializer._validated_data.get('address_line_2')
        city                = serializer._validated_data.get('city')
        country             = serializer._validated_data.get('country')
        state               = serializer._validated_data.get('state')
        postal_code         = serializer._validated_data.get('postal_code')
        if cart  :
            for item in cart :
                order= OrderPlease.objects.create(
                    product=item.product,
                    quantity=item.quantity,
                    total_price=item.total_price_cart,
                    user=user,
                    name=name,
                    nickname=nickname,
                    address_type=address_type,
                    address_line_1=address_line_1,
                    address_line_2=address_line_2,
                    city=city,
                    country=country,
                    state=state,
                    postal_code=postal_code,
                    )
                item.delete()
                product = Product.objects.get(name=order.product.name)
                product.inventory_quantity -= order.quantity
                product.save()
        else :
            return Response({"message": "can't doing order becouse don't have products in your cart"})
        return Response({"message": "your order has been created...."}, status=status.HTTP_201_CREATED)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)