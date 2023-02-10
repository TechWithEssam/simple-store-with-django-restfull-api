from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import  Product


class PublicUserSerializers(serializers.Serializer) :
    pk = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)


