from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .form import OrderForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
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

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs

	context = {'get_customer':get_customer, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter}
	return render(request, 'customer/customer.html', context=context)


def createOrder(request,pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
	customer = Customer.objects.get(id=pk)
	formSet = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	# form = OrderForm(initial={'customer':customer})

	if request.method == 'POST':
		
		# form = OrderForm(request.POST)
		formSet = OrderFormSet(request.POST,instance=customer)
		if formSet.is_valid():
			formSet.save()
			return redirect('/')
	context = {'formSet':formSet}
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