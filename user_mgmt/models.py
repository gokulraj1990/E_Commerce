from django.db import models
from django.utils import timezone

class User(models.Model):
    ADMIN = 'Admin'
    CUSTOMER = 'Customer'

    ACTIVE = 'Active'
    SUSPENDED = 'Suspended'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (CUSTOMER, 'Customer'),
    ]

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (SUSPENDED, 'Suspended'),
    ]

    userID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CUSTOMER)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)
    createdDate = models.DateTimeField(default=timezone.now)

    def viewUserDetails(self):
        return {
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'status': self.status,
        }

    def __str__(self):
        return self.username


class Customer(models.Model):
    # Reference the 'User' model with 'user_mgmt.User' (app_name.Model_name)
    user = models.OneToOneField('user_mgmt.User', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    def updateProfile(self, new_address, new_phone):
        self.address = new_address
        self.phone = new_phone
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.phone}"
