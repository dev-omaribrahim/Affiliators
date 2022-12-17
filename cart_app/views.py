from decimal import Decimal

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from custome_utils.decorators import (
    ajax_required,
    marketer_role_check,
    merchant_role_check,
)
from product.models import Product

from .cart import Cart
from .forms import CartAddProductForm


@login_required
@user_passes_test(
    marketer_role_check,
    login_url=settings.MERCHANT_PRODUCTS_URL,
    redirect_field_name=None,
)
def cart_detail(request):
    cart = Cart(request)
    # cart.clear()

    context = {"cart": cart}
    # return render(request, 'cart_app/cart_test.html', context)
    return render(request, "cart_app/cart_detail.html", context)


@ajax_required
@user_passes_test(
    marketer_role_check,
    login_url=settings.MERCHANT_PRODUCTS_URL,
    redirect_field_name=None,
)
def cart_add(request):
    cart = Cart(request)

    product_id = request.POST.get("product_id")
    product_quantity = request.POST.get("quantity")
    product_quantity = int(product_quantity)
    product_size = request.POST.get("size")

    # print(product_size)

    product = get_object_or_404(Product, id=product_id)

    if product_size:
        cart.add(product=product, quantity=product_quantity, size=product_size)
    else:
        cart.add(product=product, quantity=product_quantity)

    data = {"length": cart.__len__()}
    return JsonResponse(data, safe=False)


@login_required
@user_passes_test(
    marketer_role_check,
    login_url=settings.MERCHANT_PRODUCTS_URL,
    redirect_field_name=None,
)
def cart_remove(request, product_id, size):
    cart = Cart(request)
    id_product = str(product_id) + " " + str(size)
    cart.remove(id_product)
    return redirect("cart_app:cart_detail")


# not used
@ajax_required
@user_passes_test(
    marketer_role_check,
    login_url=settings.MERCHANT_PRODUCTS_URL,
    redirect_field_name=None,
)
def cart_detail_ajax(request):
    cart = Cart(request)
    product_ids = []
    product_info = []

    for item in cart:
        product = item["product"]
        # cart_dict[product.id]["quantity"] = item["quantity"]
        # product_ids.append(product.id)
        product_ids.append(str(product.id) + item["size"])
        product_info.append(
            {
                "quantity": item["quantity"],
                "total_price": item["total_price"],
                "total_cart_price": cart.get_total_price(),
            }
        )

    cart_dict = dict(zip(product_ids, product_info))

    return JsonResponse(cart_dict, safe=False)
