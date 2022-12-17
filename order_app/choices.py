UNDER_REVIEW = "under review"
REFUSED = "refused"
CONFIRMED = "confirmed"
ON_THE_WAY = "in his way"
RETURNED = "returned"
PAID = "paid"


ORDER_STATUS_CHOICES = (
    (UNDER_REVIEW, "under review"),
    (REFUSED, "refused"),
    (CONFIRMED, "confirmed"),
    (ON_THE_WAY, "on the way"),
    (RETURNED, "returned"),
    (PAID, "paid"),
)


ALEXANDRIA = "alexandria"
CAIRO = "cairo"

CITIES_DELIVERY_CHOICES = (
    (ALEXANDRIA, "Alexandria"),
    (CAIRO, "Cairo"),
)
