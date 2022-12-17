from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render, reverse

from custome_utils.decorators import marketer_role_check, merchant_role_check
from users.models import Marketer

from . import choices
from .forms import MoneyRequestForm
from .models import MoneyRequest, Wallet


@login_required
@user_passes_test(
    marketer_role_check,
    login_url=settings.MERCHANT_PRODUCTS_URL,
    redirect_field_name=None,
)
def wallet_details(request):
    try:
        marketer = Marketer.objects.get(username=request.user.username)
        marketer_wallet = marketer.wallet
        if (
            marketer_wallet.wallet_potential_commission > 0
            or marketer_wallet.wallet_total_commission > 0
        ):
            money_in_wallet = marketer_wallet
        else:
            money_in_wallet = None
    except Marketer.DoesNotExist:
        money_in_wallet = None

    context = {"money_in_wallet": money_in_wallet}
    return render(request, "wallet_app/my_wallet.html", context)


@login_required
@user_passes_test(
    marketer_role_check,
    login_url=settings.MERCHANT_PRODUCTS_URL,
    redirect_field_name=None,
)
def request_money(request):
    marketer = get_object_or_404(Marketer, username=request.user.username)
    if request.method == "POST":
        form = MoneyRequestForm(marketer.username, request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.marketer = marketer
            new_request.save()
            return redirect(reverse("wallet_app:current_money_requests"))
    else:
        form = MoneyRequestForm(username=request.user.username)
    context = {"form": form}
    return render(request, "wallet_app/request_money.html", context)


@login_required
@user_passes_test(
    marketer_role_check,
    login_url=settings.MERCHANT_PRODUCTS_URL,
    redirect_field_name=None,
)
def request_money_history(request):
    marketer = get_object_or_404(Marketer, username=request.user.username)
    request_history = MoneyRequest.objects.filter(
        marketer=marketer, money_request_status=choices.MONEY_SENT
    )
    if not request_history:
        request_history = None

    context = {"request_history": request_history}
    return render(request, "wallet_app/request_history.html", context)


@login_required
@user_passes_test(
    marketer_role_check,
    login_url=settings.MERCHANT_PRODUCTS_URL,
    redirect_field_name=None,
)
def current_money_requests(request):
    marketer = get_object_or_404(Marketer, username=request.user.username)
    current_requests = MoneyRequest.objects.filter(
        marketer=marketer, money_request_status=choices.UNDER_REVIEW
    )
    if not current_requests:
        current_requests = None

    context = {"current_requests": current_requests}
    return render(request, "wallet_app/current_requests.html", context)
