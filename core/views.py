from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Vehicle, Booking, Testimonial
from .form import (
    ContactForm, RegisterForm, UpdateProfileForm,
    BookingForm, TestimonialForm
)


# --------------------- HOME ---------------------
def home(request):
    vehicles = Vehicle.objects.all()
    success = False

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = ContactForm()
    else:
        form = ContactForm()

    return render(request, "home.html", {
        "vehicles": vehicles,
        "contact_form": form,
        "success": success
    })


# --------------------- REGISTER ---------------------
def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


# --------------------- LOGIN ---------------------
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm() 

    return render(request, "login.html", {"form": form})


# --------------------- LOGOUT ---------------------
def user_logout(request):
    logout(request)
    return redirect("login")



@login_required
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    testimonials = Testimonial.objects.all() 
    return render(request, "dashboard.html", {
        "bookings": bookings,
        "testimonials": testimonials
    })


# --------------------- BOOK CAR ---------------------
@login_required
def book_car(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.status = "Pending"   # ⭐ IMPORTANT
            booking.save()
            messages.success(request, "Booking created successfully!")
            return redirect("booking_history")

    form = BookingForm()
    return render(request, "book_car.html", {"form": form})


# --------------------- BOOKING HISTORY ---------------------

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'booking_history.html', {'bookings': bookings})



# --------------------- UPDATE PROFILE ---------------------
@login_required
def update_profile(request):
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("dashboard")
    else:
        form = UpdateProfileForm(instance=request.user)

    return render(request, "update_profile.html", {"form": form})


# --------------------- CHANGE PASSWORD ---------------------
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect("dashboard")

    form = PasswordChangeForm(request.user)
    return render(request, "change_password.html", {"form": form})


# --------------------- POST TESTIMONIAL ---------------------
@login_required
def post_testimonial(request):
    if request.method == "POST":
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            return redirect("dashboard")

    form = TestimonialForm()
    return render(request, "post_testimonial.html", {"form": form})


# --------------------- VIEW TESTIMONIALS ---------------------
def view_testimonials(request):
    testimonials = Testimonial.objects.filter(active=True)
    return render(request, "view_testimonial.html", {
        "testimonials": testimonials
    })
