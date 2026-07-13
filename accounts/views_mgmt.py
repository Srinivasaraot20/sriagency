from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from dashboard.views import role_required

@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        if request.FILES.get('avatar'):
            user.avatar = request.FILES.get('avatar')
            
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password:
            if password == confirm_password:
                user.set_password(password)
                messages.success(request, "Profile and password updated successfully. Please login again.")
                user.save()
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match.")
        else:
            user.save()
            messages.success(request, "Profile updated successfully.")
            
    return render(request, 'dashboard/profile.html')

@login_required
@role_required(['super_admin', 'admin'])
def user_list(request):
    users = User.objects.all()
    return render(request, 'dashboard/users/list.html', {'users': users})

@login_required
@role_required(['super_admin'])
def user_add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role
            )
            messages.success(request, f"User '{username}' created successfully.")
            return redirect('user_list')
            
    return render(request, 'dashboard/users/form.html')

@login_required
@role_required(['super_admin'])
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.email = request.POST.get('email')
        user.role = request.POST.get('role')
        user.is_active = request.POST.get('is_active') == 'on'
        
        password = request.POST.get('password')
        if password:
            user.set_password(password)
            messages.success(request, f"User '{user.username}' updated with new password.")
        else:
            messages.success(request, f"User '{user.username}' updated successfully.")
            
        user.save()
        return redirect('user_list')
        
    return render(request, 'dashboard/users/form.html', {'target_user': user})

@login_required
@role_required(['super_admin'])
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
    else:
        name = user.username
        user.delete()
        messages.success(request, f"User '{name}' deleted successfully.")
    return redirect('user_list')
