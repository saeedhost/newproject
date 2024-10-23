from django.contrib import admin
from django.urls import path
from newproject import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name="Home"),
    path('about-us/', views.about, name="About"),
    path('contact-us/', views.contact, name="Contact"),
    path('services/', views.service, name="Service"),
    path('roadmap/', views.roadmap, name="Roadmap"), 
    path('', views.signin, name="Signin"), 
    path('signup/', views.signup, name="Signup"), 
    path('signout/', views.signout, name="Signout"), 
    path('request-otp/', views.request_otp_view, name="RequestOtp"), 
    path('show-otp/', views.show_otp_view, name="ShowOtp"), 
    
    path('custom-header-test/', views.custom_header_test, name="custom_header_test"), 
    
    
]
