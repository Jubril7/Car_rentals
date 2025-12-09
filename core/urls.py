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

]