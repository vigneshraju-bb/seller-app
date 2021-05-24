from django.urls import path
from .views import SellerAPIView,SellerGetOtp,SellerVerifyOtp,SellerLogoutApiView,CustomerGetOtp,CustomerVerifyOtp,CustomerAPIView,CustomerLogoutApiView

urlpatterns = [
    path('seller/generate_otp',SellerGetOtp.as_view()),
    path('seller/verify_otp',SellerVerifyOtp.as_view()),
    path('seller/',SellerAPIView.as_view()),
    path('seller/logout',SellerLogoutApiView.as_view()),
	
	
	
    path('customer/generate_otp',CustomerGetOtp.as_view()),
    path('customer/verify_otp',CustomerVerifyOtp.as_view()),
    path('customer/',CustomerAPIView.as_view()),
    path('customer/logout',CustomerLogoutApiView.as_view()),
]
