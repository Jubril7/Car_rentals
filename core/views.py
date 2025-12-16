from django.shortcuts import render, redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import Vehicle, Booking, Testimonial, VehicleBrand
from .form import (
    ContactForm, RegisterForm, UpdateProfileForm,
    BookingForm, TestimonialForm
)
User = get_user_model()


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

            if user.is_staff:  
                return redirect("admin_dashboard")

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
    testimonials = Testimonial.objects.filter(active=True)
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


@login_required
@user_passes_test(lambda u: u.is_staff) 
def admin_dashboard(request):
    # gather counts and recent objects
    context = {
        "total_users": User.objects.count(),
        "total_bookings": Booking.objects.count(),
        "total_vehicles": Vehicle.objects.count(),
        "total_testimonials": Testimonial.objects.count(),
        "bookings": Booking.objects.order_by('-created_at')[:6],
        "testimonials": Testimonial.objects.order_by('-created_at')[:6],
    }
    return render(request, "admin_dashboard.html", context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_manage_bookings(request):
    bookings = Booking.objects.all().order_by("-created_at")
    return render(request, "admin_manage_bookings.html", {"bookings": bookings})

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_staff, login_url='login')(view_func)

@admin_required
def admin_add_vehicle(request):
    if request.method == "POST":
        brand_id = request.POST.get('brand')
        name = request.POST.get('name')
        description = request.POST.get('description')
        daily_rent = request.POST.get('daily_rent')
        available = True if request.POST.get('available') == 'on' else False
        image = request.FILES.get('image')

        brand = VehicleBrand.objects.get(id=brand_id)
        Vehicle.objects.create(
            brand=brand,
            name=name,
            description=description,
            daily_rent=daily_rent,
            available=available,
            image=image
        )
        messages.success(request, f"Vehicle '{name}' added successfully!")
        return redirect('admin_manage_vehicles')
    
    return redirect('admin_manage_vehicles')

def admin_edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    brands = VehicleBrand.objects.all()

    if request.method == "POST":
        vehicle.name = request.POST.get('name')
        vehicle.brand_id = request.POST.get('brand')
        vehicle.description = request.POST.get('description')
        vehicle.daily_rent = request.POST.get('daily_rent')
        vehicle.available = True if request.POST.get('available') == 'on' else False

        if 'image' in request.FILES:
            vehicle.image = request.FILES['image']

        vehicle.save()
        return redirect('admin_manage_vehicles')

    return render(request, 'admin_edit_vehicle.html', {
        'vehicle': vehicle,
        'brands': brands
    })

def admin_delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == "POST":
        vehicle.delete()
    return redirect('admin_manage_vehicles')



@admin_required
def admin_manage_vehicles(request):
    vehicles = Vehicle.objects.all().order_by('-created_at')
    brands = VehicleBrand.objects.all()
    return render(request, 'admin_manage_vehicles.html', {
        'vehicles': vehicles,
        'brands': brands
    })

def admin_manage_brands(request):
    brands = VehicleBrand.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        if name:
            VehicleBrand.objects.create(
                name=name,
                description=description
            )
            return redirect("admin_manage_brands")

    return render(request, "admin_manage_brands.html", {
        "brands": brands
    })


def admin_delete_brand(request, brand_id):
    brand = get_object_or_404(VehicleBrand, id=brand_id)
    brand.delete()
    return redirect("admin_manage_brands")


@admin_required
def admin_manage_testimonials(request):
    testimonials = Testimonial.objects.select_related('user').order_by('-created_at')
    return render(request, 'admin_manage_testimonials.html', {
        'testimonials': testimonials
    })


@admin_required
def toggle_testimonial(request, id):
    testimonial = get_object_or_404(Testimonial, id=id)
    testimonial.active = not testimonial.active
    testimonial.save()
    return redirect('admin_manage_testimonials')


@admin_required
def delete_testimonial(request, id):
    testimonial = get_object_or_404(Testimonial, id=id)
    testimonial.delete()
    return redirect('admin_manage_testimonials')

@admin_required
def admin_manage_users(request):
    return render(request, 'admin_manage_users.html')

@admin_required
def admin_queries(request):
    return render(request, 'admin_queries.html')

@admin_required
def admin_change_password(request):
    return render(request, 'admin_change_password.html')