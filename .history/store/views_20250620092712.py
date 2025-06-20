from django.shortcuts import render
from .models import Store, Product

from django.shortcuts import render
from .models import ProductType, Store
from django.contrib.auth.decorators import login_required


@login_required
def store_list(request):
    product_type_id = request.GET.get('product_type', None)  # Get selected ProductType from the request
    product_types = ProductType.objects.all()  # Retrieve all ProductTypes
    stores = Store.objects.all().order_by('name')

    if product_type_id:
        # Filter stores that have items with products of the selected ProductType
        stores = stores.filter(items__product__type_id=product_type_id).distinct()

    return render(request, 'store/store_list.html', {
        'product_types': product_types,
        'stores': stores,
        'selected_product_type': int(product_type_id) if product_type_id else None,
    })
    
    

# View for product detail page
def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'store/product_detail.html', {'product': product})

# View for store detail page
def store_detail(request, id):
    store = Store.objects.get(id=id)    
    return render(request, 'store/store_detail.html', {'store': store})




from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Store

@login_required
def store_location(request, id):
    # Get the store instance by ID
    store = Store.objects.get(id=id)

    # Pass only the store's location to the template
    return render(request, 'store/store_location.html', {'store': store})



from django.shortcuts import render
from .models import Store

def all_store_locations(request):
    # Get all stores from the database
    stores = Store.objects.all()

    # Pass the stores to the template
    return render(request, 'store/all_store_locations.html', {'stores': stores})





# accounts/views.py

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('store_list')  # Change to the desired redirect
    else:
        form = AuthenticationForm()

    return render(request, 'store/login.html', {'form': form})




from django.shortcuts import render

