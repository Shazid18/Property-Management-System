from django.urls import path

from . import views

# app_name = "polls"
urlpatterns = [
    path("home/", views.home, name="home"),
    path('sign-up/', views.property_owner_sign_up, name='property_owner_sign_up'),
    path('sign-up/success/', views.property_owner_sign_up_success, name='property_owner_sign_up_success'),
]
