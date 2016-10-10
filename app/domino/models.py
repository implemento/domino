from django.db import models



class Customer(models.Model):
    name = models.CharField(max_length=300, default='')
    extended_name = models.CharField(max_length=300, default='')

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=300, default='')

    def __str__(self):
        return self.name


class Server(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, default='')
    model = models.CharField(max_length=100)
    model.blank = True
    serial_number = models.CharField(max_length=100)
    serial_number.blank = True
    ip_address = models.GenericIPAddressField()
    enabled = models.BooleanField(default=True)
    requires_vpn = models.BooleanField(default=False)

    def __str__(self):
        return self.name
