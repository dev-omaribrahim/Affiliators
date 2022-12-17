from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string

from users.models import Merchant


class Package(models.Model):
    package_name = models.CharField(max_length=255, null=True, blank=False)
    package_image = models.ImageField(
        null=True, blank=False, default="default_product_image.jpg"
    )
    package_category = models.ForeignKey(
        "Category",
        related_name="packages",
        on_delete=models.PROTECT,
        null=True,
        blank=False,
    )

    class Meta:
        verbose_name = "Package"
        verbose_name_plural = "Packages"

    def get_absolute_url(self):
        return reverse("product:product_details", kwargs={"pk": self.pk})

    def get_package_info(self):
        package_info_dic = {
            "price": [],
            "commission": [],
            "colors": [],
            "sizes": [],
            "stock": [],
        }
        for product in self.products.all():
            package_info_dic["price"].append(str(product.product_price))
            package_info_dic["commission"].append(str(product.product_commission))
            package_info_dic["colors"].append(product.product_color)
            package_info_dic["sizes"] += [
                size.size for size in product.size_amount.all()
            ]
            package_info_dic["stock"] += [
                size.amount for size in product.size_amount.all()
            ]

        package_info_dic["price"] = list(set(package_info_dic["price"]))
        package_info_dic["commission"] = list(set(package_info_dic["commission"]))
        package_info_dic["colors"] = list(set(package_info_dic["colors"]))
        package_info_dic["sizes"] = list(set(package_info_dic["sizes"]))
        package_info_dic["stock"] = sum(package_info_dic["stock"])

        return package_info_dic

    def __str__(self):
        return self.package_name


class Product(models.Model):
    product_merchant = models.ForeignKey(
        Merchant,
        related_name="products",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    product_name = models.CharField(max_length=255, null=True, blank=False)
    product_code = models.CharField(max_length=50, blank=True, null=True)
    product_price = models.DecimalField(
        max_digits=4, decimal_places=0, null=True, blank=False
    )
    product_commission = models.DecimalField(
        max_digits=4, decimal_places=0, null=True, blank=False
    )
    product_color = models.CharField(max_length=50, blank=True, null=True)
    product_image = models.ImageField(
        null=True, blank=False, default="default_product_image.jpg"
    )
    product_description = models.TextField(null=True, blank=False)
    product_session_url = models.URLField(max_length=250, null=True, blank=False)

    product_package = models.ForeignKey(
        Package,
        related_name="products",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):

        product_code = self.product_code

        chars = "abcdefghijklmnopqrstuvwxyz123456789".upper()

        if not product_code:
            product_code = get_random_string(length=5, allowed_chars=chars)

        while (
            Product.objects.filter(product_code=product_code)
            .exclude(pk=self.pk)
            .exists()
        ):
            product_code = get_random_string(length=5, allowed_chars=chars)

        self.product_code = product_code
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name


class SizeAmount(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="size_amount",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    size = models.CharField(max_length=6, null=True, blank=True)
    amount = models.PositiveIntegerField(null=True, blank=False)
    amount_is_empty = models.BooleanField(default=False)
    amount_renewable = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Size and Amount"
        verbose_name_plural = "Sizes and Amounts"

    def save(self, *args, **kwargs):
        if self.amount < 1:
            self.amount_is_empty = True
        else:
            self.amount_is_empty = False
        super(SizeAmount, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.product_name


class Category(models.Model):
    category_name = models.CharField(max_length=100, null=True, blank=False)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse(
            "product:product_category", kwargs={"category": self.category_name}
        )

    def __str__(self):
        return self.category_name
