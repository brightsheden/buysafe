from rest_framework.decorators import api_view, permission_classes,parser_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from base.serializers  import *
from base.models import *


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    try:
        profile = request.user.profile
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userbalance(request):
    try:
        profile = request.user.profile
        balance = Balance.objects.get(profile=profile)
        serializer = BalanceSerializer(balance, many=False)
        return Response(serializer.data)
    except Balance.DoesNotExist:
        return Response({'error': 'Balance not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def editProfile(request):
    user = request.user
    data = request.data

    try:
        profile = user.profile
        

    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    profile.image = data.get('image', profile.image)
    user.username = data.get('username',user.username)
    user.email = data.get('email', user.email)
    profile.name = user.username
    profile.email =  user.email
    profile.phone = data.get('phone', profile.phone)
    user.save()
    profile.save()
    return Response({'message': 'Profile update successful'})



#withdraw endpoints

from rest_framework.views import APIView
from rest_framework.response import Response


class WithdrawalListCreateView(APIView):
    def get(self, request):
        withdrawals = Withdrawal.objects.all()
        serializer = WithdrawalSerializer(withdrawals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WithdrawalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    


from decimal import Decimal

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_withdrawal(request):
    try:
        # Get the authenticated user
        user = request.user
        
        # Extract withdrawal data from the request
        data = request.data
        print(data)
        
        # Validate input data
        required_fields = ['amount', 'accountName', 'bankName', 'accountNumber']
        if not all(field in data for field in required_fields):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new Withdrawal instance
        withdrawal = Withdrawal(
            profile=user.profile,
            amount=data['amount'],
            account_name=data['accountName'],
            bank_name=data['bankName'],
            account_number=data['accountNumber'],
            is_approved=False
        )
        
        profile = user.profile.balance
        profile.available_balance -= Decimal(withdrawal.amount) 
        profile.pending_withdrawal += Decimal(withdrawal.amount) 
        profile.save()
        # Save the withdrawal to the database
        withdrawal.save()

        
        # Return success response
        serializer = WithdrawalSerializer(withdrawal)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        # Handle any exceptions
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def approve_withdrawal(request,pk):
    withdrawal = Withdrawal.objects.get(pk=pk)
    profile = profile.objects.get(id=withdrawal.profile)
    profile.pending_withdrawal  -= withdrawal.amount
    profile.payout = withdrawal.amount
    profile.save()
    withdrawal.is_approved = True
    withdrawal.save()
    return Response({"message":"Withdrawal approved"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_withdrawals(request):
    user = request.user.profile
    withdrawals = Withdrawal.objects.filter(profile=user)
    serializer = WithdrawalSerializer(withdrawals, many=True)
    return Response(serializer.data)

class ApproveWithdrawalView(APIView):
    def post(self, request, pk):
        try:
            withdrawal = Withdrawal.objects.get(pk=pk)
            
            # Update the profile's balance
            profile = withdrawal.profile
            profile.pending_withdrawal -= withdrawal.amount
            profile.payout += withdrawal.amount
            profile.save()
            
            # Update the withdrawal status
            withdrawal.is_approved = True
            withdrawal.save()
            
            return Response({"message": "Withdrawal approved"}, status=status.HTTP_200_OK)
        except Withdrawal.DoesNotExist:
            return Response({"error": "Withdrawal not found"}, status=status.HTTP_404_NOT_FOUND)