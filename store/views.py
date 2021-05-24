from django.shortcuts import render
from .models import Store
from .serializers import StoreSerializer
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.permissions import IsAuthenticated
import jwt

class StoreAPIView(APIView):
	def check_auth(self, request):
		if "jwt_token" in request.COOKIES:
			token = request.COOKIES.get("jwt_token")
			payload = jwt.decode(token, "secret", algorithms=["HS256"])
			login_id = payload['id']
			return login_id
		else:
			login_id=""
			
	def get(self, request):
		
		login_id= self.check_auth(request)
		if login_id:
			store = Store.objects.filter(store_seller_id = login_id)
			if store:
				serializer = StoreSerializer(store,many=True)
				
				return Response(serializer.data)
			else:
				return Response({"Error":'No data found'},status = status.HTTP_404_NOT_FOUND)
		else:
			return Response({"Error":'UnAuthenticated!'},status = status.HTTP_404_NOT_FOUND)
			
	def post(self, request):
	
		login_id= self.check_auth(request)
		if login_id:
			temp_store_name = request.data['store_name'].strip()
			request.data['store_id'] =""
			request.data['store_name'] = request.data['store_name'].strip()
			
			if Store.objects.filter(store_name=request.data['store_name']).exists():
				return Response({"Error":'Store already exist'},status = status.HTTP_404_NOT_FOUND)
				
			request.data['store_link'] = temp_store_name.replace(" ","_")
			request.data['status'] = 1
			request.data['store_seller_id'] = login_id
			
			serializer = StoreSerializer(data=request.data)
			
			if serializer.is_valid():
			
				serializer.save()
				
				return_data = {
					"store_id":serializer.data['store_id'],
					"store_link":request.get_host()+'/store_detail_view/'+temp_store_name.replace(" ","_")
				}
				return Response(return_data, status = status.HTTP_201_CREATED)
				
			return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)
		else:
			return Response({"Error":'UnAuthenticated!'},status = status.HTTP_404_NOT_FOUND)
			
class StoreDetailAPIView(APIView):	
	def check_auth(self, request):
		if "jwt_token" in request.COOKIES:
			token = request.COOKIES.get("jwt_token")
			payload = jwt.decode(token, "secret", algorithms=["HS256"])
			login_id = payload['id']
			return login_id
		else:
			login_id=""
	def get_store_object(self, link):
		try:
			return Store.objects.get(store_link=link)
		except:
			return Response({"Error":'No data found'},status = status.HTTP_404_NOT_FOUND)
	def get_store_object_by_id(self, id):
		
		try:
			return Store.objects.get(store_id=id)
		except Store.DoesNotExits:
			return Response({"Error":'No data found'},status = status.HTTP_404_NOT_FOUND)
			
	def get(self, request, link):
		Store = self.get_store_object(link)
		serializer = StoreSerializer(Store)
		return_data = {
				"store_id":serializer.data['store_id'],
				"store_name":serializer.data['store_name'],
				"store_address":serializer.data['store_address']
			}
		return Response(return_data)
	
	def put(self, request, id):
		login_id= self.check_auth(request)
		if login_id:
			store_data = self.get_store_object_by_id(id)
			
			new_store_name = request.data['store_name']
			request.data['store_link'] = new_store_name.replace(" ","_")
			if Store.objects.filter(store_name=new_store_name).exclude(store_id=id):
				return Response({"Error":'Store already exist'},status = status.HTTP_404_NOT_FOUND)
			
			serializer =  StoreSerializer(store_data, data=request.data, partial=True)
			
			if serializer.is_valid():
				serializer.save()
				
				return_data = {
					"store_id":serializer.data['store_id'],
					"store_link":request.get_host()+'/store_detail_view/'+request.data['store_link']
				}
				return Response(return_data)
				
			return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)
			
		else:
			return Response({"Error":'UnAuthenticated!'},status = status.HTTP_404_NOT_FOUND)
			
	def delete(self, request, id):
		login_id= self.check_auth(request)
		if login_id:
			Store = self.get_store_object_by_id(id)
			Store.delete()
			return Response(status = status.HTTP_204_NO_CONTENT)
		else:
			return Response({"Error":'UnAuthenticated!'},status = status.HTTP_404_NOT_FOUND)
		