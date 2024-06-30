from django.shortcuts import render, redirect
from .models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from .tokens import account_activation_token

User = get_user_model()

def send_verification_email(user, request):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    message = render_to_string('acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # Redirect to a success page
        return redirect('activation_success')
    else:
        # Invalid link
        return redirect('activation_invalid')


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

def logout_view(request):
    logout(request)
    return render(request, 'main.html')

def main_view(request):
    return render(request, 'main.html')

def contact_view(request):
    return render(request, 'contact.html')

def paywall_view(request):
    return render(request, 'paywall.html')

def email_verification_sent(request):
    return render(request, 'email_verification_sent.html')

def activation_success(request):
    return render(request, 'activation_success.html')

def activation_invalid(request):
    return render(request, 'activation_invalid.html')

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
        user.is_active = False
        user.save()
        send_verification_email(user,request)
        return HttpResponseRedirect(reverse('email_verification_sent'))

        # Optionally, authenticate and log in the user
        # user = authenticate(request, email=email, password=password)
        # if user is not None:
        #     login(request, user)
        #     return HttpResponseRedirect(reverse('profile'))  # Redirect to user's profile page

        return HttpResponseRedirect(reverse('login'))  # Redirect to login page after successful registration

    return render(request, 'signUp.html')
