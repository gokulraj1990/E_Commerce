#models.py
from django.db import models
import random
from django.contrib.auth.hashers import make_password

class User_Reg(models.Model):
    id = models.CharField(max_length=12, primary_key=True, editable=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email_id = models.EmailField(max_length=50, unique=True)
    mobile_number = models.CharField(max_length=20, null=True, unique=True)
    password = models.CharField(max_length=255)  # Use a CharField for storing hashed passwords
    gender = models.CharField(max_length=20, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')], default='O')
    is_active = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_unique_id(self):
        while True:
            # Generate a random 12-digit number as a string
            random_id = ''.join([str(random.randint(0, 9)) for _ in range(12)])
            # Check if it already exists
            if not User_Reg.objects.filter(id=random_id).exists():
                return random_id

    def save(self, *args, **kwargs):
        if not self.id:  # Only generate an ID if it's not already set
            self.id = self.generate_unique_id()
        # Hash the password before saving
        if self.password and not self.password.startswith('$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name}"
    
   