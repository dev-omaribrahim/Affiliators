import re

from django.core.exceptions import ValidationError


def validate_mobile_number(value):
    pattern = re.compile("(0)?[1][0-9]{9}")
    valid_number = pattern.match(value)
    if not valid_number:
        raise ValidationError("Enter a valid number")
    else:
        return valid_number


def validate_id_number(value):
    pattern = re.compile("[0-9]{14}")
    valid_number = pattern.match(value)
    if not valid_number:
        raise ValidationError("Enter a valid number")
    else:
        return valid_number
