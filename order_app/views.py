from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render, reverse

from cart_app.cart import Cart
from custome_utils.decorators import (
    ajax_required,
    marketer_role_check,
    merchant_role_check,
    ownership_required,
)
from users.models import Marketer

from . import choices
from .forms import OrderClientInfoForm
from .models import CitiesDeliver, Order, OrderProduct


@login_required
@user_passes_test(
    marketer_role_check,
    login_url=settings.MERCHANT_PRODUCTS_URL,
    redirect_field_name=None,
)
def order_client_info(request):
    cart = Cart(request)

    if request.method == "POST":
        form = OrderClientInfoForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            marketer = get_object_or_404(Marketer, username=request.user.username)
            # delivery_city_obj = CitiesDeliver.objects.get(city_name=cd['order_client_city'])
            delivery_city_obj = get_object_or_404(
                CitiesDeliver, city_name=cd["order_client_city"]
            )
            delivery_price = delivery_city_obj.city_delivery_price
            # cart_price = cart.get_total_price()
            # final_price = delivery_price + cart_price

            new_order = Order.objects.create(
                order_marketer=marketer,
                order_client_name=cd["order_client_name"],
                order_client_number=cd["order_client_number"],
                order_client_number2=cd["order_client_number2"],
                order_client_city=cd["order_client_city"],
                order_client_area=cd["order_client_area"],
                order_client_address=cd["order_client_address"],
                order_delivering_price=delivery_price,
                order_notes=cd["order_notes"],
                order_total_commission=cart.get_total_commission(),
                order_total_price=cart.get_total_price()
                # order_total_price=final_price
            )

            for item in cart:
                OrderProduct.objects.create(
                    product_order=new_order,
                    product_name=item["product"].product_name,
                    product_code=item["product"].product_code,
                    product_price=item["product"].product_price,
                    product_commission=item["product"].product_commission,
                    product_image=item["product"].product_image,
                    product_size=item["size"],
                    product_quantity=item["quantity"],
                    product_total_price=item["total_price"],
                    product_total_commission=item["total_commission"],
                )
            cart.clear()
            return redirect(reverse("order_app:thank_you"))
    else:
        form = OrderClientInfoForm()

    context = {"form": form}
    return render(request, "order_app/client_info_form.html", context)


@login_required
@user_passes_test(
    marketer_role_check,
    login_url=settings.MERCHANT_PRODUCTS_URL,
    redirect_field_name=None,
)
def orders_dashboard(request):
    try:
        marketer = Marketer.objects.get(username=request.user.username)
        orders = Order.objects.filter(
            order_marketer=marketer, order_status=choices.UNDER_REVIEW
        )
    except Marketer.DoesNotExist:
        orders = None

    context = {"orders": orders}
    return render(request, "order_app/orders_dashboard.html", context)


@login_required
@user_passes_test(
    marketer_role_check,
    login_url=settings.MERCHANT_PRODUCTS_URL,
    redirect_field_name=None,
)
@ownership_required
def order_details(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        order = None
        return HttpResponse("no")
    context = {"order": order}
    return render(request, "order_app/order_details.html", context)


@login_required
@user_passes_test(
    marketer_role_check,
    login_url=settings.MERCHANT_PRODUCTS_URL,
    redirect_field_name=None,
)
def orders_history(request, status=None):
    try:
        marketer = Marketer.objects.get(username=request.user.username)
        orders = Order.objects.filter(order_marketer=marketer).exclude(
            order_status=choices.UNDER_REVIEW
        )
        if status:
            orders = Order.objects.filter(order_marketer=marketer, order_status=status)
    except Marketer.DoesNotExist:
        orders = None
        marketer = None

    orders_status = {
        choices.REFUSED: Order.objects.filter(
            order_marketer=marketer, order_status=choices.REFUSED
        ).count(),
        choices.RETURNED: Order.objects.filter(
            order_marketer=marketer, order_status=choices.RETURNED
        ).count(),
        choices.PAID: Order.objects.filter(
            order_marketer=marketer, order_status=choices.PAID
        ).count(),
    }

    context = {"orders": orders, "orders_status": orders_status}
    return render(request, "order_app/orders_history.html", context)


@login_required
@user_passes_test(
    marketer_role_check,
    login_url=settings.MERCHANT_PRODUCTS_URL,
    redirect_field_name=None,
)
@ownership_required
def remove_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect(reverse("order_app:orders_dashboard"))


@login_required
@user_passes_test(
    marketer_role_check,
    login_url=settings.MERCHANT_PRODUCTS_URL,
    redirect_field_name=None,
)
@ownership_required
def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.order_status == choices.UNDER_REVIEW:
        initial_dict = {"order_client_city": order.order_client_city}
        if request.method == "POST":
            form = OrderClientInfoForm(
                request.POST, instance=order, initial=initial_dict
            )
            if form.is_valid():
                cd = form.cleaned_data
                delivery_city_obj = get_object_or_404(
                    CitiesDeliver, city_name=cd["order_client_city"]
                )
                delivery_price = delivery_city_obj.city_delivery_price
                edited_order = form.save(commit=False)
                edited_order.order_client_city = cd["order_client_city"]
                edited_order.order_delivering_price = delivery_price
                edited_order.save()
                return redirect(reverse("order_app:thank_you"))
        else:
            form = OrderClientInfoForm(instance=order, initial=initial_dict)
    else:
        return redirect(reverse("order_app:orders_dashboard"))

    context = {"form": form, "order_status": order.order_status}
    return render(request, "order_app/edit_client_information.html", context)


@login_required
@user_passes_test(
    marketer_role_check,
    login_url=settings.MERCHANT_PRODUCTS_URL,
    redirect_field_name=None,
)
def thank_you(request):
    return render(request, "order_app/thank_you.html", {})


@login_required
@user_passes_test(
    marketer_role_check,
    login_url=settings.MERCHANT_PRODUCTS_URL,
    redirect_field_name=None,
)
def delivery_price(request):
    cities = CitiesDeliver.objects.all()
    context = {"cities": cities}
    return render(request, "order_app/delivery_price.html", context)
