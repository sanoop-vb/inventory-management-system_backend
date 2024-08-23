# products/urls.py

from django.urls import path
from .import views

urlpatterns = [

    path('products/',views.products,name='create-product'),
    path('products/add-stock/', views.add_stock, name='add-stock'),
    path('products/remove-stock/', views.remove_stock, name='remove-stock'),


]
