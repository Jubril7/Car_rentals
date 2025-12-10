from django.utils import timezone
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Booking, Testimonial, Contact
from django.core.exceptions import ValidationError

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

class UpdateProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'email', 'phone']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['message']

class BookingForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Booking
        fields = ['vehicle', 'start_date', 'end_date']

    def clean(self):
        cleaned = super().clean()

        vehicle = cleaned.get('vehicle')
        start = cleaned.get('start_date')
        end = cleaned.get('end_date')

        if not vehicle or not start or not end:
            return cleaned

        # Ensure start <= end
        if start > end:
            raise ValidationError("Start date must be before or equal to end date.")

        # Prevent past bookings
        today = timezone.localdate()
        if start < today:
            raise ValidationError("Start date cannot be in the past.")

        # Check overlapping bookings
        overlapping = Booking.objects.filter(
            vehicle=vehicle,
            status__in=['Pending', 'Confirmed'],
            start_date__lte=end,
            end_date__gte=start,
        ).exists()

        if overlapping:
            raise ValidationError(
                "This vehicle is already booked for those dates. Please select another date or vehicle."
            )

        return cleaned

