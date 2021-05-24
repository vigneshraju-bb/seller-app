from django.shortcuts import render
from .models import Products
from .serializers import ProductSerializer
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Count
import jwt

class ProductAPIView(APIView):

	parser_classes = [MultiPartParser,FormParser]
	def check_auth(self, request):
		if "jwt_token" in request.COOKIES:
			token = request.COOKIES.get("jwt_token")
			payload = jwt.decode(token, "secret", algorithms=["HS256"])
			login_id = payload['id']
			return login_id
		else:
			login_id=""
	def get(self, request):
		
		products = Products.objects.all()
		if products:
			serializer = ProductSerializer(products,many=True)
			return Response(serializer.data)
		else:
			return Response({"Error":'No data found'},status = status.HTTP_404_NOT_FOUND)
	
	def post(self, request, format=None):
		
		login_id= self.check_auth(request)
		if login_id:
		
			request.data["prd_status"]=1
			
			serializer = ProductSerializer(data=request.data)
			
			if serializer.is_valid():
			
				serializer.save()
				
				return_data = {
					"product_id":serializer.data['prd_id'],
					"product_name":serializer.data['prd_name'],
					"product_image":serializer.data['prd_img']
				}
				return Response(return_data, status = status.HTTP_201_CREATED)
				
			return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)
		else:
			return Response({"Error":'UnAuthenticated!'},status = status.HTTP_404_NOT_FOUND)
			
class ProductDetailAPIView(APIView):

	def check_auth(self, request):
		if "jwt_token" in request.COOKIES:
			token = request.COOKIES.get("jwt_token")
			payload = jwt.decode(token, "secret", algorithms=["HS256"])
			login_id = payload['id']
			return login_id
		else:
			login_id=""
			
	def get_prd_object(self, link):
			
		try:
			prd_info = Products.objects.filter(prd_store_link=link)
			# return_data = prd_info.values('prd_category','prd_name').annotate(prd_count=Count('prd_category')).order_by('prd_name')
			
			return prd_info
		except:
			return Response({"Error":'No data found'},status = status.HTTP_404_NOT_FOUND)
	def get_prd_object_by_id(self, id):
		
		try:
			return Products.objects.get(prd_id=id)
		except:
			return Response({"Error":'No data found'},status = status.HTTP_404_NOT_FOUND)
			
	def get(self, request, link):
		product_info = self.get_prd_object(link)
		# print(product_info)
		serializer = ProductSerializer(product_info, many=True)
		proiduct_val ={}
		# print(serializer.data)
		for val in serializer.data:
			
			temp_cat = val['prd_category']
			if temp_cat not in  proiduct_val:
				proiduct_val[temp_cat] = {}
				proiduct_val[temp_cat][val['prd_id']] ={
														"prd_name":val['prd_name'],
														"prd_mrp_price":val['prd_mrp_price'],
														"prd_sale_price":val['prd_sale_price'],
														"prd_img":val['prd_img'],
													} 
			else:
				proiduct_val[temp_cat][val['prd_id']] = {
														"prd_name":val['prd_name'],
														"prd_mrp_price":val['prd_mrp_price'],
														"prd_sale_price":val['prd_sale_price'],
														"prd_img":val['prd_img'],
													} 
					
			# print(proiduct_val)
		return Response(proiduct_val)
	
	def put(self, request, id):
	
		login_id= self.check_auth(request)
		if login_id:
			prd_data = self.get_prd_object_by_id(id)
			
			serializer =  ProductSerializer(prd_data, data=request.data, partial=True)
			
			if serializer.is_valid():
				serializer.save()
				
				return_data = {
					"product_id":serializer.data['prd_id'],
					"product_name":serializer.data['prd_name'],
					"product_image":serializer.data['prd_img']
				}
				return Response(return_data)
				
			return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)
		else:
			return Response({"Error":'UnAuthenticated!'},status = status.HTTP_404_NOT_FOUND)
			
	def delete(self, request, id):
		login_id= self.check_auth(request)
		if login_id:
			prd_info = self.get_prd_object_by_id(id)
			prd_info.delete()
			return Response(status = status.HTTP_204_NO_CONTENT)
		else:
			return Response({"Error":'UnAuthenticated!'},status = status.HTTP_404_NOT_FOUND)