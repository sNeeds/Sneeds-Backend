from django.contrib.auth import get_user_model
from django.db import models

from abroadin.apps.store.carts.models import Cart
from abroadin.apps.users.consultants.models import ConsultantProfile

User = get_user_model()


class PayPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    authority = models.CharField(max_length=1024)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


