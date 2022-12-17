from django.urls import path

from . import views

app_name = "product"

urlpatterns = [
    path("home/", views.package_list, name="product_list"),
    path("home/<category>/", views.package_list, name="product_category"),
    path("package/<int:pk>/", views.package_details, name="product_details"),
    path("merchant_products/", views.merchant_products, name="merchant_products"),
]
