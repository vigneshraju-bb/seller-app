from django.db import models

class Seller(models.Model):

	seller_id		= models.AutoField(primary_key=True)
	seller_name		= models.CharField(max_length=250,null=True)
	seller_address	= models.TextField(null=True)
	seller_mobile 	= models.CharField(max_length=100)
	seller_otp	 	= models.CharField(max_length=50)
	seller_status	= models.SmallIntegerField(default=1)
	seller_created_on = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.seller_name
	class Meta:
		db_table = "tbl_seller"
		ordering = ['seller_name']
		
class Customer(models.Model):
	
	cust_id			= models.AutoField(primary_key=True)
	cust_name		= models.CharField(max_length=250,null=True)
	cust_address	= models.TextField(null=True)
	cust_mobile 	= models.CharField(max_length=100)
	cust_otp	 	= models.CharField(max_length=50)
	cust_status		= models.SmallIntegerField(default=1)
	cust_created_on = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.cust_name
	class Meta:
		db_table = "tbl_customer"
		ordering = ['cust_name']
		