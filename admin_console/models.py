from django.db import models
from django.contrib.auth.hashers import make_password
import uuid

class User(models.Model):
    ADMIN = 'Admin'
    CUSTOMER = 'Customer'

    ACTIVE = 'Active'
    SUSPENDED = 'Suspended'

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (SUSPENDED, 'Suspended'),
    ]

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (CUSTOMER, 'Customer'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    mobilenumber = models.CharField(max_length=10, unique=True, default=None)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CUSTOMER)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def view_user_details(self):
        return {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'mobilenumber': self.mobilenumber,
            'role': self.role,
            'status': self.status,
        }

    def __str__(self):
        return f"{self.firstname} {self.lastname or ''}".strip()
