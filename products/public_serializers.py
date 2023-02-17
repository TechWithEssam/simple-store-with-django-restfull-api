from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import  *


class PublicUserSerializers(serializers.Serializer) :
    pk = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)



class AllRateAndCommentInLineRelated(serializers.ModelSerializer) :
    user = PublicUserSerializers(read_only=True)
    update_rate_url = serializers.SerializerMethodField(read_only=True)
    delete_rate_url = serializers.SerializerMethodField(read_only=True)
    class Meta :
        model = Rate
        fields = (
            "pk",
            "user",
            "product",
            "comment",
            "rate",
            "rated_date",
            "updated",
            "update_rate_url",
            "delete_rate_url"
        )
    def get_update_rate_url(self, obj) :
        request = self.context.get("request")
        if not request :
            return None
        return reverse("products:update_rate", kwargs={"slug":obj.product.slug, "pk":obj.pk}, request=request)
    def get_delete_rate_url(self, obj) :
        return reverse("products:delete_rate", kwargs={"pk":obj.pk}, request=self.context.get("request"))
