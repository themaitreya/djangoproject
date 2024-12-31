from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list_view, name = 'product_list'),
    path('create/', views.product_create_view, name = 'product_create'),
    path('<int:pk>/', views.product_detail_view, name = 'product_detail'),
    path('<int:pk>/update/', views.product_update_view, name = 'product_update'),
    path('<int:pk>/delete/', views.product_delete_view, name = 'product_delete'),
    path('<int:pk>/like/', views.product_like_view, name = 'product_like'),
]