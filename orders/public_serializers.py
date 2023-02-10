from rest_framework import serializers
from products.models import Product
from store import settings

ActionAddToCartList = settings.ActionAddToCartList
ListOptionsCustomizeHisCart = settings.ListOptionsCustomizeHisCart
class ActionAddToCart(serializers.Serializer) :
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value) :
        value = value.strip().lower()
        if not value in ActionAddToCartList :
            raise serializers.ValidationError(f"your input is bad please chose one of them {ActionAddToCartList}")
        return value

class ListOptionsCustomizeCart(serializers.Serializer) :
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value) :
        value = value.strip().lower()
        if not value  in ListOptionsCustomizeHisCart :
            raise serializers.ValidationError(f"you can add action to customize cart with those command {ListOptionsCustomizeHisCart}")
        return value





class PublicProductSerializer(serializers.ModelSerializer) :
    brand_name = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)
    class Meta :
        model =Product
        fields = [
            "name",
            "image",
            "price",
            "new_price_after_discound",
            "brand_name",
            "category_name",
            "gender",
            "discound",
            "inventory_quantity",
            "is_available",
            "description"
        ]
    def get_brand_name(self, obj) :
        return obj.brand.name

    def get_category_name(self, obj) :
        return obj.category.name