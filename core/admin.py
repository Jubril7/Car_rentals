from django.contrib import admin
from .models import VehicleBrand, Vehicle, Booking
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


User = get_user_model()

admin.site.register(VehicleBrand)
admin.site.register(Vehicle)
admin.site.register(User, UserAdmin)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('user__username', 'vehicle__name', 'vehicle__brand__name')