from django.db import models

from custome_utils.my_validators import validate_id_number, validate_mobile_number
from users.models import Marketer

from . import choices


class Wallet(models.Model):
    marketer = models.OneToOneField(Marketer, on_delete=models.CASCADE)

    wallet_potential_commission = models.DecimalField(
        max_digits=4, decimal_places=0, blank=True, null=True, default=0
    )

    wallet_total_commission = models.DecimalField(
        max_digits=4, decimal_places=0, blank=True, null=True, default=0
    )

    def __str__(self):
        return "Wallet of {}".format(self.marketer)


class MoneyRequest(models.Model):
    marketer = models.ForeignKey(
        Marketer, related_name="money_requests", on_delete=models.CASCADE
    )

    money_request_status = models.CharField(
        max_length=100,
        choices=choices.MONEY_REQUEST_STATUS,
        default=choices.UNDER_REVIEW,
    )

    money_receive_number = models.CharField(
        max_length=11, validators=[validate_mobile_number], null=True, blank=False
    )

    id_number = models.CharField(
        max_length=14, validators=[validate_id_number], null=True, blank=False
    )

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return "{} ::: Requsted his Money".format(self.marketer.get_full_name())
