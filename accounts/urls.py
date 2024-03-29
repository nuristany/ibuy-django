from django.urls import path
from .import views

app_name  ='accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout,name ='logout'),
    path('dashboard/', views.dashboard,name ='dashboard'),
    path('', views.dashboard,name ='dashboard'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    
   
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('resetpasswordV/<uidb64>/<token>/', views.resetpasswordV, name='resetpasswordV'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    
    path('my_orders/', views.my_orders, name='my_orders'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('changePassword/', views.changePassword, name='changePassword'),
    path('order_detail/<int:order_id>', views.order_detail, name='order_detail')


]

