from django.shortcuts import render

def login_view(request):
    if request.method == 'POST':
        # Handle login logic here
        pass
    return render(request, 'login.html')

def main_view(request):
    return render(request, 'main.html')

def signUp_view(request):
    if request.method == 'POST':
        #Handle sign up logic here
        pass
    return render(request, 'signUp.html')
