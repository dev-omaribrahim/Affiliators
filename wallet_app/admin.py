from django.contrib import admin

from .models import MoneyRequest, Wallet


class MoneyRequestAdmin(admin.ModelAdmin):
    list_filter = ("money_request_status",)


admin.site.register(Wallet)
admin.site.register(MoneyRequest, MoneyRequestAdmin)
