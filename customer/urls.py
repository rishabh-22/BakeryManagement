from django.urls import path

from customer.views import registration_view, login_view, items_view, place_order_view, see_order_view

urlpatterns = [
    path('register/', registration_view),
    path('login/', login_view),
    path('view-items/', items_view),
    path('order/', place_order_view),
    path('view-orders/', see_order_view),
]
