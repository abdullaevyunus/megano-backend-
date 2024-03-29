from django.core.paginator import Paginator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from shopapp.models import Product, Category, Sales
from shopapp.serializers import ProductSerializer, CategorySerializer, SalesSerializer


class ProductListAPIView(APIView):
    """
    List of Products
    """

    @swagger_auto_schema(tags=['catalog'])
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({'items': serializer.data})


class PopularListAPIView(APIView):
    """
    Popular Products List
    """

    @swagger_auto_schema(tags=['catalog'])
    def get(self, request):
        popular_products = Product.objects.filter(rating__gte=4.5)
        serializer = ProductSerializer(popular_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LimitedListAPIview(APIView):
    """
    Limited Products List
    """

    @swagger_auto_schema(tags=['catalog'])
    def get(self, request):
        limited_products = Product.objects.filter(count__lt=10)
        serializer = ProductSerializer(limited_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryListAPIview(APIView):
    """
    List of Categories
    """

    @swagger_auto_schema(tags=['catalog'])
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class SalesAPIView(APIView):
    """
    Sales list
    """
    @swagger_auto_schema(tags=['catalog'])
    def get(self, request):
        sales = Sales.objects.all()
        paginator = Paginator(sales, 2)

        page_number = request.query_params.get('page', 1)
        current_page = int(page_number)


        sales_page = paginator.page(current_page)
        serializer = SalesSerializer(sales_page, many=True)

        response_data = {
            'items': serializer.data,
            'currentPage': sales_page.number,
            'lastPage': paginator.num_pages
        }

        return Response(response_data)

class BannersAPIView(APIView):
    """
    Banners
    """

    @swagger_auto_schema(tags=['catalog'])
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
