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
        obj = Product.objects.all().order_by("?")
        price_q = request.query_params.get("price")
        categories = request.query_params.get("categories")
        brands = request.query_params.get("brands")
        if price_q :
            obj = obj.filter(price__lte=price_q)
        if categories :
            obj = obj.filter(category__name=categories)
        if brands :
            obj = obj.filter(brand__name=brands)
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