from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from dashboard.views_public import home, about, contact, products, faq
from accounts.views import user_login, user_logout
from dashboard.views import dashboard_home
from categories.views import category_list, category_add, category_edit, category_delete
from products.views import product_list, product_add, product_edit, product_delete, product_delete_image, export_products, import_products
from enquiries.views import submit_enquiry, enquiry_list, enquiry_detail, enquiry_update_status, enquiry_delete, export_enquiries
from accounts.views_mgmt import profile_edit, user_list, user_add, user_edit, user_delete

urlpatterns = [
    # Public views
    path('', home, name='home'),
    path('sitemap.xml', TemplateView.as_view(template_name='sitemap.xml', content_type='text/xml')),
    path('llms.txt', TemplateView.as_view(template_name='llms.txt', content_type='text/plain')),
    path('about.html', about, name='about'),
    path('contact.html', contact, name='contact'),
    path('products.html', products, name='products'),
    path('faq.html', faq, name='faq'),
    path('login.html', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    
    # SEO Slugs
    path('best-agricultural-products-supplier-in-nandyal/', home),
    path('leading-agriculture-products-company-in-nandyal/', about),
    
    path('agricultural-fertilizers-supplier-in-nandyal/', products, {'category_slug': 'fertilizers'}),
    path('agricultural-insecticides-supplier-in-nandyal/', products, {'category_slug': 'insecticides'}),
    path('agricultural-fungicides-supplier-in-nandyal/', products, {'category_slug': 'fungicides'}),
    path('agricultural-herbicides-supplier-in-nandyal/', products, {'category_slug': 'herbicides'}),
    path('agricultural-micronutrients-supplier-in-nandyal/', products, {'category_slug': 'micronutrients'}),
    path('agricultural-bio-fertilizers-supplier-in-nandyal/', products, {'category_slug': 'bio-fertilizers'}),
    path('agricultural-seeds-supplier-in-nandyal/', products, {'category_slug': 'seeds'}),

    # Contact Form endpoint
    path('submit-enquiry/', submit_enquiry, name='submit_enquiry'),
    
    # Dashboard Views
    path('dashboard/', dashboard_home, name='dashboard_home'),
    
    # Categories CRUD
    path('dashboard/categories/', category_list, name='category_list'),
    path('dashboard/categories/add/', category_add, name='category_add'),
    path('dashboard/categories/edit/<int:pk>/', category_edit, name='category_edit'),
    path('dashboard/categories/delete/<int:pk>/', category_delete, name='category_delete'),
    
    # Products CRUD
    path('dashboard/products/', product_list, name='product_list'),
    path('dashboard/products/add/', product_add, name='product_add'),
    path('dashboard/products/edit/<int:pk>/', product_edit, name='product_edit'),
    path('dashboard/products/delete/<int:pk>/', product_delete, name='product_delete'),
    path('dashboard/products/delete-image/<int:img_id>/', product_delete_image, name='product_delete_image'),
    path('dashboard/products/export/<str:format_type>/', export_products, name='export_products'),
    path('dashboard/products/import/', import_products, name='import_products'),
    
    # Enquiries Management
    path('dashboard/enquiries/', enquiry_list, name='enquiry_list'),
    path('dashboard/enquiries/<int:pk>/', enquiry_detail, name='enquiry_detail'),
    path('dashboard/enquiries/<int:pk>/status/<str:status>/', enquiry_update_status, name='enquiry_update_status'),
    path('dashboard/enquiries/delete/<int:pk>/', enquiry_delete, name='enquiry_delete'),
    path('dashboard/enquiries/export/<str:format_type>/', export_enquiries, name='export_enquiries'),
    
    # User / Profile Management
    path('dashboard/profile/', profile_edit, name='profile_edit'),
    path('dashboard/users/', user_list, name='user_list'),
    path('dashboard/users/add/', user_add, name='user_add'),
    path('dashboard/users/edit/<int:pk>/', user_edit, name='user_edit'),
    path('dashboard/users/delete/<int:pk>/', user_delete, name='user_delete'),
]

# Static & Media URL Handling (handled at routing level in debug mode)
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
