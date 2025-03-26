from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# Home Page View
def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        print(f"Received Username: {username}")  # Debugging
        print(f"Received Password: {password}")  # Debugging
        
        user = authenticate(request, username=username, password=password)
        print(f"Authenticated User: {user}")  # Debugging
        
        if user is not None:
            login(request, user)
            print("Login successful")  # Debugging
            return redirect('inventory')
        else:
            print("Invalid credentials")  # Debugging
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

# Features Page View
def features(request):
    return render(request, 'feature.html')

# Inventory Page View
def inventory_view(request):
    return render(request, 'inventory.html')
