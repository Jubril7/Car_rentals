from django.contrib import admin
from .models import VehicleBrand, Vehicle
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# User = get_user_model()

admin.site.register(VehicleBrand)
admin.site.register(Vehicle)
admin.site.register(User, UserAdmin)