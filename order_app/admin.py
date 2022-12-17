from django.contrib import admin

from .models import CitiesDeliver, Order, OrderProduct


class OrderProductInline(admin.StackedInline):
    model = OrderProduct
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]
    list_filter = ("order_status",)


admin.site.register(Order, OrderAdmin)
admin.site.register(CitiesDeliver)
admin.site.register(OrderProduct)
