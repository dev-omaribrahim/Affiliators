from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.shortcuts import render

from custome_utils.decorators import marketer_role_check, merchant_role_check
from users.models import Merchant

from .models import Category, Package, Product


@login_required
@user_passes_test(
    marketer_role_check,
    login_url=settings.MERCHANT_PRODUCTS_URL,
    redirect_field_name=None,
)
def package_list(request, category=None):
    if category:
        packages = Package.objects.filter(package_category__category_name=category)
        # if not packages:
        #     return render(request, 'product/empty_home.html')
    else:
        packages = Package.objects.all()

    categories = Category.objects.all()

    if not packages:
        return render(request, "product/empty_home.html", {"categories": categories})

    paginator = Paginator(packages, 9)
    page = request.GET.get("page", 1)

    try:
        packages = paginator.page(page)
    except PageNotAnInteger:
        packages = paginator.page(1)
    except EmptyPage:
        packages = paginator.page(paginator.num_pages)

    context = {"packages": packages, "categories": categories}
    return render(request, "product/home.html", context)


@login_required
@user_passes_test(
    marketer_role_check,
    login_url=settings.MERCHANT_PRODUCTS_URL,
    redirect_field_name=None,
)
def package_details(request, pk):
    try:
        package = Package.objects.get(pk=pk)
        products = (
            Product.objects.filter(product_package=package)
            .annotate(num_amount=Count("size_amount"))
            .exclude(num_amount__lte=1, size_amount__amount_is_empty=True)
        )
        if not products:
            categories = Category.objects.all()
            context = {"categories": categories}
            return render(request, "product/empty_home.html", context)

    except Package.DoesNotExist:
        products = None

    context = {"products": products}
    return render(request, "product/package_details.html", context)


@login_required
@user_passes_test(
    merchant_role_check, login_url=settings.HOME_URL, redirect_field_name=None
)
def merchant_products(request):
    username = request.user.username
    try:
        merchant = Merchant.objects.get(username=username)
        products = Product.objects.filter(product_merchant=merchant)
        # products = Product.objects.all()
    except Merchant.DoesNotExist:
        products = None

    context = {"products": products}
    return render(request, "product/merchant_products.html", context)
