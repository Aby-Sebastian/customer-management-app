from django.db import models

# Create your models here.

class Customer(models.Model):
	"""docstring for Customer"""
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=20, null=True)
	email = models.EmailField(null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.name

class Product(models.Model):

	CATEGORY = (
		('Indoor','Indoor'),
		('Out door','Out door')
		)
	name=models.CharField(max_length=200, null=True)
	price=models.FloatField(null=True)
	category=models.CharField(max_length=200, null=True, choices=CATEGORY)
	description=models.TextField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True)

class Order(models.Model):

	STATUS = (
		('Pending','Pending'),
		('Out for delivery','Out for delivery'),
		('Delivered','Delivered')
		)

	date_created = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)