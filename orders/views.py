from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics, status, permissions, authentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import *
from .serializers import *
from .public_serializers import *
from products.models import Product
import requests
# Create your views here.


@api_view(["GET"])
def cart_customer_view(request) :
    if not request.user.is_authenticated :
        obj, _ = Order.objects.new_or_get(request)
        cart = Cart.objects.filter(order=obj)
        for item in cart :
            product = Product.objects.get(name=item.product.name)
            if item.quantity > product.inventory_quantity and obj == item.order:
                item.quantity = product.inventory_quantity
                if product.inventory_quantity <= 0 :
                    item.delete()
    else :
        obj, _ = Order.objects.new_or_get(request)
        obj = obj.user.username
        cart = Cart.objects.filter(order__user__username=obj)
    for item in cart :
        product = Product.objects.get(name=item.product.name)
        if item.quantity > product.inventory_quantity:
            item.quantity = product.inventory_quantity
            if product.inventory_quantity <= 0 :
                item.delete()
    serializer = CartsSerializers(cart, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def action_add_to_cart_view(request) :
    serializer = ActionAddToCart(data=request.data)
    if serializer.is_valid(raise_exception=True) :
        id = serializer.validated_data.get("id")
        action = serializer.validated_data.get("action")
        if id :
            product = get_object_or_404(Product, id=id)
            order, _ = Order.objects.new_or_get(request)
        
        if product :
            if action == "add" :
                cart, _ = Cart.objects.get_or_create(product=product, order=order)
                if cart.product.name :
                    if cart.product.is_available :
                        if cart.product.inventory_quantity > cart.quantity :
                            cart.quantity += 1
                            cart.save()
                            cart_serializer = CartsSerializers(cart).data
                            return Response(cart_serializer, status=status.HTTP_200_OK)
                        else :
                            cart.quantity = cart.product.inventory_quantity
                            cart.save()
                            return Response({"message": f"can't add more than {cart.product.inventory_quantity} becouse the qauntity is avalible in inventory {cart.product.inventory_quantity}"})
                    else :
                        return Response({"message" : f"'{cart.product.name}' is not aavailable"})
            elif action == "remove" :
                try :
                    cart = Cart.objects.filter(Q(product=product) | Q(order=order))
                except :
                    cart = None
                print(cart)
                if cart:
                    cart.delete()
                    return Response({"message": "delete this product from cart...."})
                else :
                    return Response({"message": f"not found product with this id {id}"}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT"])
def coustomize_cart_customer_view(request) :

    if not request.user.is_authenticated :
        obj, _ = Order.objects.new_or_get(request)
        cart = Cart.objects.filter(order=obj)
    else :
        obj, _ = Order.objects.new_or_get(request)
        obj = obj.user.username
        cart = Cart.objects.filter(order__user__username=obj)

    serializer = ListOptionsCustomizeCart(data=request.data)
    if serializer.is_valid(raise_exception=True) :
        id = serializer.validated_data.get("id")
        action = serializer.validated_data.get("action")

        try :
            obj = cart.get(id=id)
        except :
            obj = None
        if obj :
            if action == "plus" :
                if obj.product.is_available :
                    if obj.product.inventory_quantity > obj.quantity :
                        obj.quantity += 1
                        obj.save()
                        cart_serializer = CartsSerializers(obj).data
                        return Response(cart_serializer, status=status.HTTP_200_OK)
                    else :
                        obj.quantity = obj.product.inventory_quantity
                        obj.save()
                        return Response({"message": f"can't add more than {obj.product.inventory_quantity} becouse the qauntity is avalible in inventory {obj.product.inventory_quantity}"})
                else :
                    return Response({"message" : f"'{obj.product.name}' is not aavailable"})
            
            elif action == "minus" :
                obj.quantity -= 1
                obj.save()
                if obj.quantity == 0 :
                    obj.delete()
                    return Response({"message": f"'{obj.product.name}' deleted from cart"})
                cart_serializer = CartsSerializers(obj).data
                return Response(cart_serializer, status=status.HTTP_200_OK)
            elif action == "remove" :
                obj.delete()
                return Response({"message": "delete this product from cart...."})
            else :
                return Response({"message": "this action is not found"})
        else :
            return Response({"message" : f"no have item cart with id {id}"})
    return Response({"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST)
