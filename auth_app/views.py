from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse

from wallet_app.models import Wallet

from .forms import SignIn, SignUp


def sign_up(request):
    if request.user.is_authenticated:
        return redirect(reverse("product:product_list"))
    else:
        if request.method == "POST":
            signup_form = SignUp(request.POST)
            if signup_form.is_valid():
                cd = signup_form.cleaned_data
                new_user = signup_form.save(commit=False)
                new_user.set_password(cd["password1"])
                # new_user.is_active = False
                new_user.save()
                Wallet.objects.create(marketer=new_user)
                return redirect(reverse("account_under_review"))
                # return render(request, 'auth_app/landing_page.html', {})
        else:
            signup_form = SignUp()
        context = {"signup_form": signup_form}
        return render(request, "auth_app/signup.html", context)


def sign_in(request):
    if request.user.is_authenticated:
        return redirect(reverse("product:product_list"))
    else:
        error = ""
        if request.method == "POST":
            signin_form = SignIn(request.POST)
            if signin_form.is_valid():
                cd = signin_form.cleaned_data
                user = authenticate(
                    request, username=cd["username"], password=cd["password"]
                )
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        # return HttpResponse("Login Successfully")
                        return redirect(reverse("product:product_list"))
                    else:
                        # return HttpResponse("Disabled Account")
                        error = "Disabled Account, your account in review"
                else:
                    # return HttpResponse("Invalid Account")
                    error = "Invalid Account"
        else:
            signin_form = SignIn()

        context = {"signin_form": signin_form, "error": error}
        return render(request, "auth_app/signin.html", context)
        # return redirect(reverse("product:product_list"))


def sign_out(request):
    # Change the GET method to POST later when add logout button
    logout(request)
    return redirect(reverse("sign_in"))


def landing_page(request):
    if request.user.is_authenticated:
        return redirect(reverse("product:product_list"))
    return render(request, "auth_app/landing_page.html", {})


def account_under_review(request):
    return render(request, "auth_app/account_under_review.html", {})
