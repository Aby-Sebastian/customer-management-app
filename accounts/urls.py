from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('customer/', views.customer, name='customer'),
	path('products/', views.products, name='products'),
]