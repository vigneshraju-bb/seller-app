from django.shortcuts import render
from .models import Seller,Customer
from .serializers import SellerSerializer,CustomerSerializer
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
import datetime
import jwt

class SellerGetOtp(APIView):
	def post(self, request):
		
		if request.data['mobile']:
			seller_info = Seller.objects.filter(seller_mobile = request.data['mobile'])
			if seller_info:
				otp = random.randint(0,20000)
				seller_info.update(seller_otp=otp)
			else:
				otp = random.randint(0,20000)
				Seller.objects.create(seller_mobile = request.data['mobile'],seller_otp=otp)
			return Response({"otp":otp})
		else:
			return Response({"Error":'Please enter valid mobile number'},status = status.HTTP_404_NOT_FOUND)
			
class SellerVerifyOtp(APIView):
	def post(self, request):
		if request.data['mobile'] == "" and request.data['otp'] == "":
			return_data = {
								"Mobile":"Error:Please enter mobile number",
								"Otp":"Error:Please enter otp "
						}
			return Response(return_data)
		else:
			if request.data['mobile'] == "":
				return Response({"Mobile":'Error : Please enter valid mobile number'},status = status.HTTP_404_NOT_FOUND)
			elif request.data['otp'] == "":
				return Response({"Otp":'Error : Please enter valid otp'},status = status.HTTP_404_NOT_FOUND)
			else:
				try:
					seller_data = Seller.objects.get(seller_mobile = request.data['mobile'],seller_otp = request.data['otp'])
				except:
					return Response({"Otp":'Error : Please enter valid otp'},status = status.HTTP_404_NOT_FOUND)
				
				payload ={
							"id":seller_data.seller_id,
							"exp":datetime.datetime.now() + datetime.timedelta(minutes=60),
							"iat":datetime.datetime.now()
				}
				token = jwt.encode(payload, 'secret', algorithm='HS256')
				
				response = Response()
				response.set_cookie(key='jwt_token', value=token, httponly=True)
				response.data={
								"jwt_token":token 
				}
				
				return response
				
class SellerAPIView(APIView):

	def get(self, request):
		try:
			token = request.COOKIES.get("jwt_token")
		except:
			return Response({"Error":"Unauthenticated!"},status = status.HTTP_404_NOT_FOUND)
			
		if not token:
			return Response({"Error":"Unauthenticated!"},status = status.HTTP_404_NOT_FOUND)
	
		try:
			payload = jwt.decode(token, "secret", algorithms=["HS256"])
		except:
			return Response({"Error":"Unauthenticated!"},status = status.HTTP_404_NOT_FOUND)

		seller_info = Seller.objects.get(seller_id = payload['id'])
		
		serializer = SellerSerializer(seller_info)
		return_data= {
						"seller_id":serializer.data["seller_id"],
						"seller_name":serializer.data["seller_name"],
						"seller_address":serializer.data["seller_address"],
						"seller_mobile":serializer.data["seller_mobile"],
		}
		return Response(return_data)
	def put(self, request):
		try:
			token = request.COOKIES.get("jwt_token")
		except:
			return Response({"Error":"Unauthenticated!"},status = status.HTTP_404_NOT_FOUND)
			
		if not token:
			return Response({"Error":"Unauthenticated!"},status = status.HTTP_404_NOT_FOUND)
	
		try:
			payload = jwt.decode(token, "secret", algorithms=["HS256"])
		except:
			return Response({"Error":"Unauthenticated!"},status = status.HTTP_404_NOT_FOUND)

		seller_data = Seller.objects.get(seller_id = payload['id'])
		
		if seller_data:
			if Seller.objects.filter(seller_mobile = request.data['seller_mobile']).exclude(seller_id=seller_data.seller_id):
				return Response({"Error":"Mobile number already exits!"},status = status.HTTP_404_NOT_FOUND) 
				
			serializer =  SellerSerializer(seller_data, data=request.data, partial=True)
			
			if serializer.is_valid():
				serializer.save()

				return_data = {
					"Message":"Profile updated successfully",
					"seller_id":serializer.data['seller_id']
				}
				return Response(return_data)
			
			return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)
		
class SellerLogoutApiView(APIView):
	def post(self, request):
		response = Response()
		response.delete_cookie("jwt_token")
		response.data ={
						"Message":"Seller Logout successfully"
		}
		return response
		
		
		

