from django.db import models

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(ProductType, related_name='products', on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='products/')

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
    picture = models.ImageField(upload_to='stores/')
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stores', null=True, blank=True)  # link to User

    def __str__(self):
        return self.name

class Item(models.Model):
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='items', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"{self.product.name} at {self.store.name}"


class CustomerProfile(models.Model):
    name = models.CharField(max_length=100)
    facebook_page = models.URLField(null=True, blank=True)    
    phone_number = models.CharField(max_length=20, null=True, blank=True)    
    barangay = models.CharField(max_length=100, null=True, blank=True)
    address_line = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='customers/')
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer', null=True, blank=True)  # link to User
    
    def __str__(self):
        return f"{self.name}"



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
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.id} - {self.customer.username} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"

class Om(models.Model):
        product_name = models.CharField(max_length=255)
    