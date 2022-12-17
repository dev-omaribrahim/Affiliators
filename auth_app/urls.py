from django.urls import include, path

from . import views

urlpatterns = [
    path("signup/", views.sign_up, name="sign_up"),
    path("login/", views.sign_in, name="sign_in"),
    path("logout/", views.sign_out, name="sign_out"),
    path("under_review/", views.account_under_review, name="account_under_review"),
    path("", include("django.contrib.auth.urls")),
]
