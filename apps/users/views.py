from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from apps.users.models import User
from apps.users.serializers import (
    UserDetailSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserLoginResponseSerializer,
)
from apps.users.services.jwt import AuthService
from apps.users.services.users import (
    UserService,
    UserCreatService,
    UserLoginService,
    UserUpdateService,
)


def create_user_service() -> UserService:
    auth_service = AuthService()
    user_create_service = UserCreatService()
    user_login_service = UserLoginService(auth_service)
    user_update_service = UserUpdateService()
    return UserService(user_create_service, user_login_service, user_update_service)


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    swagger_tags = ["User"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = create_user_service()

    def get_serializer_class(self):
        serializer_map = {
            'sign_up': UserRegistrationSerializer,
            'sign_in': UserLoginSerializer,
            'user': UserDetailSerializer,
        }
        return serializer_map.get(self.action, self.serializer_class)

    @swagger_auto_schema(
        operation_description="Creates a new user with the provided data.",
        request_body=UserRegistrationSerializer,
        responses={201: UserDetailSerializer()}
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='sign_up')
    def sign_up(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.user_service.user_create_service.create(
            email=serializer.validated_data['email'],
            username=serializer.validated_data['username'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            password=serializer.validated_data['password']
        )
        return Response(UserDetailSerializer(user).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="User login.",
        request_body=UserLoginSerializer,
        responses={200: UserLoginResponseSerializer()}
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='sign_in')
    def sign_in(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response_data = self.user_service.user_login_service.execute(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='get',
        operation_description="Retrieves information about the user.",
        responses={200: UserDetailSerializer()}
    )
    @swagger_auto_schema(
        method='patch',
        operation_description="Updates user information with the provided data.",
        request_body=UserDetailSerializer(),
        responses={200: UserDetailSerializer()}
    )
    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated], url_path='')
    def user(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = UserDetailSerializer(data=request.data, instance=user)
            serializer.is_valid(raise_exception=True)
            user = self.user_service.update_user(user.id, **serializer.validated_data)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
