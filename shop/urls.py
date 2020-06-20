from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="shop"),
    path('detail/<int:myid>', views.product_details, name="detail"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('checkdb/', views.checkdb, name="checkdb"),
    path('contact/', views.contact, name="contact"),
    path('track/', views.track, name="track"),
    path('receipt/<str:orderid>', views.receipt, name="receipt"),
    path('handlerequest/', views.handlerequest, name="Handlerequest"),
]