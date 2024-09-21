from django.db import models

class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    customerID = models.IntegerField()
    productID = models.IntegerField()
    quantity = models.IntegerField()
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2)
    orderDate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f'Order {self.orderID}'
