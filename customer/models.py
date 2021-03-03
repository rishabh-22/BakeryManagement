from django.core.validators import RegexValidator
from django.db import models

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


class Customer(models.Model):
    name = models.CharField(max_length=75, null=False)
    age = models.IntegerField(null=False)
    number = models.CharField(validators=[RegexValidator(regex=r'^[6-9]\d{9}$',
                                                         message='invalid mobile number!', code='nomatch')])
    address = models.TextField(null=False)  # provision for only one address as of now


class Orders(models.Model):
    buyer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='IP')
    total_amount = models.IntegerField(null=False)
    is_cancelled = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES, null=False)
    shipping_address = models.CharField(max_length=100, blank=True, null=False)
    transaction_id = models.CharField(max_length=256, unique=True)
