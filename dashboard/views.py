from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count
from products.models import Product
from categories.models import Category
from enquiries.models import Enquiry
from accounts.models import User

# Role checks
def role_required(allowed_roles):
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role in allowed_roles or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            messages.error(request, "You do not have permission to access this page.")
            return redirect('dashboard_home')
        return wrapped_view
    return decorator

@login_required
def dashboard_home(request):
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    inactive_products = Product.objects.filter(is_active=False).count()
    total_categories = Category.objects.count()
    total_enquiries = Enquiry.objects.count()
    total_users = User.objects.count()
    
    # Recent items
    recent_products = Product.objects.order_by('-created_at')[:5]
    recent_enquiries = Enquiry.objects.order_by('-created_at')[:5]
    low_stock_products = Product.objects.filter(stock_quantity__lte=5).order_by('stock_quantity')[:5]
    
    # We can get counts of categories for charts
    category_product_counts = Category.objects.annotate(num_products=Count('products')).values('name', 'num_products')
    
    context = {
        'total_products': total_products,
        'active_products': active_products,
        'inactive_products': inactive_products,
        'total_categories': total_categories,
        'total_enquiries': total_enquiries,
        'total_users': total_users,
        'recent_products': recent_products,
        'recent_enquiries': recent_enquiries,
        'low_stock_products': low_stock_products,
        'category_chart_data': list(category_product_counts),
    }
    return render(request, 'dashboard/index.html', context)
