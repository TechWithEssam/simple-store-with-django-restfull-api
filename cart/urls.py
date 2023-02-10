from django.urls import path
from . import views


app_name = "cart"
urlpatterns = [
    path('checkout/', views.check_out_api_view, name="checkout")
]