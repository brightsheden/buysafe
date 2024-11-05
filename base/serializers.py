from rest_framework import serializers
from .models import Profile, Balance,Order,Shipping,Withdrawal
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken




class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User 
        fields = ['id',"_id",'username','name', 'email',"isAdmin",]

    def get_name(self,obj):
        name= obj.first_name
        if name == "":
            name = obj.email
        return name

    def get__id(self,obj):
        return obj.id
    
    def get_isAdmin(self,obj):
        return obj.is_staff



class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username','email',"isAdmin",'name', 'token']

    def get_token(self, obj):
        token =RefreshToken.for_user(obj)
        return str(token.access_token)

class ProfileSerializer(serializers.ModelSerializer):
    #total_checkings = serializers.IntegerField()
    class Meta:
        model = Profile
        fields = '__all__'

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'





class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'




class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = ['id', 'profile', 'account_name', 'bank_name', 'amount', 'account_number', 'is_approved']
        read_only_fields = ['id', 'profile']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_is_approved(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("is_approved must be a boolean value.")
        return value