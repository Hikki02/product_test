from django.contrib.postgres.search import SearchVector
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from Product.settings import ProductPagination
from apps.products.services.products import (
    CreateProductService,
    UpdateProductService,
    DeleteProductService,
    ListProductService,
    ProductService, RetrieveProductService,
)
from .filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer


def create_product_service() -> ProductService:
    create_service = CreateProductService()
    update_service = UpdateProductService()
    delete_service = DeleteProductService()
    list_service = ListProductService()
    retrieve_service = RetrieveProductService()
    return ProductService(create_service, update_service, delete_service, list_service, retrieve_service)


class ProductViewSet(viewsets.GenericViewSet):
    swagger_tags = ["Products"]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = ProductPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = create_product_service()

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.annotate(
                search=SearchVector('name', 'description')
            ).filter(search=search)

        return queryset

    @swagger_auto_schema(
        operation_description='Creates a new product with provided data.',
        request_body=ProductSerializer,
        responses={201: ProductSerializer(many=False)}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = self.product_service.create_service.create(**serializer.validated_data)
        return Response(self.serializer_class(product).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description='Updates product information with provided data.',
        request_body=ProductSerializer,
        responses={200: ProductSerializer(many=False)}
    )
    def update(self, request, pk=None, *args, **kwargs):
        product = self.product_service.update_service.get_by_id(pk)
        serializer = self.serializer_class(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_product = self.product_service.update_service.update(pk, **serializer.validated_data)
        return Response(self.serializer_class(updated_product).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description='Retrieves a list of all products.',
        responses={200: ProductSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description='Deletes a product by its ID. Only authenticated users can delete.',
        responses={204: 'Product deleted successfully.'}
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        self.product_service.delete_service.delete(pk)
        return Response({"message": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description='Retrieves a product by its ID.',
        responses={200: ProductSerializer(many=False)}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        product = self.product_service.retrieve_service.get_by_id(pk)
        serializer = self.serializer_class(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

