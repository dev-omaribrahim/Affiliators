from django.urls import path

from . import views

app_name = "chat_app"

urlpatterns = [
    path("msg_page/", views.msg_page, name="msg_page"),
]
