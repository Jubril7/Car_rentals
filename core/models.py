from django.db import models
from django.contrib.auth.models import AbstractUser


class VehicleBrand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE, related_name='vehicles')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    daily_rent = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.brand.name} - {self.name}"
    

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[('Pending','Pending'),('Confirmed','Confirmed'),('Cancelled','Cancelled')],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
