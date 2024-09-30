from django.db import models

class CustomerProfile(models.Model):
    user = models.OneToOneField('admin_console.User', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    def update_profile(self, new_address, new_phone):
        self.address = new_address
        self.phone = new_phone
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.phone}"
