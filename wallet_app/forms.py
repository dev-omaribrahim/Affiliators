from django import forms

from users.models import Marketer

from .models import MoneyRequest


class MoneyRequestForm(forms.ModelForm):
    # password = forms.CharField(
    #     label="Password", max_length=255, widget=forms.PasswordInput
    # )

    class Meta:
        model = MoneyRequest
        fields = (
            "money_receive_number",
            "id_number",
        )

    def __init__(self, username, *args, **kwargs):
        self.username = username
        try:
            self.marketer = Marketer.objects.get(username=username)
        except Marketer.DoesNotExist:
            self.marketer = None
        super(MoneyRequestForm, self).__init__(*args, **kwargs)

    def clean_id_number(self):
        id_number = self.cleaned_data["id_number"]
        if self.marketer:
            if id_number != self.marketer.id_number:
                raise forms.ValidationError("Enter your registered id number")
        return id_number

    # def clean_money_amount(self):
    #     money_amount = self.cleaned_data['money_amount']
    #     marketer_earned_money = self.marketer.wallet.wallet_total_commission
    #
    #     if marketer_earned_money < 100:
    #         raise forms.ValidationError("you must earn at least 100 L.E")
    #
    #     if marketer_earned_money < money_amount:
    #         raise forms.ValidationError("you don't have that amount")

    # def clean_password(self):
    #     password = self.cleaned_data['password']
    #     if not self.marketer.check_password(password):
    #         raise forms.ValidationError("Enter a Correct Password!")
