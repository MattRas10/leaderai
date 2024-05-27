from django.shortcuts import render

def login_view(request):
    if request.method == 'POST':
        # Handle login logic here
        pass
    return render(request, 'leaderaiWebsite/login.html')

def main_view(request):
    return render(request, 'leaderaiWebsite/main.html')
