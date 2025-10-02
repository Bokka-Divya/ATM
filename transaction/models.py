from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class Account(models.Model):
	name=models.CharField(max_length=50)
	email=models.EmailField(max_length=50)
	account_number=models.CharField(max_length=50,unique=True)
	pin=models.CharField(max_length=50)
	balance=models.FloatField(default=500)
	def __str__(self):
		return f"{self.name}-{self.balance}"
class Transaction_History(models.Model):
	account=models.ForeignKey(Account,on_delete=models.CASCADE)
	amount=models.CharField(max_length=50)
	date=models.DateField(auto_now_add=True)
	transaction_type=models.CharField(max_length=20)
	def __str__(self):
		return f"{self.transaction_type}-----{self.amount}-----{self.date}"
