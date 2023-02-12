from django.db.models.signals import pre_save, post_save, m2m_changed
from orders.models import Cart
from .models import CartProcessOrders, Invoice
from django.dispatch import receiver



@receiver(post_save, sender=Cart)
def pre_save_create_cart_process_orders(created, sender, instance, **kwargs) :
    if created :
        obj = CartProcessOrders.objects.create(
            product=instance.product,
            id_cart = instance.id,
            id_nub_product=instance.product.id,
            order=instance.order,
            quantity=instance.quantity
        )

def pre_save_change_product_status(sender, instance, **kwargs) :
    try :
        obj = CartProcessOrders.objects.filter()
    except :
        obj = None
    if obj :
        for item in obj :
            if item.id_nub_product == instance.product.id and item.order == instance.order:
                item.quantity = instance.quantity
                item.save()
                
pre_save.connect(pre_save_change_product_status, sender=Cart)



def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        orders = instance.orders.all()
        total_price = 0
        total_quantity = 0
        for item in orders:
            total_price += item.total_price
            total_quantity += item.quantity
        instance.total_price = total_price
        instance.total_quantity = total_quantity
        instance.save()
m2m_changed.connect(m2m_changed_cart_receiver, sender=Invoice.orders.through)