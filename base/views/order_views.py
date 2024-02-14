from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import status
from base.models import Order,Profile,Shipping
from base.serializers  import *
from django.db.models import Q


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def creatOrder(request):
    data= request.data
    seller=request.user.profile
    name = data.get('name')
    description = data.get('description')
    amount =data.get('amount')

    order= Order.objects.create(
        seller = seller,
        product_name = name,
        product_description = description,
        amount = amount
    )

    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getOrderById(request,pk):
    order = Order.objects.get(id=pk)
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
#@permission_classes([IsAuthenticated])
def OrderPaid(request, pk):
    order = Order.objects.get(id=pk)
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def OrderPaid(request, pk):
    order = Order.objects.get(id=pk)
    data = request.data
    user = request.user.profile
    print(user)

    """shipping = Shipping(
        profile = user,
        address= data.get('address'),
        city= data.get('city'),
        country = data.get('country'),
        post_code = data.get('postal_code')

    )
    """
    order.buyer= user
    order.is_paid = True
    order.status = 'processing'
    if order.is_paid:
        seller_balance = Balance.objects.get(profile=order.seller)
        seller_balance.pending_balance += order.amount
        seller_balance.save()

    order.save()

    return Response('Order Paid')


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def Order_delivered(request, pk):
    order = get_object_or_404(Order, id=pk)

    # Check if the order has already been delivered
    if order.status == 'delivered':
        return Response({'detail': 'Order has already been delivered'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the current user is the buyer of the order
    if request.user.profile != order.buyer:
        return Response({'detail': 'You do not have permission to mark this order as delivered'}, status=status.HTTP_403_FORBIDDEN)

    # Update order status and balances
    order.status = 'delivered'
    seller_balance = Balance.objects.get(profile=order.seller)
    seller_balance.available_balance += order.amount

    if seller_balance.pending_balance <= 0:
        return Response({'detail': 'Seller\'s pending balance is zero or negative. Cannot proceed with order delivery.'}, status=status.HTTP_400_BAD_REQUEST)

    seller_balance.pending_balance -= order.amount
    seller_balance.save()
    order.save()

    return Response({'detail': 'Order delivered successfully'})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def UpdateOrder(requst,pk):
    order = Order.objects.get(id=pk)
    data = requst.data
    order.product_name = data.get('name')
    order.product_description = data.get('description')
    order.amount= data.get('amount')
    order.save()
    return Response('Order updated')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserOrder(request):
    user = request.user.profile
    orders = Order.objects.filter(Q(seller=user) | Q(buyer=user)).order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