@login_required
def landing_page(request):
    return render(request, 'store/base.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm, CustomerProfileForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = CustomerProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user
            user = user_form.save()
            # Save the profile and link it to the user
            profile = profile_form.save(commit=False)
            profile.username = user
            profile.save()
            # Log the user in
            login(request, user)
            return redirect('store_list')  # Redirect to your home or success page
    else:
        user_form = UserRegistrationForm()
        profile_form = CustomerProfileForm()
    return render(request, 'store/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CustomerProfile

@login_required
def profile_view(request):
    # Access the logged-in user
    user = request.user
    
    # Get the associated CustomerProfile instance
    try:
        customer_profile = user.username  # This assumes your User model is linked to CustomerProfile using a OneToOneField
        
        profile_picture_url = customer_profile.profile_picture.url  # Get the URL of the profile picture
    except CustomerProfile.DoesNotExist:       
        profile_picture_url = None  # In case there's no profile picture or CustomerProfile

    return render(request, 'store/base.html', {'profile_picture_url': profile_picture_url})


def logout_confirmation(request):
    return render(request, 'login.html')

from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    next_page = 'login'  # Redirect to home page after logout




# from django.shortcuts import render, get_object_or_404
# from .models import Store, Item

# def store_products(request, store_id):
#     store = get_object_or_404(Store, id=store_id)
#     items = Item.objects.filter(store=store).select_related('product')  # Fetch items for this store
#     return render(request, 'store/store_products.html', {'store': store, 'items': items})

from django.shortcuts import render, get_object_or_404
from .models import Store, Item

def store_products(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    # Filter items for the store and ensure product.active is False
    items = Item.objects.filter(store=store, product__active=False).select_related('product').order_by('product__name')
    return render(request, 'store/store_products.html', {'store': store, 'items': items})





from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomerProfileForm
from .models import CustomerProfile

@login_required
def edit_profile(request):
    profile = request.user.customer
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Adjust the redirect as needed
    else:
        form = CustomerProfileForm(instance=profile)
    return render(request, 'store/edit_profile.html', {'form': form})

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Store
from django.db import transaction
from decimal import Decimal

@login_required
def proceed_to_checkout(request):
    if request.method == 'POST':
        store_id = request.POST.get('store_id')
        store = Store.objects.get(id=store_id)
        customer = request.user
        total_price = float(request.POST.get('total_price'))
        cart_items = request.POST.get('cart_items', '').split('|')  # Split by pipe
        
        # Retrieve the money and instructions from the POST data
        money = request.POST.get('money')  # Allow None or blank values
        instructions = request.POST.get('instructions', '')  # Default to empty string if not provided

        # Create the order
        with transaction.atomic():
            order = Order.objects.create(
                store=store,
                customer=customer,
                total_price=total_price,
                money=money if money else None,  # Store None if money is blank
                instructions=instructions,  # Save the instructions value
                status='Pending'
            )

            # Add items to the order
            for item in cart_items:
                # Split each item by commas to get name, price, quantity
                product_name, product_price, quantity = item.split(",")
                OrderItem.objects.create(
                    order=order,
                    product_name=product_name,
                    product_price=float(product_price),
                    quantity=int(quantity)  # Now quantity should be a valid integer
                )

            # Return success response
            return JsonResponse({'success': True, 'order_id': order.id})
        
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


from django.shortcuts import render
from django.db.models import Sum, F
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def customer_dashboard(request):
    # Fetch orders for the logged-in customer and annotate them with the total_amount (sum of product_price * quantity)
    orders = Order.objects.filter(customer=request.user).annotate(
        total_amount=Sum(F('items__product_price') * F('items__quantity'))
    ).order_by('-created_at')  # Orders sorted by latest created_at
    
    # Track status changes
    status_changes = []
    for order in orders:
        # Assuming there's an 'original_status' field that tracks the status when the order was created
        if order.status != order.original_status:
            status_changes.append(order.id)  # Add order id to the status changes list
    
    # Pass the orders and the status changes to the template
    return render(request, 'store/customer_dashboard.html', {
        'orders': orders,
        'status_changes': status_changes  # Pass status_changes to template for notifications
    })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from .models import Order, CustomerProfile, DeliveryDriver

from django.db.models import Sum, F
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def store_dashboard(request):
 
    # Fetch customer profiles with their locations
    customer_profiles = CustomerProfile.objects.all()

    # Get orders for the store owned by the logged-in user
    orders = Order.objects.filter(store__owner=request.user).annotate(
        total_amount=Sum(F('items__product_price') * F('items__quantity'))
    ).order_by('-created_at')

    available_drivers = DeliveryDriver.objects.filter(is_available=True)
    
    context = {
        'orders': orders,  # your existing orders
        'available_drivers': available_drivers,
        # ... other context variables
    }
    # Add customer location directly to each order
    orders_with_location = []
    for order in orders:
        customer_profile = customer_profiles.get(username=order.customer)
        order.customer_location = customer_profile.location if customer_profile else "Location not available"
        order.customer_name = customer_profile.name
        order.phone_number = customer_profile.phone_number
        orders_with_location.append(order)

    return render(request, 'store/store_dashboard.html', {
        'orders': orders_with_location
    }, context)



import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["POST"])
def update_order_status(request):
    """
    Update order status and/or assign driver
    """
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        status = data.get('status')
        driver_id = data.get('driver_id')
        
        # Get the order
        order = Order.objects.get(id=order_id)
        
        # Update status if provided
        if status:
            order.status = status
        
        # Update driver assignment if provided
        if driver_id:
            try:
                driver = DeliveryDriver.objects.get(id=driver_id, is_available=True)
                order.assigned_to = driver
            except DeliveryDriver.DoesNotExist:
                return JsonResponse({'error': 'Driver not found or not available'}, status=400)
        
        order.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Order updated successfully'
        })
        
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem

def order_items(request, order_id):
    order = get_object_or_404(Order, id=order_id)
   
    
    items = order.items.all()  # Fetch related items using the related_name
    
    for item in items:
        item.total_price = item.product_price * item.quantity
    
    return render(request, 'store/order_items.html', {'order': order, 'items': items, 'item.total_price':item.total_price})


from django.http import JsonResponse

