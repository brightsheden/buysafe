from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    number = models.CharField(max_length=15)
    address = models.TextField()
    email_verified =  models.BooleanField(default=False)
    passcode = models.IntegerField( blank=True, null=True)
    def __str__(self):
        return self.name
    

class Balance(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    available_balance = models.DecimalField(max_digits=10, default=0.00, decimal_places=2, blank=True, null=True)
    pending_balance = models.DecimalField(max_digits=10, default=0.00,decimal_places=2, blank=True, null=True)
    payout = models.DecimalField(max_digits=10,default=0.00, decimal_places=2, blank=True, null=True)
    pending_withdrawal = models.DecimalField(max_digits=10, default=0.00,decimal_places=2, blank=True, null=True)
    deposit = models.DecimalField(max_digits=10,default=0.00, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.profile.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    buyer = models.ForeignKey(Profile, related_name='buyer_orders', on_delete=models.CASCADE, blank=True, null=True)
    seller = models.ForeignKey(Profile, related_name='seller_orders', on_delete=models.CASCADE, blank=True, null=True)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    amount = models.DecimalField( max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.status}"

    def mark_delivered(self):
        self.status = 'delivered'
        self.save()

    def mark_cancelled(self):
        self.status = 'cancelled'
        self.save()


class Shipping(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    post_code = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.profile.name
    

class Transaction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type = models.CharField(max_length=200, blank=True, null=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    def __str__(self):
        return self.name
    


class Withdrawal(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account_number = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Withdrawal for {self.profile.name}"