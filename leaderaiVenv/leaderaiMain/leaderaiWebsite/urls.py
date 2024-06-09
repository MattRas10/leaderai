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
]
