from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=300)


class Brand(models.Model):
    pass


class Server(models.Model):
    customer_id = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE
    )
    brand_id = models.ForeignKey(
        'Brand',
        on_delete=models.CASCADE
    )
    hostname = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    enabled = models.BooleanField(default=True)