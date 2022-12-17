from django.urls import path

from . import views

app_name = "order_app"

urlpatterns = [
    path("client-info/", views.order_client_info, name="order_detail"),
    path("orders_dashboard/", views.orders_dashboard, name="orders_dashboard"),
    path("orders_dashboard/", views.orders_dashboard, name="orders_dashboard"),
    path("orders/<int:pk>/", views.order_details, name="order_details"),
    path("history/", views.orders_history, name="orders_history"),
    path("history/<status>/", views.orders_history, name="orders_history"),
    path("remove_order/<int:pk>/", views.remove_order, name="remove_order"),
    path("edit_order/<int:pk>/", views.edit_order, name="edit_order"),
    path("thank_you/", views.thank_you, name="thank_you"),
    path("delivery_price/", views.delivery_price, name="delivery_price"),
]
