from django.shortcuts import render
from products.models import Products
from .models import Cart
from .serializers import CartSerializer
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Count
import random
import datetime
import jwt
from django.db.models import Q

class CartAPIView(APIView):
	def get_user_data(self, request):
		payload ={
					"id":0,
					"exp":datetime.datetime.now() + datetime.timedelta(minutes=60),
					"iat":datetime.datetime.now()
		}
		new_token = jwt.encode(payload, 'secret', algorithm='HS256')
		crt_user_id =0
		crt_token=""
		
		response = Response()
		# print(request.COOKIES)
		if "jwt_token" not in request.COOKIES and "temp_token" not in request.COOKIES:
			# print(new_token)
			# request.COOKIES[""]
			# response.set_cookie(key='temp_token', value=new_token, httponly=True)
			# crt_token=request.COOKIES.get("temp_token")
			response.data={'crt_user_id':crt_user_id,'crt_token':new_token}
			return response
			# return {'crt_user_id':crt_user_id,'crt_token':crt_token}
		else:
			if "jwt_token" in request.COOKIES:
				token = request.COOKIES.get("jwt_token")
				payload = jwt.decode(token, "secret", algorithms=["HS256"])
				crt_user_id = payload['id']
				
				# if "temp_token" in request.COOKIES:
					# temp_tok = request.COOKIES.get("temp_token")
					# Cart.objects.filter(crt_token=temp_tok).update(crt_user_id=crt_user_id,crt_token="")
					# response.delete_cookie("temp_token")
					
			elif "temp_token" in request.COOKIES:
				crt_token=request.COOKIES.get("temp_token")
		# print(crt_token)
		
			response.data={'crt_user_id':crt_user_id,'crt_token':crt_token}
			return response
		
	def get(self, request):
		
		user_data = self.get_user_data(request).data
		# print(request.COOKIES)
		
		if user_data['crt_user_id'] != 0:
			cart = Cart.objects.filter(crt_user_id=user_data['crt_user_id'],crt_prd_status=1)
		elif user_data['crt_token']:
			cart = Cart.objects.filter(crt_token=user_data['crt_token'],crt_prd_status=1)
		response = Response()
		# cart = Cart.objects.all()
		
		if user_data['crt_token']:
			response.set_cookie(key='temp_token', value=user_data['crt_token'], httponly=True)
		if cart:
			serializer = CartSerializer(cart,many=True)
			response.data = serializer.data
			return response
		else:
			return Response({"Error":'No data found'},status = status.HTTP_404_NOT_FOUND)
	
	def post(self, request):
		user_data = self.get_user_data(request).data
		request.data["crt_user_id"] =user_data['crt_user_id']
		if user_data['crt_token'] == "":
			request.data["crt_token"] =None
		else:
			request.data["crt_token"] = user_data['crt_token']
		if request.data["crt_prd_id"] == "" :
			return Response({"Error":'Invalid product data'},status = status.HTTP_404_NOT_FOUND)
		elif request.data["crt_prd_qty"] == "" :
			return Response({"Error":'Invalid product data'},status = status.HTTP_404_NOT_FOUND)
		else:
			# print("aa")
			try:
				product_data = Products.objects.get(prd_id = request.data["crt_prd_id"])
			except:
				return Response({"Error": 'Invalid product data'},status = status.HTTP_404_NOT_FOUND)
				
		if product_data:
			cart_check = Cart.objects.filter(Q(crt_user_id=user_data['crt_user_id']) | Q(crt_token=user_data['crt_token']))
			if cart_check.filter(crt_prd_id = request.data["crt_prd_id"],crt_prd_status=1).exists():
				return Response({"Error": 'Product already in cart	'},status = status.HTTP_404_NOT_FOUND)
			else:
				request.data["crt_prd_qty"] =request.data["crt_prd_qty"]
				request.data["crt_prd_tot_price"] = product_data.prd_sale_price * int(request.data["crt_prd_qty"])
				request.data["crt_prd_price"] = product_data.prd_sale_price
				request.data["crt_prd_status"] = 1
				# print(request.data)
				response = Response()
				serializer = CartSerializer(data=request.data)
			
				if serializer.is_valid():
				
					serializer.save()
					
					return_data = {
						"cart_id":serializer.data['cart_id'],
						"Message":"Product added to cart successfully"
					}
					if user_data['crt_token']:
						response.set_cookie(key='temp_token', value=user_data['crt_token'], httponly=True)
					response.data = return_data
					return response
					
				return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)
		else:
			return Response({"Error": 'Invalid product data'},status = status.HTTP_404_NOT_FOUND)
			
class CartDetailAPIView(APIView):	
	def get_cart_object(self, id):
		cart_data =""
		try:
			cart_data = Cart.objects.get(cart_id = id)
			return cart_data
		except:
			return cart_data
			
	def put(self, request, id):
		
		cart_info = self.get_cart_object(id)
		
		if cart_info:
			try:
				if request.data["crt_prd_qty"]:
					crt_prd_tot_price = cart_info.crt_prd_price * int(request.data["crt_prd_qty"])
					crt_prd_qty= request.data["crt_prd_qty"]
					
				Cart.objects.filter(cart_id=id).update(crt_prd_tot_price=crt_prd_tot_price,crt_prd_qty=crt_prd_qty)
			
				return_data = {
					"Message":"Cart updated successfully",
					"cart_id":id
				}
				return Response(return_data)
			except:
				return Response({"Error":'Empty or invalid data'},status = status.HTTP_404_NOT_FOUND)
		else:
			return Response({"Error":'No data found'},status = status.HTTP_404_NOT_FOUND)
			
	def delete(self, request, id):
		cart_data = self.get_cart_object(id)
		if cart_data:
			cart_data.delete()
			return Response(status = status.HTTP_204_NO_CONTENT)
		else:
			return Response({"Error":'No data found'},status = status.HTTP_404_NOT_FOUND)