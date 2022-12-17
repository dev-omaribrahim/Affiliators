from decimal import Decimal

from django.conf import settings

from product.models import Product


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, size="none", quantity=1):
        product_id = str(product.id)

        # new
        product_id = product_id + " " + size

        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": quantity,
                "size": size,
                "price": str(product.product_price),
                "commission": str(product.product_commission),
            }

        # if self.cart[product_id]['size'] != size:
        #     self.cart[product_id]['size'] = size

        self.cart[product_id]["quantity"] = quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        # product_id = str(product.id)
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):

        # product_ids = self.cart.keys()

        # products ids + sizes
        old_product_ids = self.cart.keys()

        # products ids only to query it
        product_ids = []

        for product_id in old_product_ids:
            x = product_id.split()[0]
            product_ids.append(x)

        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        # for product in products:
        #     cart[str(product.id)]['product'] = product

        for old_key in old_product_ids:
            new_key = old_key.split()[0]
            for product in products:
                if new_key == str(product.id):
                    cart[old_key]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["commission"] = Decimal(item["commission"])
            item["total_commission"] = item["commission"] * item["quantity"]
            item["total_price"] = item["price"] * item["quantity"]

            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def get_total_commission(self):
        return sum(
            Decimal(item["commission"]) * item["quantity"]
            for item in self.cart.values()
        )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
