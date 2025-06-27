from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.contrib.auth import authenticate, login



from familyconnect.settings import DEFAULT_FROM_EMAIL
from .models import CustomUser, UserRole

def register_page(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        name = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Basic field checks
        if not name or not email or not password or not confirm_password:
            messages.error(request, "All required fields (Name, Email, Password) are mandatory.")
            return render(request, 'users/register.html', {
                'username': name,
                'email': email,
            })

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'users/register.html', {
                'username': name,
                'email': email,
            })

        if CustomUser.objects.filter(username=name).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'users/register.html', {'email': email})

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'users/register.html', {'username': name})

       


        # Create user if everything is fine
        try:
            CustomUser.objects.create(
                username=name,
                email=email,
                password=make_password(password),
                role=UserRole.USER
            )
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('users:login')
        except IntegrityError:
            messages.error(request, "Account already exists. Please try again.")
        except Exception as e:
            messages.error(request, f"Unexpected error: {e}")

    return render(request, 'users/register.html')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('core:home') 

    if request.method == 'POST':
        email = request.POST.get('email', '').lower().strip()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, "Please enter both email and password.")
            return render(request, 'users/login.html', {'email': email})

  
        from .models import CustomUser
        try:
            user_obj = CustomUser.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('core:home')
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'users/login.html', {'email': email})

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('users:login')