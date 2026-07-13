from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Enquiry
from dashboard.views import role_required
import csv
from openpyxl import Workbook
import datetime
import re

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_protect
def submit_enquiry(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        village = request.POST.get('location', '').strip()
        crop_type = request.POST.get('crop', '').strip()
        product_category = request.POST.get('category', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        errors = {}
        
        # Validation
        if not name or not re.match(r'^[A-Za-z ]{3,50}$', name):
            errors['name'] = "Please enter a valid name."
            
        if not phone or not re.match(r'^[6-9][0-9]{9}$', phone):
            errors['phone'] = "Please enter a valid 10-digit mobile number."
            
        if not email:
            errors['email'] = "Please enter a valid email address."
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors['email'] = "Please enter a valid email address."
                
        if not village or not re.match(r'^[A-Za-z \-,]+$', village):
            errors['location'] = "Please enter a valid village/location."
            
        if not crop_type:
            errors['crop'] = "Please select a crop type."
            
        if not product_category:
            errors['category'] = "Please select a product category."
            
        if not subject or not (5 <= len(subject) <= 100):
            errors['subject'] = "Subject must be between 5 and 100 characters."
            
        if not message or not (20 <= len(message) <= 1000):
            errors['message'] = "Message must be between 20 and 1000 characters."
            
        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)
            
        try:
            ip_address = get_client_ip(request)
            
            enquiry = Enquiry.objects.create(
                name=name,
                phone=phone,
                email=email,
                village=village,
                crop_type=crop_type,
                product_category=product_category,
                subject=subject,
                message=message,
                ip_address=ip_address
            )
            
            return JsonResponse({
                'success': True,
                'message': "Thank you! Your enquiry has been submitted successfully. Our team will contact you shortly."
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'errors': {'general': 'Unable to submit your enquiry. Please try again.'}}, status=500)
            
    return redirect('home')

@login_required
@role_required(['super_admin', 'admin', 'store_manager'])
def enquiry_list(request):
    enquiries = Enquiry.objects.all()
    
    query = request.GET.get('q')
    status = request.GET.get('status')
    
    if query:
        enquiries = enquiries.filter(
            Q(name__icontains=query) | 
            Q(phone__icontains=query) | 
            Q(message__icontains=query)
        )
    if status:
        enquiries = enquiries.filter(status=status)
        
    context = {
        'enquiries': enquiries,
        'query': query,
        'status_filter': status,
    }
    return render(request, 'dashboard/enquiries/list.html', context)

@login_required
@role_required(['super_admin', 'admin', 'store_manager'])
def enquiry_detail(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    return render(request, 'dashboard/enquiries/detail.html', {'enquiry': enquiry})

@login_required
@role_required(['super_admin', 'admin', 'store_manager'])
def enquiry_update_status(request, pk, status):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    if status in ['new', 'contacted', 'closed']:
        enquiry.status = status
        enquiry.save()
        messages.success(request, f"Enquiry status updated to {status.capitalize()}.")
    return redirect('enquiry_list')

@login_required
@role_required(['super_admin', 'admin', 'store_manager'])
def enquiry_delete(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    enquiry.delete()
    messages.success(request, "Enquiry deleted successfully.")
    return redirect('enquiry_list')

@login_required
@role_required(['super_admin', 'admin', 'store_manager'])
def export_enquiries(request, format_type):
    enquiries = Enquiry.objects.all()
    
    if format_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="enquiries_export.csv"'
        writer = csv.writer(response)
        writer.writerow(['Date', 'Name', 'Phone', 'Email', 'Village', 'Crop', 'Category', 'Subject', 'Message', 'Status'])
        for e in enquiries:
            writer.writerow([e.created_at.strftime('%Y-%m-%d %H:%M'), e.name, e.phone, e.email, e.village, e.crop_type, e.product_category, e.subject, e.message, e.get_status_display()])
        return response
        
    elif format_type == 'excel':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="enquiries_export.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = "Enquiries"
        ws.append(['Date', 'Name', 'Phone', 'Email', 'Village', 'Crop', 'Category', 'Subject', 'Message', 'Status'])
        for e in enquiries:
            ws.append([e.created_at.replace(tzinfo=None), e.name, e.phone, e.email, e.village, e.crop_type, e.product_category, e.subject, e.message, e.get_status_display()])
        wb.save(response)
        return response
        
    return redirect('enquiry_list')
