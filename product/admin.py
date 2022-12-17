from django.contrib import admin

from .models import Category, Package, Product, SizeAmount

# class ProductsInline(admin.StackedInline):
#     model = Product
#
#
# class PackageAdmin(admin.ModelAdmin):
#     list_display = ('package_name', 'products')
#     inlines = [ProductsInline]
#
#     def products(self, obj):
#         products = []
#         for product in obj.products.all():
#             products.append(product.product_name)
#         return products


class SizeAmountInline(admin.TabularInline):
    model = SizeAmount
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [SizeAmountInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Package)
admin.site.register(SizeAmount)
admin.site.register(Category)
