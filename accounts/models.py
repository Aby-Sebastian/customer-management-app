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
	name=models.CharField(max_length=200, null=True)
	price=models.FloatField(null=True)
	category=models.CharField(max_length=200, null=True)
	description=models.TextField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True)