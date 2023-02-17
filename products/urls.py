from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    path('', views.home_product_view, name="home"),
    path('categories/', views.categories_api_view, name="categories"),
    path('brands/', views.brand_api_view, name="brands"),
    path("detail/<slug>/", views.detail_product_view, name="detail_product"),
    path("add-product/", views.add_new_prodcut_view, name="add_new_product"),
    path("update-product/<int:pk>/", views.update_product_view, name="update_product"),
    path("delete-product/<int:pk>/", views.delete_product_view, name="delete_product"),
    path("detail/<slug>/rate/", views.add_rate_api_view, name="add_rate"),
    path("detail/<slug>/update-rate/<int:pk>/", views.update_rate_user_view, name="update_rate"),
    path("delete-rate/<pk>/", views.delele_rate_api_view, name="delete_rate")
]