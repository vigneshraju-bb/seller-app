from django.shortcuts import render
from products.models import Products
from cart.models import Cart
from cart.serializers import CartSerializer
from accounts.models import Customer
from accounts.serializers import CustomerSerializer
from .models import Orders
from .serializers import OrderSerializer
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
import datetime
import jwt
from django.db.models import Q

class CreateOrderAPIView(APIView):
	
	def post(self, request):
		
		if "jwt_token" in request.COOKIES:
			token = request.COOKIES.get("jwt_token")
			payload = jwt.decode(token, "secret", algorithms=["HS256"])
			crt_user_id = payload['id']
			cart_data = Cart.objects.filter(crt_user_id=crt_user_id,crt_prd_status=1)
			if cart_data:
				cart_ids=[]
				total_cart_amt=0
				for cart_val in cart_data:
					cart_ids.append(cart_val.cart_id)
					total_cart_amt += cart_val.crt_prd_tot_price
				data={"ord_customer_id":crt_user_id,"ord_total_amt":total_cart_amt}	
				serializer=OrderSerializer(data=data)
				if serializer.is_valid():
					serializer.save()
					if cart_ids:
						Cart.objects.filter(cart_id__in=cart_ids).update(crt_user_id=crt_user_id,crt_order_id=serializer.data["ord_id"],crt_prd_status=2)
						
				return Response({"Order id":serializer.data["ord_id"],"Message":"Order placed successfully"})			
			else:
				return Response({"Error":'No data found'},status = status.HTTP_404_NOT_FOUND)
		elif "temp_token" in request.COOKIES:
			response = Response()
			crt_token=request.COOKIES.get("temp_token")
			if "cus_mobile" in request.data:
				if Customer.objects.filter(cust_mobile=request.data["cus_mobile"]).exists():
					try:
						customer_id=Customer.objects.get(cust_mobile=request.data["cus_mobile"]).cust_id
						
						payload ={
							"id":customer_id,
							"exp":datetime.datetime.now() + datetime.timedelta(minutes=60),
							"iat":datetime.datetime.now()
						}
						token = jwt.encode(payload, 'secret', algorithm='HS256')
						
						
						response.set_cookie(key='jwt_token', value=token, httponly=True)
						# response.data={
										# "jwt_token":token 
						# }
					except:
						customer_id=""
				else:
					serializer = CustomerSerializer(data=request.data)
					if serializer.is_valid():
						serializer.save()
						customer_id = serializer.data['cust_id']
						
						payload ={
							"id":customer_id,
							"exp":datetime.datetime.now() + datetime.timedelta(minutes=60),
							"iat":datetime.datetime.now()
						}
						token = jwt.encode(payload, 'secret', algorithm='HS256')
						
						
						response.set_cookie(key='jwt_token', value=token, httponly=True)
						# response.data={
										# "jwt_token":token 
						# }
					else:
						return Response({"Error":'while customer data create'},status = status.HTTP_404_NOT_FOUND)
						
				if customer_id:
					
					cart_data = Cart.objects.filter(crt_token=crt_token,crt_prd_status=1)
					
					if cart_data:
						cart_ids=[]
						total_cart_amt=0
						for cart_val in cart_data:
							cart_ids.append(cart_val.cart_id)
							total_cart_amt += cart_val.crt_prd_tot_price
						data={"ord_customer_id":customer_id,"ord_total_amt":total_cart_amt}	
						serializer=OrderSerializer(data=data)
						if serializer.is_valid():
							serializer.save()
							if cart_ids:
								Cart.objects.filter(cart_id__in=cart_ids).update(crt_user_id=customer_id,crt_order_id=serializer.data["ord_id"],crt_prd_status=2)
								
							response.delete_cookie("temp_token")
							response.data={"Order id":serializer.data["ord_id"],"Message":"Order placed successfully"}
							return response
						else:
							return Response({"Error":'while order create'},status = status.HTTP_404_NOT_FOUND)
					else:
						return Response({"Error":'No data found'},status = status.HTTP_404_NOT_FOUND)
				else:
					return Response({"Error":'Invalid customer data'},status = status.HTTP_404_NOT_FOUND)
			else:
				return Response({"Error":'Please enter mobile number'},status = status.HTTP_404_NOT_FOUND)
			
		else:
			return Response({"Error":'No data found'},status = status.HTTP_404_NOT_FOUND)

class OrderAPIView(APIView):
	def get(self, request):
		if "jwt_token" in request.COOKIES:
			token = request.COOKIES.get("jwt_token")
			payload = jwt.decode(token, "secret", algorithms=["HS256"])
			crt_user_id = payload['id']
			order_data = Orders.objects.filter(ord_customer_id=crt_user_id)
			if order_data:
				serializer = OrderSerializer(order_data,many=True)
				return Response(serializer.data)
			else:
				return Response({"Error":'No orders found!'},status = status.HTTP_404_NOT_FOUND)
		else:
			return Response({"Error":'UnAuthenticated!'},status = status.HTTP_404_NOT_FOUND)
			
