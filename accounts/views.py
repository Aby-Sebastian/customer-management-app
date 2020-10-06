from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .form import OrderForm
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

def customer(request, pk):

	get_customer = Customer.objects.get(id=pk)
	orders = get_customer.order_set.all()
	order_count = orders.count()

	context = {'get_customer':get_customer, 'orders':orders, 'order_count':order_count}
	return render(request, 'customer/customer.html', context=context)

def createOrder(request):
	form = OrderForm()

	if request.method == 'POST':
		
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form':form}
	return render(request, 'order/order_form.html', context=context)

def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'order/order_form.html', context=context)

def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')
		
	context = {'item':order}
	return render(request, 'delete.html', context=context)