from django.urls import path

from . import views

app_name = "cart_app"


urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("ajax/", views.cart_detail_ajax, name="cart_detail_ajax"),
    # path('add/<int:product_id>/', views.cart_add, name="cart_add"),
    path("add/", views.cart_add, name="cart_add"),
    path("remove/<int:product_id>/<size>/", views.cart_remove, name="cart_remove"),
]
