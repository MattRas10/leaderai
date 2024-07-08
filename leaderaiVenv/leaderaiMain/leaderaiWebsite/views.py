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
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import stripe
import time
from django.views import View
from .forms import SubscriptionForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY
INSIGHT_PRICE_ID = settings.INSIGHT_PRICE_ID
PROFESSIONAL_PRICE_ID = settings.PROFESSIONAL_PRICE_ID
PROFESSIONAL_PLUS_PRICE_ID = settings.PROFESSIONAL_PLUS_PRICE_ID
#ENTERPRISE_PRICE_ID = settings.ENTERPRISE_PRICE_ID
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
def useQuery(request):
    user = request.user  # Assuming UserProfile is related to User
    if user.queries > 0:
        user.queries -= 1
        user.save()
    return redirect('/')
@login_required
def subscribe_view(request):
    return render(request, 'subscribe.html')
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
#These next 3 methods could be simplified into 1 most likely.
@method_decorator(login_required, name='dispatch')
class InsightSubscribeView(View):
    def get(self, request):
        # Replace with your actual price ID for the Insight plan
        price_id = settings.INSIGHT_PRICE_ID

        try:
            # Create a Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                customer_email=request.user.email,
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': price_id,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=request.build_absolute_uri(reverse('subscription_success')),
                cancel_url=request.build_absolute_uri(reverse('subscription_cancelled')),
            )

            # Redirect to Stripe Checkout page
            return redirect(checkout_session.url)
        except stripe.error.StripeError as e:
            return render(request, 'error.html', {'error': str(e)})
class ProfessionalSubscribeView(View):
    def get(self, request):
        # Replace with your actual price ID for the Insight plan
        price_id = settings.PROFESSIONAL_PRICE_ID

        try:
            # Create a Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                customer_email=request.user.email,
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': price_id,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=request.build_absolute_uri(reverse('subscription_success')),
                cancel_url=request.build_absolute_uri(reverse('subscription_cancelled')),
            )

            # Redirect to Stripe Checkout page
            return redirect(checkout_session.url)
        except stripe.error.StripeError as e:
            return render(request, 'error.html', {'error': str(e)})
class ProfessionalPlusSubscribeView(View):
    def get(self, request):
        # Replace with your actual price ID for the Insight plan
        price_id = settings.PROFESSIONAL_PLUS_PRICE_ID

        try:
            # Create a Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                customer_email=request.user.email,
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': price_id,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=request.build_absolute_uri(reverse('subscription_success')),
                cancel_url=request.build_absolute_uri(reverse('subscription_cancelled')),
            )

            # Redirect to Stripe Checkout page
            return redirect(checkout_session.url)
        except stripe.error.StripeError as e:
            return render(request, 'error.html', {'error': str(e)})
def subscription_success(request):
    return render(request, 'subscription_success.html')
def subscription_cancelled(request):
    return render(request, 'subscription_cancelled.html')
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.WEBHOOK_SECRET  # Replace with your webhook secret

    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print(f"Invalid payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(f"Signature verification error: {e}")
        return HttpResponse(status=400)

    print(f"Received event: {event['type']}")

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(f"Checkout session completed: {session}")

        # Fulfill the purchase and update the user subscription
        handle_checkout_session(session)

    return JsonResponse({'status': 'success'})
def handle_checkout_session(session):
    # Retrieve the user email from the session
    user_email = session['customer_details']['email']
    subscription_id = session['subscription']
    line_items = stripe.checkout.Session.list_line_items(session['id'])
    price_id = line_items['data'][0]['price']['id']

    print(
        f"Handling checkout session for email: {user_email}, subscription_id: {subscription_id}, price_id: {price_id}")

    # Determine subscription type based on price_id
    subscription_type = determine_subscription_type(price_id)
    queries = determine_queries(price_id)

    try:
        user = User.objects.get(email=user_email)
        user.stripe_subscription_id = subscription_id
        user.subscription_type = subscription_type
        user.subscription_active = True
        user.queries = queries
        user.save()
        print(f"Updated user {user_email} with subscription type {subscription_type}")
    except User.DoesNotExist:
        print(f"User with email {user_email} does not exist")
        # Handle the case where the user does not exist
        pass
def determine_subscription_type(price_id):
    # Map Stripe price_id to your subscription type logic
    # Example mapping, customize based on your actual Stripe products and prices
    if price_id == INSIGHT_PRICE_ID:
        return 'INSIGHT'
    elif price_id == PROFESSIONAL_PRICE_ID:
        return 'PROFESSIONAL'
    elif price_id == PROFESSIONAL_PLUS_PRICE_ID:
        return 'PROFESSIONAL_PLUS'
    #elif price_id == ENTERPRISE_PRICE_ID:
    #    return 'ENTERPRISE'
    else:
        return 'UNKNOWN'  # Handle unknown cases or raise an error
def determine_queries(price_id):
    # Map Stripe price_id to your subscription type logic
    # Example mapping, customize based on your actual Stripe products and prices
    if price_id == INSIGHT_PRICE_ID:
        return 50
    elif price_id == PROFESSIONAL_PRICE_ID:
        return 500
    elif price_id == PROFESSIONAL_PLUS_PRICE_ID:
        return 2000
    # elif price_id == ENTERPRISE_PRICE_ID:
    #    return 'ENTERPRISE'
    else:
        return 'UNKNOWN'  # Handle unknown cases or raise an error