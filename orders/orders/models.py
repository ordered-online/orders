from django.db import models

from sessions.models import Session


class Order(models.Model):

    # mandatory fields
    product_id = models.IntegerField()
    # note that the price could also be inferred by the product,
    # but we want a fixed price on purchase, independent from the
    # price of the product itself
    price = models.DecimalField(max_digits=10, decimal_places=2)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=["session"])
        ]
