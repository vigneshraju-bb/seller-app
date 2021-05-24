from django.urls import path
from .views import CartAPIView,CartDetailAPIView

urlpatterns = [
    path('cart/',CartAPIView.as_view()),
    path('cart_details/<int:id>',CartDetailAPIView.as_view())
]
