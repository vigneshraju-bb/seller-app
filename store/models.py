from django.db import models
from accounts.models import Seller

class Store(models.Model):

	store_id		= models.AutoField(primary_key=True)
	store_seller_id	= models.ForeignKey(Seller, on_delete=models.CASCADE)
	store_name		= models.CharField(max_length=100)
	store_address 	= models.TextField(null=True)
	store_link 		= models.CharField(max_length=250)
	status 			= models.SmallIntegerField()
	created_on 		= models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.store_name
	class Meta:
		db_table = "tbl_store"
		ordering = ['store_name']
		
