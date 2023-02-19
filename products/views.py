from django.shortcuts import get_object_or_404
from rest_framework import generics,permissions, authentication, status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from .models import *
from .serializers import *
import requests

class CategoriesApiView(generics.ListAPIView) :
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
categories_api_view = CategoriesApiView.as_view()

class BrandsApiView(generics.ListAPIView) :
    queryset = Brand.objects.all()
    serializer_class = BrandSerializers
brand_api_view = BrandsApiView.as_view()


class HomeProductView(generics.ListAPIView) :
    queryset = Product.objects.all()
    serializer_class = ProductSerailizers

    def get_queryset(self):
        request = self.request
        obj = Product.objects.all()
        price_q = request.query_params.get("price")
        categories = request.query_params.get("categories")
        brands = request.query_params.get("brands")
        ordering = request.query_params.get("ordering")
        if price_q :
            obj = obj.filter(price__lte=price_q)
        if categories :
            obj = obj.filter(category__name=categories)
        if brands :
            obj = obj.filter(brand__name=brands)
        if ordering :
            item = ordering.split(",")
            obj = obj.order_by(*item)
        return obj
home_product_view = HomeProductView.as_view()

class DetailProductView(generics.RetrieveAPIView) :
    queryset = Product.objects.all()
    serializer_class = ProductSerailizers
    lookup_field = 'slug'

detail_product_view = DetailProductView.as_view()



class AddNewProductView(generics.ListCreateAPIView) :
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializers
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(salesman=self.request.user)
add_new_prodcut_view = AddNewProductView.as_view()


class UpdateProductView(generics.UpdateAPIView) :
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializers
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    def perform_update(self, serializer):
        serializer.save(salesman=self.request.user)
        return super().perform_update(serializer)
update_product_view = UpdateProductView.as_view()


@api_view(["PUT", "GET"])
@permission_classes([permissions.IsAuthenticated])
def update_product_view(request, pk) :
    try :
        obj = Product.objects.get(pk=pk)
    except :
        return Response({"masg": "not found"})
    serializer = CreateProductSerializers(data=request.data, instance=obj)
    if serializer.is_valid(raise_exception=True) :
        salesman = serializer.validated_data.get("salesman")
        if request.user == salesman :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteProductView(generics.DestroyAPIView) :
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializers
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"
    def perform_destroy(self, instance):
        print(instance.salesman)
        if self.request.user == instance.salesman :
            return super().perform_destroy(instance)
delete_product_view = DeleteProductView.as_view()


@api_view(["POST", "GET"])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def add_rate_api_view(request, slug) :
    qs = get_object_or_404(Product, slug=slug)
    serializer = AddRateSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True) :
        serializer.save(user=request.user, product=qs)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT", "GET"])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def update_rate_user_view(request, slug, pk) :
    product = Product.objects.get(slug=slug)
    rate = get_object_or_404(Rate, pk=pk)
    serializer = AddRateSerializers(data=request.data, instance=rate)
    if serializer.is_valid(raise_exception=True) :
        if  request.user == rate.user :
            serializer.save()
            return Response({"message": "your rate's editing "}, status=status.HTTP_200_OK)
        return Response({"message" : f"hi {request.user} this rate is not for you this for {rate.user}"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def delele_rate_api_view(request,pk) :
    url = "http://127.0.0.1:8000/"
    items = requests.get(url)
    print(items.content)
    try :
        qs = Rate.objects.get(pk=pk) 
    except :
        qs= None
    if qs :
        if request.method == "DELETE" :
            if request.user == qs.user :
                qs.delete()
                return Response({"message" : "deleted is done!!!"},status=status.HTTP_200_OK)
        return Response({"message" : "not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    return Response({"message" : "not found"}, status=status.HTTP_404_NOT_FOUND)