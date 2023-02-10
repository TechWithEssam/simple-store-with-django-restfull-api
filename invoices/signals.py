# from django.db.models.signals import m2m_changed
# from .models import Invoice

# def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
#     if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
#         orders = instance.orders.all()
#         total_price = 0
#         total_quantity = 0
#         for item in orders:
#             total_price += item.total_price
#             total_quantity += item.quantity
#         instance.total_price = total_price
#         instance.total_quantity = total_quantity
#         instance.save()
# m2m_changed.connect(m2m_changed_cart_receiver, sender=Invoice.orders.through)