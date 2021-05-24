from django.urls import path
from .views import StoreAPIView,StoreDetailAPIView

urlpatterns = [
    path('store/',StoreAPIView.as_view()),
    path('store_detail_view/<str:link>',StoreDetailAPIView.as_view()),
    path('store_details/<int:id>',StoreDetailAPIView.as_view()),
]
