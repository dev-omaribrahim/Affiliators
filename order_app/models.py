from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.crypto import get_random_string

from product.models import Product, SizeAmount
from users.models import Marketer
from users.validators import validate_mobile_number
from wallet_app.models import Wallet

from . import choices


class Order(models.Model):
    order_status = models.CharField(
        choices=choices.ORDER_STATUS_CHOICES,
        max_length=20,
        default=choices.UNDER_REVIEW,
    )

    order_code = models.CharField(max_length=100, blank=True, null=True)

    order_marketer = models.ForeignKey(
        Marketer,
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    order_client_name = models.CharField(max_length=100, null=True, blank=False)

    order_client_number = models.CharField(
        validators=[validate_mobile_number], max_length=11, null=True, blank=False
    )

    order_client_number2 = models.CharField(
        validators=[validate_mobile_number], max_length=11, null=True, blank=True
    )

    order_client_city = models.CharField(max_length=100, null=True, blank=False)

    order_client_area = models.CharField(max_length=255, null=True, blank=False)

    order_client_address = models.CharField(max_length=255, null=True, blank=False)

    order_delivering_price = models.DecimalField(
        max_digits=4, decimal_places=1, blank=True, null=True
    )

    order_notes = models.TextField(blank=True, null=True)

    order_total_price = models.DecimalField(
        max_digits=4, decimal_places=0, blank=True, null=True
    )

    order_total_commission = models.DecimalField(
        max_digits=4, decimal_places=0, blank=True, null=True
    )

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    updated = models.DateTimeField(auto_now=True)

    order_confirmed = models.BooleanField(default=False)

    calculated = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def clean(self):

        if not self.order_confirmed:
            for product in self.products.all():
                try:
                    stock_product = Product.objects.get(
                        product_code=product.product_code
                    )

                    try:
                        stock_product_size_amount = SizeAmount.objects.get(
                            product=stock_product, size=product.product_size
                        )
                        if stock_product_size_amount.amount < product.product_quantity:
                            raise ValidationError(
                                "Our Stock Doesn't Have this quantity of product : {}, size: {}".format(
                                    product.product_name, product.product_size
                                )
                            )

                    except SizeAmount.DoesNotExist:
                        stock_product_size_amount = SizeAmount.objects.get(
                            product=stock_product
                        )
                        if stock_product_size_amount.amount < product.product_quantity:
                            raise ValidationError(
                                "Our Stock Doesn't Have this quantity of product : {}, size: {}".format(
                                    product.product_name, product.product_size
                                )
                            )

                except Product.DoesNotExist:
                    pass
                    # raise ValidationError("Not Found")

        if (
            self.order_status == choices.PAID or self.order_status == choices.RETURNED
        ) and not self.order_confirmed:
            raise ValidationError({"order_status": "Order must bo confirmed first"})

    def save(self, *args, **kwargs):
        order_code = self.order_code
        chars = "abcdefghijklmnopqrstuvwxyz123456789".upper()

        if not order_code:
            order_code = get_random_string(length=5, allowed_chars=chars)

        while Order.objects.filter(order_code=order_code).exclude(pk=self.pk).exists():
            order_code = get_random_string(length=5, allowed_chars=chars)

        self.order_code = order_code

        if not self.calculated:
            # add order commission to marketer potential commission
            if self.order_status == choices.CONFIRMED:
                wallet = Wallet.objects.get(marketer=self.order_marketer)
                commission = self.order_total_commission
                wallet.wallet_potential_commission += commission
                wallet.save()
                self.order_confirmed = True
                self.calculated = True

                # remove ordered products quantity from product stock quantity
                for product in self.products.all():
                    try:
                        stock_product = Product.objects.get(
                            product_code=product.product_code
                        )

                        try:
                            stock_product_size_amount = SizeAmount.objects.get(
                                product=stock_product, size=product.product_size
                            )
                            stock_product_size_amount.amount -= product.product_quantity
                            stock_product_size_amount.save()

                        except SizeAmount.DoesNotExist:
                            stock_product_size_amount = SizeAmount.objects.get(
                                product=stock_product
                            )
                            stock_product_size_amount.amount -= product.product_quantity
                            stock_product_size_amount.save()

                    except Product.DoesNotExist:
                        pass

            # remove order commission from marketer potential commission
            if self.order_status == choices.RETURNED:
                wallet = Wallet.objects.get(marketer=self.order_marketer)
                commission = self.order_total_commission
                wallet.wallet_potential_commission -= commission
                wallet.save()
                self.calculated = True

                # add ordered products quantity from product stock quantity
                for product in self.products.all():
                    try:
                        stock_product = Product.objects.get(
                            product_code=product.product_code
                        )

                        try:
                            stock_product_size_amount = SizeAmount.objects.get(
                                product=stock_product, size=product.product_size
                            )
                            stock_product_size_amount.amount += product.product_quantity
                            stock_product_size_amount.save()

                        except SizeAmount.DoesNotExist:
                            stock_product_size_amount = SizeAmount.objects.get(
                                product=stock_product
                            )
                            stock_product_size_amount.amount += product.product_quantity
                            stock_product_size_amount.save()
                    except Product.DoesNotExist:
                        pass

            # move order commission from potential commission to sure commission
            if self.order_status == choices.PAID:
                wallet = Wallet.objects.get(marketer=self.order_marketer)
                commission = self.order_total_commission
                wallet.wallet_potential_commission -= commission
                wallet.wallet_total_commission += commission
                wallet.save()
                self.calculated = True

        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        # return self.order_client_name or " "
        return "order from {} to {}".format(self.order_marketer, self.order_client_name)


class OrderProduct(models.Model):

    product_order = models.ForeignKey(
        Order, related_name="products", on_delete=models.CASCADE, default=1
    )

    product_name = models.CharField(max_length=255, blank=True, null=True)

    product_code = models.CharField(max_length=50, blank=True, null=True)

    product_price = models.DecimalField(
        max_digits=4, decimal_places=0, blank=True, null=True
    )

    product_commission = models.DecimalField(
        max_digits=4, decimal_places=0, blank=True, null=True
    )

    product_image = models.ImageField(
        blank=True, null=True, default="default_product_image.jpg"
    )

    product_size = models.CharField(max_length=6, blank=True, null=True)

    product_quantity = models.PositiveIntegerField(blank=True, null=True)

    product_total_price = models.DecimalField(
        max_digits=4, decimal_places=0, blank=True, null=True
    )

    product_total_commission = models.DecimalField(
        max_digits=4, decimal_places=0, blank=True, null=True
    )

    def __str__(self):
        return self.product_name


class CitiesDeliver(models.Model):
    city_name = models.CharField(max_length=255, null=True, blank=False)

    city_delivery_price = models.DecimalField(
        max_digits=4, decimal_places=0, null=True, blank=False
    )

    def __str__(self):
        return self.city_name
