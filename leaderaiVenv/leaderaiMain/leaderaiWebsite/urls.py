from django.contrib import admin
from django.urls import path
from leaderaiWebsite import views as leaderaiWebsite_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', leaderaiWebsite_views.login_view, name='login'),
    path('signup/', leaderaiWebsite_views.signUp_view, name='signUp'),
    path('', leaderaiWebsite_views.main_view, name='main'),
]
