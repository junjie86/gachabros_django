from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm

def user_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
      
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')  # Field from form
        password = request.POST.get('password')

        # Check if the input is an email
        user = None
        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                username = user.username  # Get the associated username
            except User.DoesNotExist:
                messages.error(request, "Invalid email or username.")
                return render(request, 'core/login.html', {'form': AuthenticationForm()})
        else:
            username = username_or_email  # If it's a username, use it directly

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect(reverse('dashboard'))  # Redirect after login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'registration/login.html', {'form': AuthenticationForm()})
