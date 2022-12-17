from django.http import HttpResponse, HttpResponseBadRequest

from order_app.models import Order
from users.models import Marketer


def marketer_role_check(user):
    if user.user_role == "Marketer":
        return True
    else:
        return False


def merchant_role_check(user):
    if user.user_role == "Merchant":
        return True
    else:
        return False


def ajax_required(f):
    def wrap(request, *args, **kwargs):

        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap


def ownership_required(f):
    def wrap(request, *args, **kwargs):
        pk = kwargs["pk"]
        try:
            marketer = Marketer.objects.get(username=request.user.username)
            order = Order.objects.get(pk=pk)
            if not marketer.pk == order.order_marketer.pk:
                return HttpResponseBadRequest()

        except Marketer.DoesNotExist or Order.DoesNotExist:
            return HttpResponseBadRequest()

        except Order.DoesNotExist:
            return HttpResponseBadRequest()

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap
