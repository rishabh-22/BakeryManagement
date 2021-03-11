import logging
import uuid
from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from admins.models import Items
from customer.models import Orders, Customer
from customer.serializers import RegistrationSerializer


@api_view(['GET', 'POST'])
@permission_classes([])
def registration_view(request):
    """
    this function is used for registering a user into the system.
    :param request:
    :return:
    """
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user=user).key
        response = dict(message='successfully registered.', token=token)
        return Response(response, status=status.HTTP_200_OK)
    else:
        response = serializer.errors
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([])
def login_view(request):
    """
    this function is used for returning an auth token to a valid user.
    :param request:
    :return:
    """
    try:
        user = User.objects.get(username=request.data['username'])
        if user.password != request.data['password']:
            raise Exception
        token, created = Token.objects.get_or_create(user=user)
        response = dict(message='login successful.', token=token.key)
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        logging.debug(e)
        return Response({
            'error': 'provided data is incorrect.'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
@permission_classes([IsAuthenticated])
def items_view(request):
    """
    this method is used to get the list of all available items
    ** pagination to be implemented later **
    :param request:
    :return:
    """
    try:
        response = []
        items = Items.objects.all()
        for item in items:
            response.append({
                'name': item.name,
                'quantity': item.quantity,
                'price': item.sell_price,
                'mfg_date': item.mfg_date,
                'exp_date': item.expiry_date,
                'ingredients': item.ingredients
            })
        return Response({'items': response}, status=status.HTTP_200_OK)
    except Exception as e:
        logging.exception(e)
        return Response({
            'message': 'Sorry some error occurred. Please try again later.'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def place_order_view(request):
    """
    this method is used to place an order by the user.
    :param request:
    :return:
    """
    try:  # todo: add provision for adding more than one item in a single order
        error = False
        item_id = request.data.get('item_id', None)
        if not item_id:
            error = True
            message = "Please attach an item_id with the request."
            return
        item = Items.objects.get(id=item_id)
        if item.quantity > 0 and item.quantity > request.data.get('quantity', 1):
            item.quantity -= request.data.get('quantity', 1)
            order = Orders.objects.create(
                buyer=request.user,
                item=item,
                created=datetime.now(),
                total_amount=item.sell_price*request.data.get('quantity', 1),
                quantity=request.data.get('quantity', 1),
                payment_type=request.data.get('payment_type', 'COD'),
                shipping_address=request.user.username,
                transaction_id=uuid.uuid4().hex
            )
            order.save()
            item.save()
            message = "Thank you for placing your order with us.\nHere's your invoice."
            customer = Customer.objects.get(username=request.user.username)
            invoice = {
                'transaction_id': order.transaction_id,
                'buyer': order.buyer.username,
                'item': order.item.name,
                'order_date': order.created,
                'total_amount': order.total_amount,
                'payment_type': order.payment_type,
                'shipping_address': customer.address

            }
        else:
            error = True
            message = "Sorry, that product is out of stock for this quantity."
    except ObjectDoesNotExist:
        error = True
        message = "Sorry, you seem to have an id of an item which isn't available with us."
    except Exception as e:
        error = True
        logging.exception(e)
        message = "Sorry, some error occurred at our end, please try again later."
    finally:
        if not error:
            return Response({
              'message': message,
              'invoice': invoice
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': message
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
@permission_classes([IsAuthenticated])
def see_order_view(request):
    """
    this method is used to get all the orders associated with a user.
    :param request:
    :return:
    """
    try:
        response = []
        orders = Orders.objects.filter(buyer=request.user)
        for order in orders:
            response.append({
                'item': order.item.name,
                'item_id': order.item.id,
                'order_date': order.created,
                'status': order.status,
                'amount': order.total_amount,
                'is_cancelled': order.is_cancelled,
                'payment_type': order.payment_type,
                'shipping_address': order.shipping_address,
                'transaction_id': order.transaction_id
            })
        return Response({
            'orders': response
        }, status=status.HTTP_200_OK)
    except Exception as e:
        logging.exception(e)
        return Response({
            'message': 'Sorry some error occurred. Please try again later.'
        }, status=status.HTTP_400_BAD_REQUEST)