class CustomerGetOtp(APIView):
	def post(self, request):
		
		if request.data['mobile']:
			cust_info = Customer.objects.filter(cust_mobile = request.data['mobile'])
			if cust_info:
				otp = random.randint(0,20000)
				cust_info.update(cust_otp=otp)
			else:
				otp = random.randint(0,20000)
				Customer.objects.create(cust_mobile = request.data['mobile'],cust_otp=otp)
			return Response({"otp":otp})
		else:
			return Response({"Error":'Please enter valid mobile number'},status = status.HTTP_404_NOT_FOUND)
			
class CustomerVerifyOtp(APIView):
	def post(self, request):
		if request.data['mobile'] == "" and request.data['otp'] == "":
			return_data = {
								"Mobile":"Error:Please enter mobile number",
								"Otp":"Error:Please enter otp "
						}
			return Response(return_data)
		else:
			if request.data['mobile'] == "":
				return Response({"Mobile":'Error : Please enter valid mobile number'},status = status.HTTP_404_NOT_FOUND)
			elif request.data['otp'] == "":
				return Response({"Otp":'Error : Please enter valid otp'},status = status.HTTP_404_NOT_FOUND)
			else:
				try:
					cust_data = Customer.objects.get(cust_mobile = request.data['mobile'],cust_otp = request.data['otp'])
				except:
					return Response({"Otp":'Error : Please enter valid otp'},status = status.HTTP_404_NOT_FOUND)
				
				payload ={
							"id":cust_data.cust_id,
							"exp":datetime.datetime.now() + datetime.timedelta(minutes=60),
							"iat":datetime.datetime.now()
				}
				token = jwt.encode(payload, 'secret', algorithm='HS256')
				
				response = Response()
				response.set_cookie(key='jwt_token', value=token, httponly=True)
				response.data={
								"jwt_token":token 
				}
				
				return response
				
class CustomerAPIView(APIView):

	def get(self, request):
		try:
			token = request.COOKIES.get("jwt_token")
		except:
			return Response({"Error":"Unauthenticated!"},status = status.HTTP_404_NOT_FOUND)
			
		if not token:
			return Response({"Error":"Unauthenticated!"},status = status.HTTP_404_NOT_FOUND)
	
		try:
			payload = jwt.decode(token, "secret", algorithms=["HS256"])
		except:
			return Response({"Error":"Unauthenticated!"},status = status.HTTP_404_NOT_FOUND)

		cust_info = Customer.objects.get(cust_id = payload['id'])
		
		serializer = CustomerSerializer(cust_info)
		return_data= {
						"cust_id":serializer.data["cust_id"],
						"cust_name":serializer.data["cust_name"],
						"cust_address":serializer.data["cust_address"],
						"cust_mobile":serializer.data["cust_mobile"],
		}
		return Response(return_data)
	def put(self, request):
		try:
			token = request.COOKIES.get("jwt_token")
		except:
			return Response({"Error":"Unauthenticated!"},status = status.HTTP_404_NOT_FOUND)
			
		if not token:
			return Response({"Error":"Unauthenticated!"},status = status.HTTP_404_NOT_FOUND)
	
		try:
			payload = jwt.decode(token, "secret", algorithms=["HS256"])
		except:
			return Response({"Error":"Unauthenticated!"},status = status.HTTP_404_NOT_FOUND)

		cust_data = Customer.objects.get(cust_id = payload['id'])
		
		if cust_data:
			if Customer.objects.filter(seller_mobile = request.data['seller_mobile']).exclude(cust_id=cust_data.cust_id):
				return Response({"Error":"Mobile number already exits!"},status = status.HTTP_404_NOT_FOUND) 
				
			serializer =  CustomerSerializer(cust_data, data=request.data, partial=True)
			
			if serializer.is_valid():
				serializer.save()

				return_data = {
					"Message":"Profile updated successfully",
					"cust_id":serializer.data['cust_id']
				}
				return Response(return_data)
			
			return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)
		
class CustomerLogoutApiView(APIView):
	
	def post(self, request):
		# print(request.COOKIES)
		response = Response()
		response.delete_cookie("jwt_token")
		response.data ={
						"Message":"Customer Logout successfully"
		}
		return response