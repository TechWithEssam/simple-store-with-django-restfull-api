from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    path("cart/", views.cart_customer_view, name="cart"),
    path("add-to-cart/", views.action_add_to_cart_view, name="add_to_cart"),
    path("custome-cart/", views.coustomize_cart_customer_view, name="customize_cart"),
]