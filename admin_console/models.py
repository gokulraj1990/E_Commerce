#models.py
from django.db import models
from django.contrib.auth.hashers import make_password
import random

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
         (ADMIN , 'Admin'),
    (CUSTOMER , 'Customer'),
    ]

    # Unique identifier for the user
    id = models.CharField(max_length=12, primary_key=True, editable=False)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords
    role = models.CharField(max_length=20,choices=ROLE_CHOICES, default=CUSTOMER)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_unique_id(self):
        while True:
            random_id = ''.join([str(random.randint(0, 9)) for _ in range(12)])
            if not User.objects.filter(id=random_id).exists():
                return random_id

    def save(self, *args, **kwargs):
        if not self.id:  # Only generate an ID if it's not already set
            self.id = self.generate_unique_id()
        if self.password and not self.password.startswith('$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def view_user_details(self):
        return {
            'firstname': self.firstname,
            'lastname': self.lastname, 
            'email': self.email,
            'role': self.role,
            'status': self.status,
        }

    def __str__(self):
        return f"{self.firstname} {self.lastname or ''}".strip() 
