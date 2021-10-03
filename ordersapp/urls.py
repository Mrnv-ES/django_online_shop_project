from django.urls import path
import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderList.as_view(), name='order_list'),
    path('create/', ordersapp.OrderCreate.as_view(), name='create'),
    path('update/<int:pk>/', ordersapp.OrderUpdate.as_view(), name='update'),
    path('forming/complete/<int:pk>/', ordersapp.proceeding_status, name='proceeding_status'),
    path('read/<int:pk>/', ordersapp.OrderDetail.as_view(), name='read'),
    path('delete/<int:pk>/', ordersapp.OrderDelete.as_view(), name='delete'),
]