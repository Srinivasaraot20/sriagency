import os
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from io import BytesIO
from categories.models import Category
from PIL import Image

def validate_product_image(image_file):
    if not image_file:
        return
    # Limit file size to 5 MB
    if image_file.size > 5 * 1024 * 1024:
        raise ValidationError("File size exceeds 5 MB limit.")
    # Validate extension
    ext = os.path.splitext(image_file.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.webp']:
        raise ValidationError("Unsupported image format. Allowed formats: jpg, jpeg, png, webp.")

class Product(models.Model):
    STOCK_STATUS_CHOICES = (
        ('in_stock', 'In Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('low_stock', 'Low Stock'),
    )

    # Basic Info
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.CharField(max_length=100, blank=True, null=True)
    product_type = models.CharField(max_length=100, blank=True, null=True) # e.g. Nitrogen Fertilizer
    suitable_crops = models.CharField(max_length=255, blank=True, null=True)

    # Descriptions
    short_description = models.TextField(blank=True, null=True)
    full_description = models.TextField(blank=True, null=True)
    features = models.TextField(blank=True, null=True, help_text="One per line or paragraph")
    benefits = models.TextField(blank=True, null=True)
    usage_instructions = models.TextField(blank=True, null=True)

    # Pricing
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Inventory
    sku = models.CharField(max_length=50, unique=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    stock_status = models.CharField(max_length=20, choices=STOCK_STATUS_CHOICES, default='in_stock')
    availability = models.BooleanField(default=True)

    # Status
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Images
    main_image = models.ImageField(upload_to='products/main/', validators=[validate_product_image])
    
    # Required Database Columns (added for compatibility and inspection)
    product_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='products/thumbnails/', blank=True, null=True)
    image = models.ImageField(upload_to='products/main/', blank=True, null=True, validators=[validate_product_image])
    gallery_images = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    # SEO
    meta_title = models.CharField(max_length=150, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    seo_keywords = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        # Delete main image file
        if self.main_image and os.path.exists(self.main_image.path):
            try:
                os.remove(self.main_image.path)
            except Exception:
                pass
        # Delete image file
        if self.image and os.path.exists(self.image.path):
            try:
                os.remove(self.image.path)
            except Exception:
                pass
        # Delete thumbnail file
        if self.thumbnail and os.path.exists(self.thumbnail.path):
            try:
                os.remove(self.thumbnail.path)
            except Exception:
                pass
        # Delete gallery images
        for img in self.gallery.all():
            if img.image and os.path.exists(img.image.path):
                try:
                    os.remove(img.image.path)
                except Exception:
                    pass
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Sync required fields with existing fields
        self.product_name = self.name
        self.description = self.full_description or self.short_description
        self.price = self.selling_price
        self.stock = self.stock_quantity
        self.status = self.is_active
        self.featured = self.is_featured

        if self.image and self.main_image != self.image:
            self.main_image = self.image
        elif self.main_image and self.image != self.main_image:
            self.image = self.main_image

        # Auto calculate stock status if quantity is updated
        try:
            qty = int(self.stock_quantity)
        except (TypeError, ValueError):
            qty = 0

        if qty == 0:
            self.stock_status = 'out_of_stock'
        elif qty <= 5:
            self.stock_status = 'low_stock'
        else:
            self.stock_status = 'in_stock'

        # Check for image change to delete old files
        if self.pk:
            try:
                old_instance = Product.objects.get(pk=self.pk)
                if old_instance.main_image and self.main_image != old_instance.main_image:
                    if os.path.exists(old_instance.main_image.path):
                        os.remove(old_instance.main_image.path)
                if old_instance.image and self.image != old_instance.image:
                    if os.path.exists(old_instance.image.path):
                        os.remove(old_instance.image.path)
                if old_instance.thumbnail and self.thumbnail != old_instance.thumbnail:
                    if os.path.exists(old_instance.thumbnail.path):
                        os.remove(old_instance.thumbnail.path)
            except Exception:
                pass

        # Auto-generate thumbnail from main image if uploaded
        if self.image and (not self.thumbnail or (self.pk and Product.objects.get(pk=self.pk).image != self.image)):
            try:
                self.image.open()
                img = Image.open(self.image)
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                img.thumbnail((200, 200))
                temp_thumb = BytesIO()
                img.save(temp_thumb, format='JPEG', quality=85)
                temp_thumb.seek(0)
                
                thumb_name = os.path.basename(self.image.name)
                thumb_base, _ = os.path.splitext(thumb_name)
                self.thumbnail.save(f'{thumb_base}_thumb.jpg', ContentFile(temp_thumb.read()), save=False)
            except Exception as e:
                print("Error generating thumbnail:", e)

        super().save(*args, **kwargs)

        # Optimize Main Image
        if self.main_image:
            try:
                img_path = self.main_image.path
                img = Image.open(img_path)
                if img.width > 800 or img.height > 800:
                    img.thumbnail((800, 800))
                    img.save(img_path, quality=85, optimize=True)
            except Exception:
                pass

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='products/gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.image and os.path.exists(self.image.path):
            try:
                os.remove(self.image.path)
            except Exception:
                pass
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Check for image change to delete old files
        if self.pk:
            try:
                old_instance = ProductImage.objects.get(pk=self.pk)
                if old_instance.image and self.image != old_instance.image:
                    if os.path.exists(old_instance.image.path):
                        os.remove(old_instance.image.path)
            except Exception:
                pass

        super().save(*args, **kwargs)
        if self.image:
            try:
                img_path = self.image.path
                img = Image.open(img_path)
                if img.width > 800 or img.height > 800:
                    img.thumbnail((800, 800))
                    img.save(img_path, quality=85, optimize=True)
            except Exception:
                pass
