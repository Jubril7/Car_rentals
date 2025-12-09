from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Booking, Testimonial, Contact

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

class UpdateProfileForm(UserChangeForm):
    password = None  # hide password field
    class Meta:
        model = User
        fields = ['username', 'email', 'phone']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['vehicle', 'start_date', 'end_date']

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['message']
