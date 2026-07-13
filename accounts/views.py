from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.http import JsonResponse
import csv
import io
from openpyxl import Workbook
from accounts.models import User
from categories.models import Category
from products.models import Product, ProductImage
from enquiries.models import Enquiry

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard_home')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        # We can find user by email or username since accounts.User inherits from AbstractUser
        user = None
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = authenticate(request, username=email, password=password)
            
        if user is not None:
            auth_login(request, user)
            if not remember_me:
                request.session.set_expiry(0) # Browser close session expiry
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard_home')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            
    return render(request, 'login.html')

def user_logout(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')
