

# accounts/forms.py

from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    role = forms.ChoiceField(choices=[('customer', 'Customer'), ('store_owner', 'Store Owner')])

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data




from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomerProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



from django import forms
from .models import CustomerProfile

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = [
            'name', 'facebook_page', 'phone_number', 
            'barangay', 'address_line', 'location', 'profile_picture'
        ]


from django import forms
from .models import Store

class StoreOpenForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['open']
        widgets = {
            'open': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
        }


from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'type', 'description', 'price', 'picture', 'active']
        exclude = ['username']  # Exclude username since it's auto-assigned
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


from django import forms
from .models import OrderItem

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product_name', 'product_price', 'quantity']
        

from django import forms
from .models import DeliveryDriver

class DeliveryDriverRegistrationForm(forms.ModelForm):
    class Meta:
        model = DeliveryDriver
        fields = [
            'name', 'phone_number', 'license_number', 
            'vehicle_type', 'vehicle_plate_number', 
            'profile_picture', 'current_location'
        ]
        
        profile_picture = forms.ImageField(required=True, error_messages={'required': 'Profile picture is required.'})
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
                'maxlength': 100
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number',
                'maxlength': 20
            }),
            'license_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your license number',
                'maxlength': 50
            }),
            'vehicle_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'vehicle_plate_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter vehicle plate number',
                'maxlength': 20
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
          
            'current_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your current Address',
                'maxlength': 255
            }),
        }

    def clean_license_number(self):
        license_number = self.cleaned_data['license_number']
        if DeliveryDriver.objects.filter(license_number=license_number).exists():
            raise forms.ValidationError("A driver with this license number already exists.")
        return license_number

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        # Add phone number validation logic here if needed
        return phone_number
    
from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm

class DeliveryDriverLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))

# from django import forms
# from .models import SpecialRequest
# from django.utils import timezone
# from zoneinfo import ZoneInfo

# class SpecialRequestForm(forms.ModelForm):
#     class Meta:
#         model = SpecialRequest
#         fields = [
#             'request_text',         
#             'estimated_budget',
#             'special_remarks',
#             'tip',
#         ]
     

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)


from django import forms
from .models import SpecialRequest

class SpecialRequestForm(forms.ModelForm):
    class Meta:
        model = SpecialRequest
        fields = ['store', 'request_text', 'estimated_budget', 'tip']
        widgets = {
            'store': forms.Textarea(attrs={
                'class': 'form-control modern-textarea',
                'placeholder': 'Name of Store / Person',
                'rows': 2
            }),
            'request_text': forms.Textarea(attrs={
                'class': 'form-control modern-textarea narrow-textarea',
                'placeholder': 'List of items to buy / Details',
                'rows': 4
            }),
            'estimated_budget': forms.NumberInput(attrs={
                'class': 'form-control modern-input',
                'placeholder': 'e.g. 150.00'
            }),
            'tip': forms.NumberInput(attrs={
                'class': 'form-control modern-input',
                'placeholder': 'Optional tip'
            }),
        }
