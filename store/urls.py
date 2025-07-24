from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Add URLs for different views
    # path('', views.system_update, name='system_update'),  # List of all stores
    path('', views.system_update_close, name='system_update_close'),  # List of all stores
    # path('', views.landing_page, name='landing_page'),   
    # path('', views.system_update_close, name='system_update_close'),  # List of all stores
    
    path('', views.store_list, name='store_list'),  # List of all stores 
    path('product/<int:id>/', views.product_detail, name='product_detail'),  # Product detail page
    # path('store/<int:id>/', views.store_detail, name='store_detail'),  # Store detail page
    
    
    path('store/<int:id>/location/', views.store_location, name='store_location'),
    path('stores/location/', views.all_store_locations, name='all_store_locations'),
    
    path('register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),  # Add this line for the login view
    
    
    
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),    
    path('logout-confirmation/', views.logout_confirmation, name='logout-confirmation'),
    
    
    path('edit-profile/', views.edit_profile, name='edit_profile'),
     
    path('store/<int:store_id>/order/', views.store_products, name='store_products'),

    path('checkout/', views.proceed_to_checkout, name='checkout'),
    
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('dashboard_store/', views.store_dashboard, name='store_dashboard'),
    
    path('update_order_status/', views.update_order_status, name='update_order_status'),
    
    path('order/<int:order_id>/items/', views.order_items, name='order_items'),
    path('order/<int:order_id>/items_driver/', views.order_items_driver, name='order_items_driver'),
    
    path('update-item/<int:item_id>/', views.update_item, name='update_item'),   
    path('delete-item/<int:item_id>/', views.delete_item, name='delete_item'),

    path('update-profile/', views.update_profile, name='update_profile'),
    
    path('edit-prices/', views.edit_prices, name='edit_prices'),
    
    path('update-open/', views.update_store_open, name='update_store_open'),

    path('order/<int:order_id>/update-status/', views.update_order_status_delivered, name='update_order_status_delivered'),
    path('order/<int:order_id>/update-status_undelivered/', views.update_order_status_undelivered, name='update_order_status_undelivered'),
    
    path('check-new-orders/', views.check_new_orders, name='check_new_orders'),
    path('update-order-status/', views.update_order_status_original_Status, name='update_order_status_original_Status'),
    

# product CRUD
    path('list/', views.product_list, name='product_list'),
    path('add/', views.product_create, name='product_create'),
    path('<int:pk>/edit/', views.product_update, name='product_update'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    
    # update order_items_update
    
    path('orders/<int:order_id>/items_driver/', views.order_items_view_driver, name='order_items_update_driver'),
    path('orders/items/delete/<int:item_id>/', views.delete_order_item, name='delete_order_item'),

    path('driver/register/', views.driver_register, name='driver_register'),
    path('driver/dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('driver/profile/update/', views.driver_profile_update, name='driver_profile_update'),
    path('driver/toggle-availability/', views.toggle_availability, name='toggle_availability'),
    path('driver//', views.home, name='home_driver'),
    path('update_driver_status/', views.update_driver_status, name='update_driver_status'),
    
    
    path('login/', views.driver_login, name='driver_login'),
    
    path('special-request-dashboard/', views.special_requests_dashboard, name='special_requests_dashboard'),    
    path('special-request-detail/<int:pk>/', views.special_request_detail, name='special_request_detail'),    
    path('special-request/', views.special_request, name='special_request'),

    path('special-request-edit/<int:pk>/', views.edit_special_request, name='edit_special_request'),

    path('special-request/<int:pk>/assign/', views.assign_driver, name='assign_driver'),
    path('update-delivery-status/<int:pk>/', views.update_delivery_status, name='update_delivery_status'),
    path('cancel-special-request/<int:request_id>/', views.cancel_special_request, name='cancel_special_request'),

        
    path('api/driver-updates/<int:driver_id>/', views.fetch_driver_updates, name='driver_updates')
    

]




    
