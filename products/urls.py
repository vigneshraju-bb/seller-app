from django.urls import path
from .views import ProductAPIView,ProductDetailAPIView

urlpatterns = [
    path('product/',ProductAPIView.as_view()),
    path('product_details/<str:link>',ProductDetailAPIView.as_view())
]
