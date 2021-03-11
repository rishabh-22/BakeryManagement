from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from admins.models import Items

PAYMENT_CHOICES = (
    ('COD', 'COD'),
    ('Card', 'Card'),
    ('UPI', 'UPI'),
    ('Wallet', 'Wallet'),
)

ORDER_STATUS = (
    ('IP', 'In Processing'),
    ('OH', 'On Hold'),
    ('C', 'Cancelled'),
    ('OFD', 'Out For Delivery'),
    ('R', 'Returned'),
    ('D', 'Delivered'),
)


class Customer(User):
    age = models.IntegerField(null=False)
    number = models.CharField(max_length=10, validators=[RegexValidator(regex=r'^[6-9]\d{9}$',
                                                         message='invalid mobile number!', code='nomatch')])
    address = models.TextField(null=False)  # provision for only one address as of now

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Customers"


class Orders(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='IP')
    quantity = models.IntegerField(null=False, default=1)
    total_amount = models.IntegerField(null=False)
    is_cancelled = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES, null=False)
    shipping_address = models.CharField(max_length=100, blank=True, null=False)
    transaction_id = models.CharField(max_length=256, unique=True)

    class Meta:
        verbose_name_plural = "Orders"


@receiver(post_save, sender=Customer)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
