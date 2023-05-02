from . import views
from django.urls import path


urlpatterns = [

    path('', views.store, name= 'store'),
    path('catagory/<slug:catagory_slug>', views.store, name= 'products_by_catagory'),
    path('catagory/<slug:catagory_slug>/<slug:product_slug>/', views.product_detail, name= 'product_detail'),
    path('search/', views.search, name= 'search'),
    path('submitReview/<int:product_id>/', views.submitReview, name='submitReview' )
] 