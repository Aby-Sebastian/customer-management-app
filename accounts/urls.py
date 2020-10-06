from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('customer/<str:pk>/', views.customer, name='customer'),
	path('products/', views.products, name='products'),
	
	path('create_order/', views.createOrder, name='create_order'),
	path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
	path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
]