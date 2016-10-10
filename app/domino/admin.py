from django.contrib import admin

from .models import Server
from .models import Brand
from .models import Customer

admin.site.register(Server)
admin.site.register(Brand)
admin.site.register(Customer)
