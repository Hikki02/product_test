from rest_framework import routers
from apps.products.views import ProductViewSet

# Create a router and register the ProductViewSet
product_router = routers.SimpleRouter()
product_router.register(r'products', ProductViewSet, basename='product')
