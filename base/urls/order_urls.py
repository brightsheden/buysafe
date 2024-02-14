

from django.urls import path
from ..views import order_views as views

urlpatterns = [
    path('create-order/', views.creatOrder, name='create-order'),
    path('paid/<int:pk>/', views.OrderPaid, name='order-paid'),
    path('delivered/<int:pk>/', views.Order_delivered, name='order-delivered'),
    path('order/<int:pk>/', views.UpdateOrder, name='update-order'),
    path('myorder/', views.getUserOrder, name='userorder'),
    path('<int:pk>/', views.getOrderById, name='order details'),
]