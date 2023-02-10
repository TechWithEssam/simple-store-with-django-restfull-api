from rest_framework import serializers
from rest_framework.reverse import reverse

from products.models import Product
class ContextProcessorsSerializer(serializers.Serializer) :
    cart_url = serializers.SerializerMethodField(read_only=True)
    class Meta :
        model = Product
        fields = (
            "cart_url"
        )

    def get_cart_url(self, obj) :
        return reverse("orders:cart", request=self.context.get("request"))

def all_urls(request) :
    qs = Product.objects.all()
    serializer = ContextProcessorsSerializer(qs, many=True).data
    return serializer