from django.db import models
from django.conf import settings
from products.models import Product


User = settings.AUTH_USER_MODEL


class OrderManager(models.Manager):
    def new_or_get(self, request):
        order_id = request.session.get("order_id", None)
        qs = self.get_queryset().filter(id=order_id)
        if qs.count() == 1:
            new_obj = False
            order_obj = qs.first()
            if request.user.is_authenticated and order_obj.user is None:
                order_obj.user = request.user
                order_obj.save()
        else:
            order_obj = Order.objects.new(user=request.user)
            new_obj = True
            request.session['order_id'] = order_obj.id
        return order_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class Order(models.Model) :
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = OrderManager()

    def __str__(self) :
        if self.user :
            return f"{str(self.user)} {self.pk}"
        return f"{self.pk}"
    
    @property
    def cart_total(self):
        cartitem = self.cart_set.all()
        total = sum([item.total_price_cart for item in cartitem])
        return total 

    @property
    def cart_items(self):
        cartitem = self.cart_set.all()
        total = sum([item.quantity for item in cartitem])
        return total 

class Cart(models.Model) :
    order                = models.ForeignKey(Order, on_delete=models.CASCADE)
    product              = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_price          = models.DecimalField(blank=True, null=True, max_digits=100, decimal_places=2)
    quantity             = models.IntegerField(default=0)

    def save(self, *args, **kwrgs) :
        if self.quantity > self.product.inventory_quantity :
            self.quantity = self.product.inventory_quantity
        return super().save(*args, **kwrgs)
        
    def save(self, *args, **kwargs) :
        self.total_price  =  self.product.new_price_after_discound * self.quantity
        return super().save(*args, **kwargs)
    def __str__(self) :
        return f"{self.id} {self.product.name} - {self.quantity}"

    @property
    def total_price_cart(self) :
        total = self.product.new_price_after_discound * self.quantity 
        return total