def update_item(request, item_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        item = get_object_or_404(OrderItem, id=item_id)
        item.quantity = data.get('quantity', item.quantity)
        item.save()
        return JsonResponse({'message': 'Item updated successfully!'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def delete_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(OrderItem, id=item_id)
        item.delete()
        return JsonResponse({'message': 'Item deleted successfully!'})
    return JsonResponse({'error': 'Invalid request'}, status=400)



# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomerProfileForm
from .models import CustomerProfile

@login_required
def update_profile(request):
    try:
        # Try to get the customer profile for the logged-in user
        profile = CustomerProfile.objects.get(username=request.user)
    except CustomerProfile.DoesNotExist:
        # If no profile exists, create a new one
        profile = None

    if request.method == 'POST':
        if profile:
            form = CustomerProfileForm(request.POST, request.FILES, instance=profile)
        else:
            form = CustomerProfileForm(request.POST, request.FILES)

        if form.is_valid():
            customer_profile = form.save(commit=False)
            customer_profile.username = request.user  # Assign the logged-in user to the profile
            customer_profile.save()
            return redirect('store_list')  # Replace with your success URL

    else:
        if profile:
            form = CustomerProfileForm(instance=profile)
            # Extract latitude and longitude from the location (comma-separated)
            location_parts = profile.location.split(',')
            lat = float(location_parts[0]) if len(location_parts) > 0 else 0
            lng = float(location_parts[1]) if len(location_parts) > 1 else 0
        else:
            form = CustomerProfileForm()
            lat = 0  # Default latitude
            lng = 0  # Default longitude

    return render(request, 'store/update_profile.html', {'form': form, 'lat': lat, 'lng': lng})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Item, Product

@login_required
def edit_prices(request):
    # Get the logged-in user's store
    store = request.user.stores  # This assumes `related_name='stores'` for the Store model's owner field

    # Retrieve all items associated with the user's store
    items = Item.objects.filter(store=store)

    if request.method == "POST":
        for item in items:
            # Update price
            price_field_name = f"price_{item.product.id}"
            if price_field_name in request.POST:
                try:
                    new_price = float(request.POST[price_field_name])
                    item.product.price = new_price
                except ValueError:
                    pass  # Ignore invalid inputs

            # Update active status
            active_field_name = f"active_{item.product.id}"
            # Checkbox logic: assign True if the checkbox is present, False otherwise
            item.product.active = active_field_name in request.POST

            # Save the updated product
            item.product.save()

        return redirect('edit_prices')  # Refresh the page

    # Pass the items to the template
    return render(request, 'store/store_edit_price.html', {'items': items})





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Store
from .forms import StoreOpenForm

@login_required
def update_store_open(request):
    # Get the store related to the logged-in user
    store = get_object_or_404(Store, owner=request.user)

    if request.method == 'POST':
        form = StoreOpenForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            return redirect('store_dashboard')  # Replace with the name of your dashboard view
    else:
        form = StoreOpenForm(instance=store)

    return render(request, 'store/update_open.html', {'form': form, 'store': store})



from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Product

@login_required
def product_list(request):
    # Filter products by the logged-in user
    products = Product.objects.filter(username=request.user).order_by('name')
   
    return render(request, 'store/product_list.html', {'products': products})



from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from .forms import ProductForm
from django.contrib import messages

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)  # Don't save to the database yet
            product.username = request.user  # Assign the logged-in user
            product.save()  # Save the product

            # Add a success message
            messages.success(request, 'Added New Product!')
            return redirect('product_create')
    else:
        form = ProductForm()

    return render(request, 'store/product_form.html', {'form': form, 'title': 'Add Product'})




def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/product_form.html', {'form': form, 'title': 'Edit Product', 'product': product})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'store/product_confirm_delete.html', {'product': product})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Order

def update_order_status_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if order.status != 'Delivered':  # Only allow status change if it's not already "Delivered"
        order.status = 'Delivered'
        order.save()

    return redirect('store_dashboard')



from django.http import JsonResponse
from .models import Order

def check_new_orders(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    try:
        store = request.user.stores  # Assuming a store owner has only one store
    except Store.DoesNotExist:
        return JsonResponse({"error": "No store found for this user"}, status=404)

    # Retrieve or initialize order count in session
    initial_order_count = request.session.get('initial_order_count', None)
    
    if initial_order_count is None:
        initial_order_count = Order.objects.filter(store=store).count()
        request.session['initial_order_count'] = initial_order_count

    # Get the current total order count
    current_order_count = Order.objects.filter(store=store).count()
    
    # Check if new orders exist
    new_orders = current_order_count - initial_order_count
    active = new_orders > 0

    # Update the session only if notification is pressed
    if active and request.GET.get("notification_pressed") == "true":
        request.session['initial_order_count'] = current_order_count

    return JsonResponse({
        "initial_order_count": initial_order_count,
        "current_order_count": current_order_count,
        "new_orders": new_orders,
        "active": active
    })


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order

@csrf_exempt  # This is required if you're using fetch with CSRF
def update_order_status_original_Status(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body
            data = json.loads(request.body)
            order_id = data.get('order_id')

            # Get the order by ID
            order = Order.objects.get(id=order_id)

            # Update the original status to match the current status
            order.original_status = order.status
            order.save()

            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Order, OrderItem, Product, Store
from .forms import OrderItemForm

@login_required
def order_items_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    items = order.items.all()
    products = Product.objects.filter(username=request.user)  # Only store owner's products

    if request.method == "POST":
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.save()
            return redirect('order_items_update', order_id=order.id)
    else:
        form = OrderItemForm()

    return render(request, 'store/order_items_update.html', {
        'order': order,
        'items': items,
        'products': products,
        'form': form
    })

@login_required
def delete_order_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__store__owner=request.user)
    item.delete()
    return redirect('order_items', order_id=item.order.id)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from .models import DeliveryDriver
from .forms import DeliveryDriverRegistrationForm

def home(request):
    """Home page view"""
    return render(request, 'store/home.html')

@login_required
def driver_register(request):
    """Driver registration view"""
    # Check if user already has a driver profile
    if hasattr(request.user, 'delivery_driver'):
        messages.info(request, 'You are already registered as a delivery driver.')
        return redirect('driver_dashboard')
    
    if request.method == 'POST':
        form = DeliveryDriverRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                driver = form.save(commit=False)
                driver.user = request.user
                driver.save()
                
                messages.success(request, 
                    'Your delivery driver registration has been submitted successfully! '
                    'You will be notified once your account is verified.'
                )
                return redirect('driver_dashboard')
            except ValidationError as e:
                messages.error(request, f'Registration failed: {e}')
            except Exception as e:
                messages.error(request, 'An error occurred during registration. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DeliveryDriverRegistrationForm()
    
    return render(request, 'store/driver_register.html', {'form': form})

@login_required
def driver_dashboard(request):
    """Driver dashboard view"""
    try:
        driver = request.user.delivery_driver
    except DeliveryDriver.DoesNotExist:
        messages.error(request, 'You are not registered as a delivery driver.')
        return redirect('driver_register')
    
    context = {
        'driver': driver,
        'recent_deliveries': [],  # Add logic to get recent deliveries
    }
    return render(request, 'store/driver_dashboard.html', context)

@login_required
def driver_profile_update(request):
    """Update driver profile"""
    try:
        driver = request.user.delivery_driver
    except DeliveryDriver.DoesNotExist:
        messages.error(request, 'You are not registered as a delivery driver.')
        return redirect('driver_register')
    
    if request.method == 'POST':
        form = DeliveryDriverRegistrationForm(request.POST, request.FILES, instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('driver_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DeliveryDriverRegistrationForm(instance=driver)
    
    return render(request, 'store/driver_profile_update.html', {'form': form, 'driver': driver})

@login_required
@require_http_methods(["POST"])
def toggle_availability(request):
    """Toggle driver availability status"""
    try:
        driver = request.user.delivery_driver
        driver.is_available = not driver.is_available
        driver.save()
        
        status = "available" if driver.is_available else "unavailable"
        return JsonResponse({
            'success': True, 
            'status': status,
            'message': f'You are now {status} for deliveries.'
        })
    except DeliveryDriver.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'message': 'Driver profile not found.'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': 'An error occurred while updating availability.'
        }, status=500)