class OrderDetailAPIView(APIView):	
	def get_order_object(self, id):
		
		order_data =""
		try:
			order_data = Orders.objects.get(ord_id = id)
			return order_data
		except:
			return order_data
			
	def put(self, request, id):
		if "jwt_token" in request.COOKIES:
			order_info = self.get_order_object(id)
			
			if order_info:
				try:
					Orders.objects.filter(ord_id = id).update(ord_status=request.data["ord_status"])
				
					return_data = {
						"Message":"Order status updated successfully",
						"order_id":id
					}
					return Response(return_data)
				except:
					return Response({"Error":'Empty or invalid status'},status = status.HTTP_404_NOT_FOUND)
			else:
				return Response({"Error":'No data found'},status = status.HTTP_404_NOT_FOUND)
		else:
			return Response({"Error":'UnAuthenticated!'},status = status.HTTP_404_NOT_FOUND)
	def get(self, request, id):
		if "jwt_token" in request.COOKIES:
			order_info = self.get_order_object(id)
			if order_info:
				order_items = Cart.objects.filter(crt_order_id=order_info.ord_id)
				if order_items:
					serializer = CartSerializer(order_items, many=True)
					return Response(serializer.data)
						
				else:
					return Response({"Error":'No data found'},status = status.HTTP_404_NOT_FOUND)
			else:
				return Response({"Error":'Invalid order id'},status = status.HTTP_404_NOT_FOUND)
				
		else:
			return Response({"Error":'UnAuthenticated!'},status = status.HTTP_404_NOT_FOUND)
	def delete(self, request, id):
		if "jwt_token" in request.COOKIES:
			order_info = self.get_order_object(id)
			if order_info:
				order_info.delete()
				return Response(status = status.HTTP_204_NO_CONTENT)
			else:
				return Response({"Error":'No data found'},status = status.HTTP_404_NOT_FOUND)
		else:
			return Response({"Error":'UnAuthenticated!'},status = status.HTTP_404_NOT_FOUND)	
			
class SellerOrderCreateApiView(APIView):
	def post(self, request):
		if "jwt_token" in request.COOKIES:
			if "cust_mobile" in request.data and "cust_name" in request.data:
				customer_id=""
				if Customer.objects.filter(cust_mobile =request.data["cust_mobile"] ).exists():
					try:
						customer_id = Customer.objects.get(cust_mobile=request.data["cust_mobile"]).cust_id
					except:
						customer_id=""
				else:
					otp = random.randint(0,20000)
					Customer.objects.create(cust_mobile = request.data['cust_mobile'],cust_otp=otp,cust_address= request.data['cust_address'])
					customer_id =Customer.objects.latest('cust_id')
				if customer_id:
					if "order_data" in request.data:
						order_data = request.data["order_data"]
						prd_ids=[]
						temp_ord_data={}
						for order_info in order_data:
							if order_info["prd_id"] not in prd_ids:
								prd_ids.append(order_info["prd_id"])
								temp_ord_data[order_info["prd_id"]]= order_info["prd_qty"]
						if prd_ids:
							prd_details = Products.objects.filter(prd_id__in = prd_ids)
							temp_prd_data={}
							if prd_details:
								for prd_val in prd_details:
									temp_prd_data[prd_val.prd_id]=prd_val
							create_data={}
							autoinc=1
							order_total=0
							for key,val in temp_prd_data.items():
								qty=0
								total=0
								qty = temp_ord_data[key]
								total = qty*val.prd_sale_price
								
								create_data[autoinc]={
									"crt_user_id":customer_id,
									"crt_prd_id":int(key),
									"crt_prd_qty":qty,
									"crt_prd_price":val.prd_sale_price,
									"crt_prd_tot_price":total,
									"crt_prd_status":1
								}
								order_total +=total
								autoinc +=1
							serializer = OrderSerializer(data={"ord_customer_id":customer_id,"ord_total_amt":order_total,"ord_status":1})
							if serializer.is_valid():
								serializer.save()
							
							# order_info = Orders.objects.create(ord_customer_id = customer_id,ord_total_amt=order_total,ord_status=1)
							# print(serializer.data["ord_id"])
							ord_id = serializer.data["ord_id"]
							# print(ord_id)
							cart_val_list=[]
							for key, val in create_data.items():
								
								serializer = CartSerializer(data=val)
								if serializer.is_valid():
									serializer.save()
								else:
									return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)
								# form_info = Cart(crt_order_id=ord_id,crt_user_id=val["crt_user_id"],crt_prd_id_id=val["crt_prd_id"],crt_prd_qty=val["crt_prd_qty"],crt_prd_price=val["crt_prd_price"],crt_prd_tot_price=val["crt_prd_tot_price"],crt_prd_status=2)
								# cart_val_list.append(form_info)
							return Response({"Message":"Order placed successfully!","order id":ord_id})
							# print(cart_val_list)
							# if cart_val_list:
								# try:
									# Cart.objects.bulk_create(cart_val_list)
									# return Response({"Message":"Order placed successfully!","order id":ord_id})
								# except:
									# return Response({"Error":'Cart order creations!'},status = status.HTTP_404_NOT_FOUND)
							
						else:
							return Response({"Error":'Product details are mandatory!'},status = status.HTTP_404_NOT_FOUND)
						
					else:
						return Response({"Error":'Product details are mandatory!'},status = status.HTTP_404_NOT_FOUND)
				else:
					return Response({"Error":'Invalid customer details!'},status = status.HTTP_404_NOT_FOUND)
			else:
				return Response({"Error":'Customer information is mandatory!'},status = status.HTTP_404_NOT_FOUND)
				
		else:
			
			return Response({"Error":'UnAuthenticated!'},status = status.HTTP_404_NOT_FOUND)
		
		