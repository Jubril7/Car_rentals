from django import forms
from .models import Contact
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Booking, Testimonial

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

class UpdateProfileForm(UserChangeForm):
    password = None  
    class Meta:
        model = User
        fields = ['username', 'email', 'phone']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['vehicle', 'start_date', 'end_date']

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['message']

class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]