from django.urls import path
from .views import *


urlpatterns = [
    path('',Landing_Page,name='landing'),
    path('home/',Index_Page,name='index'),
    path('shop/',Shop_Page,name='shop'),
    path('detail/<str:slug>/',Detail_Page,name='detail'),
    path('cart/',CartFlow,name='cart'),
    path('signup/',Signup_Page,name='signup'),
    path('login/',Login_Page,name='login'),
    path('logout/',Logout_Page,name='logout'),
    path('search/',Search_Page,name='search'),
    path('create/',Create_Page,name='create'),
    path('add-to-cart/<str:slug>/',Add_to_cart,name='add_to_cart'),
    path('remove-from-cart/<str:slug>/',Remove_from_cart,name='remove_from_cart'),
    path('checkout-session/<str:session>',Create_Checkout_session,name='checkout_session'),
    path('user-dashboard/',User_Dashboard,name='user_dashboard'),
    path('success/',Success_Page,name='success'),
    path('cancel/',Cancel_Page,name='cancel'),


]
