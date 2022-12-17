from django import forms

from users.models import Marketer, User


class SignUp(forms.ModelForm):
    password1 = forms.CharField(
        label="Password", max_length=255, widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Repeat Password", max_length=255, widget=forms.PasswordInput
    )

    class Meta:
        model = Marketer
        fields = (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "username",
            "mobile_number",
            "id_number",
            "gender",
            "age",
            "address",
        )

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1 != password2:
            raise forms.ValidationError("passwords don't match")
        return password2


class SignIn(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        label="Password", max_length=255, widget=forms.PasswordInput
    )
