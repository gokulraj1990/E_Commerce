from django.db import models
from product_mgmt.models import Product

class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    customerID = models.IntegerField()
    productID = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='productID')
    quantity = models.IntegerField()
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2)
    orderDate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        # Calculate total price based on product price and quantity
        self.totalPrice = self.productID.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order {self.orderID}'
