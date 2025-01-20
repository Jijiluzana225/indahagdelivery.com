from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Add URLs for different views
    path('', views.store_list, name='store_list'),  # List of all stores
    path('product/<int:id>/', views.product_detail, name='product_detail'),  # Product detail page
    path('store/<int:id>/', views.store_detail, name='store_detail'),  # Store detail page
    
    
    path('store/<int:id>/location/', views.store_location, name='store_location'),
    path('stores/location/', views.all_store_locations, name='all_store_locations'),
    
    path('register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),  # Add this line for the login view
    
    # path('', views.landing_page, name='landing_page'),   
    
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),    
    path('logout-confirmation/', views.logout_confirmation, name='logout-confirmation'),
    
    
    path('edit-profile/', views.edit_profile, name='edit_profile'),
     
    path('store/<int:store_id>/order/', views.store_products, name='store_products'),

    path('checkout/', views.proceed_to_checkout, name='checkout'),
    
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('dashboard_store/', views.store_dashboard, name='store_dashboard'),
    
    path('update_order_status/', views.update_order_status, name='update_order_status'),
    
    path('order/<int:order_id>/items/', views.order_items, name='order_items'),
    
    path('update-item/<int:item_id>/', views.update_item, name='update_item'),   
    path('delete-item/<int:item_id>/', views.delete_item, name='delete_item'),

    path('update-profile/', views.update_profile, name='update_profile'),
    
    path('edit-prices/', views.edit_prices, name='edit_prices'),
    
    path('update-open/', views.update_store_open, name='update_store_open'),


    
]
