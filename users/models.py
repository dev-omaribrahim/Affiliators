from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.crypto import get_random_string

# from .validators import validate_mobile_number, validate_id_number
from custome_utils.my_validators import validate_id_number, validate_mobile_number

from . import choices


class User(AbstractUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        null=True,
        blank=False,
    )

    user_role = models.CharField(
        max_length=20, choices=choices.USER_ROLE_CHOICES, default=choices.MARKETER
    )

    def __str__(self):
        return self.get_full_name()


class Marketer(User):
    mobile_number = models.CharField(
        max_length=11,
        validators=[validate_mobile_number],
        null=True,
        blank=False,
        unique=True,
    )

    money_receive_number = models.CharField(
        max_length=11,
        validators=[validate_mobile_number],
        null=True,
        blank=True,
        unique=True,
    )

    id_number = models.CharField(
        max_length=14,
        validators=[validate_id_number],
        null=True,
        blank=False,
        unique=True,
    )

    marketer_code = models.CharField(max_length=20, blank=True, null=True)

    gender = models.CharField(
        choices=choices.GENDER_CHOICES,
        default=choices.MALE,
        max_length=6,
        null=True,
        blank=False,
    )

    age = models.PositiveIntegerField(
        validators=[MinValueValidator(15), MaxValueValidator(60)],
        null=True,
        blank=False,
    )

    address = models.CharField(max_length=255, blank=True, null=True)

    # is_merchant = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Marketer"
        verbose_name_plural = "Marketers"

    def save(self, *args, **kwargs):
        marketer_code = self.marketer_code
        chars = "abcdefghijklmnopqrstuvwxyz123456789".upper()

        if not marketer_code:
            marketer_code = get_random_string(length=5, allowed_chars=chars)

        while (
            Marketer.objects.filter(marketer_code=marketer_code)
            .exclude(pk=self.pk)
            .exists()
        ):
            marketer_code = get_random_string(length=5, allowed_chars=chars)

        self.marketer_code = marketer_code
        super(Marketer, self).save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()


class Merchant(User):
    # is_merchant = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Merchant"
        verbose_name_plural = "Merchants"

    def __str__(self):
        return self.get_full_name()
