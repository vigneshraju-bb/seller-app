from django.db import models
from products.models import Products
class Cart(models.Model):

	cart_id			= models.AutoField(primary_key=True)
	crt_order_id	= models.IntegerField(default=0)
	crt_user_id		= models.IntegerField(default=None)
	crt_token		= models.TextField(null=True)
	crt_prd_id		= models.ForeignKey(Products, on_delete=models.CASCADE)
	crt_prd_qty 	= models.IntegerField()
	crt_prd_price 	= models.FloatField()
	crt_prd_tot_price = models.FloatField()
	crt_prd_status 		= models.SmallIntegerField()
	crt_prd_created_on 	= models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.cart_id
	class Meta:
		db_table = "tbl_cart"
		ordering = ['crt_prd_created_on']
		
