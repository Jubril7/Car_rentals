from django.shortcuts import render
from .models import Vehicle
from .form import ContactForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .form import RegisterForm, UpdateProfileForm, BookingForm, TestimonialForm
from django.contrib.auth.models import User
from .models import Booking, Testimonial
from django.contrib import messages



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

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "contact.html", {
                "form": ContactForm(),
                "success": True
            })
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form, "success": False})

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    bookings = request.user.bookings.all()
    testimonials = request.user.testimonial_set.all()
    return render(request, 'dashboard.html', {
        'bookings': bookings,
        'testimonials': testimonials
    })

@login_required
def book_car(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('booking_history')
    else:
        form = BookingForm()
    return render(request, 'book_car.html', {'form': form})

# Booking History
@login_required
def booking_history(request):
    bookings = request.user.bookings.all()
    return render(request, 'booking_history.html', {'bookings': bookings})

# Profile Update
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

# Change Password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

# Post Testimonial
@login_required
def post_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            return redirect('dashboard')
    else:
        form = TestimonialForm()
    return render(request, 'post_testimonial.html', {'form': form})

# View Testimonials
def view_testimonials(request):
    testimonials = Testimonial.objects.filter(active=True)
    return render(request, 'view_testimonials.html', {'testimonials': testimonials})

# def login_view(request):
#     message = ""

#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         try:
#             user = User.objects.get(email=email)
#             username = user.username  # Django authenticates using username
#         except User.DoesNotExist:
#             message = "Invalid email or password."
#             return render(request, "login.html", {"message": message})

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect("home")  
#         else:
#             message = "Incorrect password."

#     return render(request, "login.html", {"message": message})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "core/login.html")


