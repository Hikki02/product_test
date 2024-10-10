from rest_framework import routers
from apps.products.views import ProductViewSet
from apps.users.views import UserViewSet

# Create a router and register the ProductViewSet
user_router = routers.SimpleRouter()
user_router.register(r'users', UserViewSet, basename='user')
