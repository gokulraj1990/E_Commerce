import uuid
from django.db import models
from django.core.exceptions import ValidationError
from admin_console.models import User



class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Kitchen Appliances', 'Kitchen Appliances'),
        ('Home Appliances', 'Home Appliances'),
        ('Entertainment', 'Entertainment'),
        ('Books', 'Books'),
    ]

    productID = models.CharField(max_length=30, primary_key=True, editable=False)
    productname = models.CharField(max_length=30)
    model = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    price = models.FloatField()
    stock = models.IntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    imageUrl = models.URLField(max_length=200, blank=True)  # URL to the product image

    def save(self, *args, **kwargs):
        if not self.productID:  # Generate ID only if it doesn't exist
            new_id = uuid.uuid4().hex  # Generate a new UUID
            while Product.objects.filter(productID=new_id).exists():  # Check for uniqueness
                new_id = uuid.uuid4().hex  # Generate another one if not unique
            self.productID = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.productname} {self.model or ''}".strip()


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default=1)  # Set default user
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['rated_by', 'product'], name='unique_review_per_product')
        ]

    def clean(self):
        if not (1 <= self.rating <= 5):
            raise ValidationError('Rating must be between 1 and 5.')

    def __str__(self):
        return f'Review for {self.product.productname} - Rating: {self.rating}'







# class Review(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
#     rating = models.IntegerField()
#     comment = models.TextField(blank=True)
#     rated_by = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def clean(self):
#         if not (1 <= self.rating <= 5):
#             raise ValidationError('Rating must be between 1 and 5.')

#     def __str__(self):
#         return f'Review for {self.product.productname} - Rating: {self.rating}'

