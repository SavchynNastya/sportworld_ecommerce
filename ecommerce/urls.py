from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
     path('login/', views.CustomLoginView.as_view(template_name='login.html'), name='login'),
     path('', views.landing_page, name='landing_page'),
     path('main/', views.main_page, name='main_page'),
     path('product/<int:item_id>/',views.product_page, name='product_page'),
     path('liked/', views.liked_items, name='liked_items'),
     path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),

     path('add-to-liked/<int:item_id>/', views.add_to_liked, name='add_to_liked'),
     path('delete-from-cart-session/<int:item_id>/', views.delete_from_cart_session, name='delete_from_cart_session'),
     path('delete-from-cart/<int:item_id>/', views.delete_from_cart, name='delete_from_cart'),
     path('increment-cart-item/<int:item_id>/',views.increment_cart_item, name='increment_cart_item'),
     path('decrement-cart-item/<int:item_id>/',views.decrement_cart_item, name='decrement_cart_item'),
     
     path('add-contact-number-to-profile/', views.add_contact_number_to_profile, name="add_contact_number"),
     path('form-order/', views.form_order, name="form_order"),
     path('cart/', views.cart, name='cart'),
     path('profile/', views.profile, name='profile'),
     path('registration-form/', views.CustomRegistrationView.as_view(template_name='register.html'), name='registration_form'),
    
     path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
     path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
          views.activate, name='activate'),
     path('password_reset/', views.reset_password, name='password_reset'),
     path('password-reset-confirm/<uidb64>/<token>/',
          views.reset_password_confirm, name='password_reset_confirm'),
     path('password-reset-complete/',
          views.reset_password_complete, name='password_reset_complete'),
]
