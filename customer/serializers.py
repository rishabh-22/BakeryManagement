from customer.models import Customer

from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['username', 'password', 'age', 'number', 'address']
        extra_kwargs = {
            'password': {'write_only': True}  # todo: fix the password hashing issue.
        }
