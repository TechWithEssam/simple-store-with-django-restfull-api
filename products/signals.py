from django.db.models.signals import pre_save
from .models import Product
from django.utils.text import slugify
from uuid import uuid4



def modify_product_slug_and_product_status_available(instance, sender, **kwargs) :
    if not instance.slug :
        instance.slug = slugify(instance.name + str(uuid4())[:10])
    if instance.inventory_quantity > 0 :
        instance.is_available = True
    else :
        instance.is_available = False
pre_save.connect(modify_product_slug_and_product_status_available, sender=Product)