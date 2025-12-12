from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book-car/', views.book_car, name='book_car'),
    path('booking-history/', views.booking_history, name='booking_history'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('post-testimonial/', views.post_testimonial, name='post_testimonial'),
    path('testimonials/', views.view_testimonials, name='view_testimonials'),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/manage-bookings/", views.admin_manage_bookings, name="admin_manage_bookings"),
    path('dashboard/manage-bookings/', views.admin_manage_bookings, name='admin_manage_bookings'),
    path('dashboard/manage-vehicles/', views.admin_manage_vehicles, name='admin_manage_vehicles'),
    path('dashboard/manage-brands/', views.admin_manage_brands, name='admin_manage_brands'),
    path('dashboard/manage-testimonials/', views.admin_manage_testimonials, name='admin_manage_testimonials'),
    path('dashboard/manage-users/', views.admin_manage_users, name='admin_manage_users'),
    path('dashboard/queries/', views.admin_queries, name='admin_queries'),
    path('dashboard/change-password/', views.admin_change_password, name='admin_change_password'),

]