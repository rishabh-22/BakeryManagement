from django.contrib import admin

from admins.models import Items, Ingredients
from customer.models import Customer, Orders

admin.site.register(Items)
admin.site.register(Ingredients)
admin.site.register(Customer)
admin.site.register(Orders)
