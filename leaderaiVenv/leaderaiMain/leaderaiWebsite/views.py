from django.shortcuts import render
from .models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login

def login_view(request):
    error_message = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me') == 'on'

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)

            # Optionally, handle remember me functionality
            if not remember_me:
                request.session.set_expiry(0)  # Session expires when the user closes the browser

            # Redirect to a specific page after successful login
            return HttpResponseRedirect(reverse('main'))  # Change 'dashboard' to your desired URL name

        # If authentication fails, redirect back to the login page with an error message
        error_message = "Invalid email or password. Please try again."

        return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def main_view(request):
    return render(request, 'main.html')

def signUp_view(request):
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        agree_terms = request.POST.get('agree_terms')

        # Check if the user has agreed to the terms
        if not agree_terms:
            return HttpResponseRedirect(reverse('signUp'))  # Redirect to sign-up page with error message

        # Create a new user
        user = User.objects.create_user(email=email, password=password, full_name=name, account_name=name,
                                        phone_number='', )

        # Optionally, authenticate and log in the user
        # user = authenticate(request, email=email, password=password)
        # if user is not None:
        #     login(request, user)
        #     return HttpResponseRedirect(reverse('profile'))  # Redirect to user's profile page

        return HttpResponseRedirect(reverse('login'))  # Redirect to login page after successful registration

    return render(request, 'signUp.html')
