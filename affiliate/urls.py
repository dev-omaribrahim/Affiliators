from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from auth_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.landing_page, name="landing_page"),
    path("product/", include("product.urls", namespace="product")),
    path("accounts/", include("auth_app.urls")),
    path("cart/", include("cart_app.urls", namespace="cart_app")),
    path("order/", include("order_app.urls", namespace="order_app")),
    path("wallet/", include("wallet_app.urls", namespace="wallet_app")),
    # path('msg_support/', include('chat_app.urls', namespace='chat_app')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
