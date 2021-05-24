from django.db import models

class Products(models.Model):

	prd_id			= models.AutoField(primary_key=True)
	prd_name		= models.CharField(max_length=250)
	prd_category	= models.CharField(max_length=250)
	prd_mrp_price 	= models.FloatField(null=True)
	prd_sale_price 	= models.FloatField(null=True)
	prd_desc 		= models.TextField()
	prd_img 		= models.ImageField(upload_to ='uploads/')
	prd_store_link 	= models.CharField(max_length=100)
	prd_status 		= models.SmallIntegerField()
	prd_created_on 	= models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.prd_name
	class Meta:
		db_table = "tbl_product"
		ordering = ['prd_name']
		
