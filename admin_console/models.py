from django.db import models
import uuid
from django.contrib.auth.hashers import make_password

class User(models.Model):
    VENDOR = 'Vendor'
    CUSTOMER = 'Customer'

    ACTIVE = 'Active'
    SUSPENDED = 'Suspended'
    DEACTIVATED = 'Deactivated'

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (SUSPENDED, 'Suspended'),
        (DEACTIVATED, 'Deactivated')
    ]

    ROLE_CHOICES = [
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    mobilenumber = models.CharField(max_length=10, unique=True, default=None)
    password = models.CharField(max_length=255, default=None)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CUSTOMER)
    account_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        # If password is plain-text and not already hashed
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        # Save the instance
        super().save(*args, **kwargs)

    def get_dirty_fields(self):
        """Helper method to check which fields have changed."""
        dirty_fields = {}

        if self.pk:  # Only check for dirty fields if this is an existing instance
            try:
                original = User.objects.get(pk=self.pk)  # Get the original instance from DB

                # Compare current fields with the original fields
                for field in self._meta.fields:
                    current_value = getattr(self, field.name)
                    original_value = getattr(original, field.name)

                    # If the value has changed, add it to the dirty_fields dictionary
                    if current_value != original_value:
                        dirty_fields[field.name] = current_value

            except User.DoesNotExist:
                # If user doesn't exist (e.g., a new user), return empty
                return {}

        return dirty_fields

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


class Admin(models.Model):
    ACTIVE = 'Active'
    SUSPENDED = 'Suspended'

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (SUSPENDED, 'Suspended')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    mobilenumber = models.CharField(max_length=10, unique=True, default=None)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, default="Admin")
    account_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    admin_code = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        # If password is plain-text and not already hashed
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        # Save the instance
        super().save(*args, **kwargs)

    def get_dirty_fields(self):
        """Helper method to check which fields have changed."""
        dirty_fields = {}

        if self.pk:  # Only check for dirty fields if this is an existing instance
            try:
                original = Admin.objects.get(pk=self.pk)  # Get the original instance from DB

                # Compare current fields with the original fields
                for field in self._meta.fields:
                    current_value = getattr(self, field.name)
                    original_value = getattr(original, field.name)

                    # If the value has changed, add it to the dirty_fields dictionary
                    if current_value != original_value:
                        dirty_fields[field.name] = current_value

            except User.DoesNotExist:
                # If user doesn't exist (e.g., a new user), return empty
                return {}

        return dirty_fields
    

    def view_user_details(self):
        return {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'mobilenumber': self.mobilenumber,
            'role': self.role,
            'status': self.status,
            'admin_code': self.admin_code
        }

    def __str__(self):
        return f"Admin: {self.firstname} {self.lastname or ''}".strip()
