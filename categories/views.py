from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category
from dashboard.views import role_required

@login_required
@role_required(['super_admin', 'admin'])
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/categories/list.html', {'categories': categories})

@login_required
@role_required(['super_admin', 'admin'])
def category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        is_active = request.POST.get('is_active') == 'on'
        
        if Category.objects.filter(name__iexact=name).exists():
            messages.error(request, "A category with this name already exists.")
        else:
            Category.objects.create(
                name=name,
                description=description,
                image=image,
                is_active=is_active
            )
            messages.success(request, f"Category '{name}' created successfully.")
            return redirect('category_list')
            
    return render(request, 'dashboard/categories/form.html')

@login_required
@role_required(['super_admin', 'admin'])
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        if request.FILES.get('image'):
            category.image = request.FILES.get('image')
        category.is_active = request.POST.get('is_active') == 'on'
        category.save()
        messages.success(request, f"Category '{category.name}' updated successfully.")
        return redirect('category_list')
        
    return render(request, 'dashboard/categories/form.html', {'category': category})

@login_required
@role_required(['super_admin', 'admin'])
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    name = category.name
    category.delete()
    messages.success(request, f"Category '{name}' deleted successfully.")
    return redirect('category_list')
