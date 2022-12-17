from django import forms

from .models import CitiesDeliver, Order


class OrderClientInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderClientInfoForm, self).__init__(*args, **kwargs)

        self.fields["order_client_city"] = forms.ChoiceField(
            choices=[("", "Select City")]
            + [
                (str(city.city_name), city.city_name)
                for city in CitiesDeliver.objects.all()
            ]
        )

    class Meta:
        model = Order
        fields = (
            "order_client_name",
            "order_client_number",
            "order_client_number2",
            "order_client_area",
            "order_client_address",
            "order_notes",
        )
