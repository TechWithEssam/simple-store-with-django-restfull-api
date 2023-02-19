from rest_framework import serializers
from .models import *
from rest_framework.reverse import reverse
from .public_serializers import *



class CategorySerializers(serializers.ModelSerializer) :
    class Meta :
        model = Category
        fields = "__all__"

class BrandSerializers(serializers.ModelSerializer) :
    class Meta :
        model = Brand
        fields = "__all__"

class CreateProductSerializers(serializers.ModelSerializer) :
    class Meta :
        model = Product
        exclude = ["salesman", "is_available", "slug"]




class ProductSerailizers(serializers.ModelSerializer) :
    rate = AllRateAndCommentInLineRelated(source="all_rated_product",read_only=True, many=True)
    owner = PublicUserSerializers(read_only=True, source="salesman")
    new_product_url = serializers.SerializerMethodField(read_only=True)
    brand_name = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)
    home_url = serializers.SerializerMethodField(read_only=True)
    categories_url = serializers.SerializerMethodField(read_only=True)
    brands_url = serializers.SerializerMethodField(read_only=True)
    delete_product_url = serializers.SerializerMethodField(read_only=True)
    # order_now_url = serializers.SerializerMethodField(read_only=True)
    cart_url = serializers.SerializerMethodField(read_only=True)
    add_to_cart_url = serializers.SerializerMethodField(read_only=True)
    add_rate_url = serializers.SerializerMethodField(read_only=True)
    update_product_url = serializers.HyperlinkedIdentityField(view_name="products:update_product", lookup_field="pk")
    detail_product_url = serializers.HyperlinkedIdentityField(view_name="products:detail_product", lookup_field="slug")
    class Meta :
        model = Product
        fields = [
            "pk",
            "owner",
            "name",
            "image",
            "price",
            "new_price_after_discound",
            "discound",
            "gender",
            "category_name",
            "brand_name",
            "description",
            "inventory_quantity",
            "is_available",
            "home_url",
            "detail_product_url",
            "categories_url",
            "brands_url",
            "new_product_url",
            "update_product_url",
            "delete_product_url",
            # "order_now_url",
            "cart_url",
            "add_to_cart_url",
            "add_rate_url",
            "count_reated_user",
            "average_rating",
            "rate",
        ]
    

    def get_average_rating(self, obj) :
        return obj
    def get_cart_url(self, obj) :
        return reverse("orders:cart", request=self.context.get("request"))
    
    def get_add_rate_url(self, obj) :
        request = self.context.get("request")
        if not request  :
            return None
        return reverse("products:add_rate", kwargs={"slug": obj.slug}, request=request)

    def get_add_to_cart_url(self, obj) :
        return reverse("orders:add_to_cart", request=self.context.get("request"))

    def get_home_url(self, obj) :
        request = self.context.get("request")
        if not request :
            return None
        return reverse("products:home", request=request)
    
    def get_brand_name(self, obj) :
        return obj.brand.name
    
    def get_category_name(self, obj) :
        return obj.category.name

    def get_brands_url(self, obj) :
        request = self.context.get("request")
        if not request :
            return None
        return reverse("products:brands", request=request)
    
    def get_categories_url(self, obj) :
        request = self.context.get("request")
        if not request :
            return None
        return reverse("products:categories", request=request)
    
    def get_new_product_url(self, obj) :
        return reverse("products:add_new_product", request=self.context.get("request"))


    def get_delete_product_url(self, obj) :

        return reverse("products:delete_product", kwargs={"pk":obj.pk}, request=self.context.get("request"))
        
    # def get_order_now_url(self, obj) :
    #     return reverse("orderplease:order_now", request=self.context.get("request"))


class AddRateSerializers(serializers.ModelSerializer) :
    update_rate_url = serializers.SerializerMethodField(read_only=True)
    class Meta :
        model = Rate
        fields = (
            "pk",
            "comment",
            "rate",
            "rated_date",
            "updated",
            "update_rate_url"
        )


    def get_update_rate_url(self, obj) :
        request = self.context.get("request")
        if not request :
            return None
        return reverse("products:update_rate", kwargs={"slug":obj.product.slug, "pk":obj.pk}, request=request)