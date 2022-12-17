from django import forms

from .choices import PRODUCT_QUANTITY_CHOICES


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)

    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
