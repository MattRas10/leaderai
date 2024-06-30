from django.contrib import admin
from django.urls import path
from . import views as leaderaiWebsite_views

urlpatterns = [
    path('login/', leaderaiWebsite_views.login_view, name='login'),
path('logout/', leaderaiWebsite_views.logout_view, name='logout'),
    path('signup/', leaderaiWebsite_views.signUp_view, name='signUp'),
    path('', leaderaiWebsite_views.main_view, name='main'),
    path('contact/', leaderaiWebsite_views.contact_view, name='contact'),
    path('paywall/', leaderaiWebsite_views.paywall_view, name='paywall'),
    path('activate/<uidb64>/<token>/', leaderaiWebsite_views.activate, name='activate'),
    path('email_verification_sent/', leaderaiWebsite_views.email_verification_sent, name='email_verification_sent'),
    path('activation_success/', leaderaiWebsite_views.activation_success, name='activation_success'),
    path('activation_invalid/', leaderaiWebsite_views.activation_invalid, name='activation_invalid'),
]
