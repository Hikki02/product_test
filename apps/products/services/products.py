from django.http import JsonResponse

from apps.products.models import Product
from services.base.services import BaseService


class CreateProductService(BaseService):
    """
    Service for creating products.
    """
    model = Product


class UpdateProductService(BaseService):
    """
    Service for updating products.
    """
    model = Product


class DeleteProductService(BaseService):
    """
    Service for deleting products.
    """
    model = Product


class ListProductService(BaseService):
    """
    Service for listing products.
    """
    model = Product


class RetrieveProductService(BaseService):
    """
    Service for retrieve product.
    """
    model = Product


class ProductService:
    def __init__(self,
                 create_service: CreateProductService,
                 update_service: UpdateProductService,
                 delete_service: DeleteProductService,
                 list_service: ListProductService,
                 retrieve_service: RetrieveProductService,
                 ):
        self.create_service = create_service
        self.update_service = update_service
        self.delete_service = delete_service
        self.list_service = list_service
        self.retrieve_service = retrieve_service

    def create_product(self, **kwargs) -> Product:
        return self.create_service.create(**kwargs)

    def update_product(self, product_id: int, **kwargs) -> Product:
        return self.update_service.update(product_id, **kwargs)

    def delete_product(self, product_id: int) -> JsonResponse:
        return self.delete_service.delete(product_id)

    def list_products(self):
        return self.list_service.get_all()

    def retrieve_product(self, product_id: int):
        return self.retrieve_service.get_by_id(product_id)
