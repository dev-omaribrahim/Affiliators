from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from wallet_app.models import Wallet

from .models import Marketer, Merchant, User

# UserAdmin.list_display += ('user_role',)
# UserAdmin.list_filter += ('user_role',)
# UserAdmin.fieldsets += (
#             ('Extra Fields', {'fields': ('user_role',)}),
#     )
# UserAdmin.fieldsets += ((User, {'fields': ("user_role",)}),)


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = UserAdmin.list_display + ("user_role",)
    list_filter = UserAdmin.list_filter + ("user_role",)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("User",),
                "fields": ("username", "email", "password1", "password2", "user_role"),
            },
        ),
    )


class CustomMerchantAdmin(UserAdmin):
    model = User
    list_display = UserAdmin.list_display + ("user_role",)
    list_filter = UserAdmin.list_filter + ("user_role",)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("Merchant",),
                "fields": ("username", "password1", "password2", "user_role"),
            },
        ),
    )


# Not Used
# class CustomMarketerAdmin(UserAdmin):
#     model = User
#     list_display = UserAdmin.list_display + ('user_role',)
#     list_filter = UserAdmin.list_filter + ('user_role',)
#     add_fieldsets = (
#         (None, {
#             'classes': ('Marketer',),
#             'fields': (
#                 'username', 'password1', 'password2', 'email', 'user_role',
#                 'mobile_number', 'money_receive_number', 'id_number',
#                 'marketer_code', 'gender', 'age', 'address',
#             )}
#          ),
#     )


class WalletInline(admin.StackedInline):
    model = Wallet
    extra = 0


class MarketerAdmin(admin.ModelAdmin):
    inlines = [WalletInline]
    list_filter = ("is_active",)
    search_fields = ("marketer_code", "id_number", "email", "username")


admin.site.register(User, CustomUserAdmin)
# admin.site.register(Marketer, CustomMarketerAdmin)
admin.site.register(Marketer, MarketerAdmin)
admin.site.register(Merchant, CustomMerchantAdmin)
