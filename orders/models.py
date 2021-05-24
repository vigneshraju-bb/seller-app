from django.db import models

class Orders(models.Model):

	ord_id			= models.AutoField(primary_key=True)
	ord_customer_id	= models.IntegerField(default=0)
	ord_total_amt	= models.FloatField(default=None)
	ord_status		= models.SmallIntegerField(default=0)
	ord_created_on 	= models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.cart_id
	class Meta:
		db_table = "tbl_orders"
		ordering = ['ord_created_on']
		
