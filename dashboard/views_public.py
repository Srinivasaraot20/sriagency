from django.shortcuts import render
from django.db.models import Q
from products.models import Product
from categories.models import Category

def home(request):
    featured_products = Product.objects.filter(is_featured=True, is_active=True)
    all_products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'featured_products': featured_products,
        'all_products': all_products,
        'categories': categories,
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'contact.html', {'categories': categories})

def products(request, category_slug=None):
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)
    
    if not category_slug:
        category_slug = request.GET.get('category')
        
    selected_category = None
    if category_slug:
        try:
            selected_category = Category.objects.get(slug=category_slug, is_active=True)
            products = products.filter(category=selected_category)
        except Category.DoesNotExist:
            pass
            
    q = request.GET.get('q')
    if q:
        products = products.filter(
            Q(name__icontains=q) | 
            Q(brand__icontains=q) | 
            Q(short_description__icontains=q) |
            Q(full_description__icontains=q)
        )
        
    sort = request.GET.get('sort')
    if sort == 'price_low':
        products = products.order_by('selling_price')
    elif sort == 'price_high':
        products = products.order_by('-selling_price')
    elif sort == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-is_featured', '-created_at')
        
    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'selected_category_slug': category_slug,
        'q': q,
        'sort': sort,
    }
    return render(request, 'products.html', context)

def faq(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'faq.html', {'categories': categories})

