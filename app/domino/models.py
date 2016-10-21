from django.db import models


class VPNType(models.Model):
    name = models.CharField(max_length=100, default='')
    command = models.CharField(max_length=400, default='')
    docker_image_name = models.CharField(max_length=400, default='')

    # TODO: remove when stable
    def __str__(self):
        return self.name


class VPN(models.Model):
    #implement type of the VPN
    name = models.CharField(max_length=100, default='')
    conf_file = models.TextField(null=True, blank=False)
    vpn_type = models.ForeignKey(
        VPNType,
        on_delete=models.PROTECT,
        null=True,
        blank=False
    )

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=300, default='')
    extended_name = models.CharField(max_length=300, default='')
    vpn = models.ForeignKey(
        VPN,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

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
    model = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField()
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name
