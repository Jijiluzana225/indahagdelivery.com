from django.shortcuts import render
from .models import Store, Product

from django.shortcuts import render
from .models import ProductType, Store
from django.contrib.auth.decorators import login_required


@login_required
def store_list(request):
    product_type_id = request.GET.get('product_type', None)  # Get selected ProductType from the request
    product_types = ProductType.objects.all()  # Retrieve all ProductTypes
    stores = Store.objects.all()  # Default to all stores

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




from django.shortcuts import render, get_object_or_404
from .models import Store, Item

def store_products(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    items = Item.objects.filter(store=store).select_related('product')  # Fetch items for this store
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

@login_required
def proceed_to_checkout(request):
    if request.method == 'POST':
        store_id = request.POST.get('store_id')
        store = Store.objects.get(id=store_id)
        customer = request.user
        total_price = float(request.POST.get('total_price'))
        cart_items = request.POST.get('cart_items', '').split('|')  # Split by pipe

        # Create the order
        with transaction.atomic():
            order = Order.objects.create(
                store=store,
                customer=customer,
                total_price=total_price,
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
from .models import Order

@login_required
def customer_dashboard(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')  # Orders sorted by latest created_at
    return render(request, 'store/customer_dashboard.html', {'orders': orders})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from .models import Order, CustomerProfile

@login_required
def store_dashboard(request):
    if not request.user.is_staff:  # Ensure only the store owner can access
        return redirect('store_list')

    # Fetch customer profiles with their locations
    customer_profiles = CustomerProfile.objects.all()

    # Get orders for the store owned by the logged-in user
    orders = Order.objects.filter(store__owner=request.user).order_by('-created_at')

    # Add customer location directly to each order
    orders_with_location = []
    for order in orders:
        customer_profile = customer_profiles.get(username=order.customer)
        order.customer_location = customer_profile.location if customer_profile else "Location not available"
        order.customer_name = customer_profile.name
        orders_with_location.append(order)

    return render(request, 'store/store_dashboard.html', {
        'orders': orders_with_location,
    })




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, CustomerProfile
import json
import logging

# Set up a logger
logger = logging.getLogger(__name__)

@csrf_exempt
def update_order_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data['order_id']
            new_status = data['status']
            
            # Try to retrieve and update the order
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()

            # Retrieve the customer's location and name based on the order
            customer_profile = CustomerProfile.objects.get(username=order.customer)
            customer_location = customer_profile.location
            customer_name = customer_profile.name            

            # Return the success response along with the customer's location and name
            return JsonResponse({
                'status': 'success',
                'message': 'Order status updated successfully.',
                'customer_location': customer_location,  # Include location
                'customer_namex': customer_name  # Include name
                
            })
           
        
        except Order.DoesNotExist:
            logger.error(f"Order with ID {order_id} not found.")
            return JsonResponse({'status': 'error', 'message': 'Order not found.'}, status=404)
        
        except CustomerProfile.DoesNotExist:
            logger.error(f"Customer profile for Order ID {order_id} not found.")
            return JsonResponse({'status': 'error', 'message': 'Customer profile not found.'}, status=404)
        
        except KeyError as e:
            logger.error(f"Missing key: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f'Missing key: {str(e)}'}, status=400)
        
        except json.JSONDecodeError:
            logger.error("Invalid JSON format received.")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'}, status=400)
        
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)




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

