from django.urls import path

from . import views

app_name = "wallet_app"


urlpatterns = [
    path("my_wallet/", views.wallet_details, name="my_wallet"),
    path("request_money/", views.request_money, name="request_money"),
    path(
        "request_money_history/",
        views.request_money_history,
        name="request_money_history",
    ),
    path(
        "current_requests/", views.current_money_requests, name="current_money_requests"
    ),
]
