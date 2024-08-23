from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Products
from .serializers import ProductSerializer

@api_view(['GET','POST','DELETE'])
def products(request):
    if request.method == 'GET':
        product = Products.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    else:
        data = request.data
        obj = Products.objects.get(id = data['id'])
        obj.delete()
        return Response({"Message" : "Product Deleted"})


@api_view(['POST'])
def add_stock(request):
    data = request.data
    product_id = data.get('ProductID')
    stock_change = data.get('StockChange')

    try:
        product = Products.objects.get(ProductID=product_id)
        product.TotalStock += stock_change
        product.save()
        return Response({"Message": "Stock added successfully"}, status=status.HTTP_200_OK)
    except Products.DoesNotExist:
        return Response({"Error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def remove_stock(request):
    data = request.data
    product_id = data.get('ProductID')
    stock_change = data.get('StockChange')

    try:
        product = Products.objects.get(ProductID=product_id)
        if product.TotalStock >= stock_change:
            product.TotalStock -= stock_change
            product.save()
            return Response({"Message": "Stock removed successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"Error": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)
    except Products.DoesNotExist:
        return Response({"Error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)