import uuid
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('ELEC', 'Electronics'),
        ('FASH', 'Fashion'),
        ('TOYS', 'Toys'),
    ]

    productID = models.CharField(max_length=12, primary_key=True, editable=False)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    imageUrl = models.URLField(max_length=200, blank=True)  # URL to the product image

    def save(self, *args, **kwargs):
        if not self.productID:  # Generate ID only if it doesn't exist
            self.productID = f"{self.category}{uuid.uuid4().hex[:9]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

