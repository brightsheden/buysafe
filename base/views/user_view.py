from rest_framework.decorators import api_view, permission_classes,parser_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from base.serializers  import *
from base.models import Profile


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
