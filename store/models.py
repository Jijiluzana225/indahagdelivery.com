from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.contrib.auth.models import User

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):    
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    type = models.ForeignKey(ProductType, related_name='products', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='products/')
    active = models.BooleanField(default=False)    


    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User  # Import User model



    
class Store(models.Model):
    name = models.CharField(max_length=255)
    barangay = models.CharField(max_length=100)
    address_line = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    facebook_page = models.URLField(null=True, blank=True)
    picture = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='store/')
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stores', null=True, blank=True)  # link to User
    open = models.BooleanField(default=False)
    delivery_fee =  models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    time_open= models.CharField(max_length=25, null=True)
    time_close= models.CharField(max_length=25, null=True)    
    def __str__(self):
        return self.name

class Item(models.Model):
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='items', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} at {self.store.name}"


class CustomerProfile(models.Model):
    name = models.CharField(max_length=100)
    facebook_page = models.URLField(null=True, blank=True)    
    phone_number = models.CharField(max_length=20, null=True, blank=True)    
    barangay = models.CharField(max_length=100, null=True, blank=True)
    address_line = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=100)
    profile_picture = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='customer/')
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer', null=True, blank=True)  # link to User
    
    def __str__(self):
        return f"{self.name}"

class DeliveryDriver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='delivery_driver', null=True, blank=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    license_number = models.CharField(max_length=50, unique=True)
    vehicle_type = models.CharField(
        max_length=20,
        choices=[
            ('Motorcycle', 'Motorcycle'),
            ('Bicycle', 'Bicycle'),
            ('Car', 'Car'),
            ('Tricycle', 'Tricycle'),
            ('Other', 'Other')
        ],
        default='Motorcycle'
    )
    vehicle_plate_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='drivers/',null=True, blank=True)
    is_available = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    current_location = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_deliveries = models.PositiveIntegerField(default=0)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.vehicle_type}"
    
    



from django.db import models
from django.contrib.auth.models import User  # assuming you're using Django's User model for customers

class Order(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Preparing', 'Preparing'),
            ('On the Way', 'On the Way'),
            ('Delivered', 'Delivered')
        ],
        default='Pending'
    )
    
    original_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Preparing', 'Preparing'), ('On the Way', 'On the Way'), ('Delivered', 'Delivered')], default='Pending', null=True,blank=True)
    money = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True, default=0)
    instructions=models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    assigned_to = models.ForeignKey(DeliveryDriver, null=True, on_delete=models.SET_NULL)
    
    
    def __str__(self):
        return f"Order {self.id} - {self.customer.username} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"

    

class FlatRate(models.Model):
    flat_rate_fee = models.DecimalField(max_digits=10, decimal_places=2, default=50.0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Flat Rate as of {self.updated_at}"


from django.utils import timezone

def default_local_date():
    return timezone.localtime(timezone.now()).date()

def default_local_time():
    return timezone.localtime(timezone.now()).time()

from django.conf import settings 

class SpecialRequest(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    driver = models.ForeignKey('DeliveryDriver', null=True, blank=True, on_delete=models.SET_NULL)
    request_text = models.TextField()
    date_requested = models.DateField(default=default_local_date)
    time_requested = models.TimeField(default=default_local_time)
    estimated_budget = models.DecimalField(max_digits=10, decimal_places=2)
    special_remarks = models.TextField(blank=True, null=True)
    driver_comment = models.TextField(blank=True, null=True)
    go_confirmed = models.BooleanField(default=False)
    flat_rate_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    tip = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.username} - {self.date_requested} {self.time_requested}"
