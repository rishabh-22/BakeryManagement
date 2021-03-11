from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


class Ingredients(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False)
    quantity = models.CharField(max_length=50, null=False)  # char field to store metric as well
    price = models.FloatField(null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Ingredients"


class Items(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False)
    quantity = models.IntegerField(null=False)
    cost_price = models.FloatField(null=False)
    sell_price = models.FloatField(null=False)
    mfg_date = models.DateField(null=False)
    expiry_date = models.DateField(null=False)
    ingredients = models.TextField(null=False)  # psql array/json field to be used ideally

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Items"


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
