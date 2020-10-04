from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def index(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	context = { 'orders':orders, 'customers':customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending }

	return render(request, 'dashboard/dashboard.html', context=context)

def products(request):
	products = Product.objects.all()
	return render(request, 'products/products.html', {'products':products})

def customer(request):
	return render(request, 'customer/customer.html')