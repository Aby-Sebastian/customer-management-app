from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .filters import OrderFilter
from .forms import OrderForm, CreateUserForm, CustomerForm, CreateProductForm, CreateTagForm
from .models import *
from .decorators import unauthenticated_user, allowed_users, admin_only





@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')


			messages.success(request, message='Account was created for ' + username)
			return redirect('login')

	context={"form":form,'test':'testing'}
	return render(request, 'main/register.html',context=context)


@unauthenticated_user
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
	return render(request, 'main/login.html',context=context)


def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
@admin_only
def index(request):
	orders = Order.objects.all().order_by('-id')
	customers = Customer.objects.all()
	last_5_orders = orders[:5]

	total_customers = customers.count()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	context = { 'orders':last_5_orders, 'customers':customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending }

	return render(request, 'dashboard/dashboard.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()
	return render(request, 'products/products.html', {'products':products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
	get_customer = Customer.objects.get(id=pk)
	orders = get_customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs

	context = {'get_customer':get_customer, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter}
	return render(request, 'customer/customer.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	
	context = {'orders':orders, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
	return render(request, 'user/user.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()

	context = {'form': form}
	return render(request, 'account_settings.html', context=context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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

	context = {'form':formSet}
	return render(request, 'order/order_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'order/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'order/delete.html', context=context)


# create and delete product pages

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createProduct(request):
	form = CreateProductForm()
	tag = CreateTagForm()

	if request.method == 'POST':
		form = CreateProductForm(request.POST)
		tag = CreateTagForm(request.POST)
		if tag.is_valid() and form.is_valid():
			tag.save()
			form.save()

	context = {'form':form, 'tag':tag}
	return render(request, 'products/add_products.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteProduct(request, pk):
	product = Product.objects.get(id=pk)
	if request.method == 'POST':
		product.delete()
		return redirect('/')

	context = {'item': product}
	return render(request, 'products/delete_product.html', context=context)