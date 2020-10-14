from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from .filters import OrderFilter
from .forms import OrderForm, CreateUserForm
from .models import *






def registerPage(request):

	if request.user.is_authenticated:
		return redirect('index')
	else:
		form = CreateUserForm()

		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, message='Account was created for ' + user)
				return redirect('login')

		context={"form":form,'test':'testing'}
		return render(request, 'user/register.html',context=context)


def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('index')
		else:
			messages.info(request, message='Username or Password is incorrect')
			return redirect('login')
	context = {}
	return render(request, 'user/login.html',context=context)


def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
def index(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	context = { 'orders':orders, 'customers':customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending }

	return render(request, 'dashboard/dashboard.html', context=context)

@login_required(login_url='login')
def products(request):
	products = Product.objects.all()
	return render(request, 'products/products.html', {'products':products})

@login_required(login_url='login')
def customer(request, pk):
	get_customer = Customer.objects.get(id=pk)
	orders = get_customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs

	context = {'get_customer':get_customer, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter}
	return render(request, 'customer/customer.html', context=context)

@login_required(login_url='login')
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

@login_required(login_url='login')
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


@login_required(login_url='login')
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'order/delete.html', context=context)


