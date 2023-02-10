from rest_framework .response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework import status, permissions
from .models import Invoice, CartProcessOrders
from orders.models import Cart, Order
from .serializers import CheckOutSerializers
from products.models import Product

@api_view(["POST", "GET"])
def check_out_api_view(request) :
    obj, _ = Order.objects.new_or_get(request)
    qs = obj.user.username
    items_cart = Cart.objects.filter(order__user__username=qs)
    cart = CartProcessOrders.objects.filter(order__user__username=qs,orderd=False, active=True)
    user = obj.user
    serializer = CheckOutSerializers(data=request.data)
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
            order= Invoice.objects.create(
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
            for item in cart :
                if item.orderd == False :
                    order.orders.add(item)
                    item.orderd = True
                    item.save()
                    product = Product.objects.get(name=item.product.name)
                    product.inventory_quantity -= item.quantity
                    product.save()
                    items_cart.delete()
            return Response({"message" : "your order is ready...."}, status=status.HTTP_201_CREATED)
        else :
            return Response({"message" : "can't orderd you dont have product "})
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

