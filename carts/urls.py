from . import views
from django.urls import path


urlpatterns = [
    path('', views.cart, name='cart'),
    path('addToCart/<int:product_id>/', views.addToCart, name='addToCart'),
    path('decrementCart/<int:product_id>/<int:cart_item_id>/', views.decrementCart, name='decrementCart'),
    path('removeCartItem/<int:product_id>/<int:cart_item_id>/', views.removeCartItem, name='removeCartItem'),
    
]