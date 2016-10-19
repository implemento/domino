from django.contrib import admin

from .models import Server
from .models import Brand
from .models import Customer
from .models import VPN
from .models import VPNType

admin.site.register(Server)
admin.site.register(Brand)
admin.site.register(Customer)
admin.site.register(VPN)
admin.site.register(VPNType)
