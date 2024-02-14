

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from ..serializers import *


from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from decimal import Decimal

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

#register user
@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )

     
        

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'details': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)







# Generate a random passcode
def generate_passcode():
    return get_random_string(length=6, allowed_chars='0123456789')

@api_view(['POST'])
def registerUsernew(request):
    data = request.data
    email = data.get('email', '')
    
    referal_code = data['referal']
    
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=email,  # Use email as the username
            email=email,
            password=make_password(data['password']),
           
        )

        if referal_code:
            profile = get_object_or_404(Profile, referal_code=referal_code) # Get the profile by the referal_code or return 404
            newuser = Profile.objects.get (email=user.email)
            newuser.referred_by = profile # Assign the profile object to the referred_by attribute
            newuser.save ()
    
        # Serialize user and return a response
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except Exception as e:
        message = {'details': 'User with this email already exists' if 'UNIQUE constraint' in str(e) else str(e)}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


#confirm email with passcode
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirmEmailWithPasscode(request):
    data = request.data
    user = request.user
    profile = user.profile
    email = profile.email
    passcode = data.get('passcode', '')
    
    
    try:
        profile = Profile.objects.get(passcode=passcode)
       
        # If the user exists and the passcode is correct, activate the account
        profile.is_active = True
        profile.save()

        
        email_subject = 'Email Confirmation Passcode'
        email_message = f'Email confirmed successfully'
        from_email = 'shedenbright@gmail.com'  # Change to your email address
        recipient_list = [email]
        send_mail(email_subject, email_message, from_email, recipient_list, fail_silently=False)
   
        
        return Response({"message": "Email confirmed successfully"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"detail": "Invalid passcode or email"}, status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['POST'])
def requestForgotPasswordPasscode(request):
   
    email = request.data.get('email', '')
    
    try:
        user = User.objects.get(email=email)
        profile = user.profile
        passcode = generate_passcode()
        profile.passcode= passcode
        profile.save()

        # Send the passcode to the user's email
        email_subject = 'Forgot Password Passcode'
        email_message = f'Your passcode for resetting your password: {passcode}'
        from_email = 'shedenbright@gmail.com'  # Change to your email address
        recipient_list = [email]
        send_mail(email_subject, email_message, from_email, recipient_list)

        return Response({"message": "Passcode sent to your email."}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def verifyEmail(request):
    data = request.data
    passcode = data.get('passcode','')
    profile = Profile.objects.get(passcode=passcode)
   
    try:
        
        if passcode == profile.passcode:
            return Response({"detail": "Email Verify Successful"}, status=status.HTTP_200_OK)
        

    except:
        return Response({"detail": "Invalid passcode or email"}, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def resetPassword(request):
    try:
        data = request.data
        user = request.user
        #passcode = data.get('passcode', '')
    
        #profile= Profile.objects.get(passcode=passcode)
        #user = User.objects.get(email=profile.email)

        old_password = data['old_password']
        new_password = data['new_password']

        if old_password != user.password:
            return Response(status=404)
        
        user.password = make_password(new_password)
        #profile.passcode = None  # Clear the passcode after successful reset
   
        user.save()
        return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"detail": "Invalid passcode"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UserChangePassword(request):
    try:
        data = request.data
        user = request.user

        old_password = data['old_password']
        new_password = data['new_password']

        # Verify old password
        if not check_password(old_password, user.password):
            return Response({"detail": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate new password
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({"detail": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        # Set new password
        user.password = make_password(new_password)
        user.save()

        return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"detail": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
