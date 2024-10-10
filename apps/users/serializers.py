from rest_framework import serializers
from apps.users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=9)  # Ensure password is not returned in responses
    password2 = serializers.CharField(write_only=True, min_length=9)  # Ensure password2 is not returned in responses

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password2')  # Added password and email

    def validate(self, data):
        """Check that the two passwords match."""
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for retrieving user details."""
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', )


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    email = serializers.EmailField()  # Added email field for login
    password = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    """Serializer for user logout."""
    refresh_token = serializers.CharField()


class UserLoginResponseSerializer(serializers.Serializer):
    """Serializer for user login response."""
    refresh_token = serializers.CharField()
    access_token = serializers.CharField()
    user_id = serializers.IntegerField()
