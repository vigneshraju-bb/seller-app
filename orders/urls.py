from django.urls import path
from .views import CreateOrderAPIView,OrderAPIView,OrderDetailAPIView,SellerOrderCreateApiView

urlpatterns = [
    path('create_order/',CreateOrderAPIView.as_view()),
    path('orders/',OrderAPIView.as_view()),
    path('order_details/<int:id>',OrderDetailAPIView.as_view()),
	
    path('seller_oreder_create/',SellerOrderCreateApiView.as_view()),
]
