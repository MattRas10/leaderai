from django.contrib import admin
from django.urls import path
from . import views as leaderaiWebsite_views

urlpatterns = [
    path('login/', leaderaiWebsite_views.login_view, name='login'),
    path('logout/', leaderaiWebsite_views.logout_view, name='logout'),
    path('signup/', leaderaiWebsite_views.signUp_view, name='signUp'),
    path('', leaderaiWebsite_views.main_view, name='main'),
    path('use_query/', leaderaiWebsite_views.useQuery, name='use_query'),
    path('contact/', leaderaiWebsite_views.contact_view, name='contact'),
    path('subscribe/', leaderaiWebsite_views.subscribe_view, name='subscribe'),
    path('activate/<uidb64>/<token>/', leaderaiWebsite_views.activate, name='activate'),
    path('email_verification_sent/', leaderaiWebsite_views.email_verification_sent, name='email_verification_sent'),
    path('activation_success/', leaderaiWebsite_views.activation_success, name='activation_success'),
    path('activation_invalid/', leaderaiWebsite_views.activation_invalid, name='activation_invalid'),
    path('subscribe/insight', leaderaiWebsite_views.InsightSubscribeView.as_view(), name='subscribe_insight'),
    path('subscribe/professional', leaderaiWebsite_views.ProfessionalSubscribeView.as_view(), name='subscribe_professional'),
    path('subscribe/professional_plus', leaderaiWebsite_views.ProfessionalPlusSubscribeView.as_view(), name='subscribe_professional_plus'),
    path('subscription_success/', leaderaiWebsite_views.subscription_success, name='subscription_success'),
    path('subscription_cancelled/', leaderaiWebsite_views.subscription_cancelled, name='subscription_cancelled'),
    path('webhooks/stripe/', leaderaiWebsite_views.stripe_webhook, name='stripe-webhook'),
]
