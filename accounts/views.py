from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
	return render(request, 'main/dashboard.html')

def products(request):
	return render(request, 'products/products.html')

def customer(request):
	return render(request, 'customer/customer.html')