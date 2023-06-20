from django.shortcuts import get_list_or_404, get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Collection, Product
from .serializers import CollectionSerializer, ProductSerializer
from store import serializers


@api_view()
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True, context={"request": request})
    return Response(serializer.data)


@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product, context={"request": request})
    return Response(serializer.data)


@api_view()
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data)
