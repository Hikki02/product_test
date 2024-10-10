
from rest_framework import serializers

from apps.products.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'price',
            'category',
            'image',
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше нуля")
        return value

    def validate(self, data):
        if 'name' in data and len(data['name']) < 3:
            raise serializers.ValidationError("Название продукта должно содержать минимум 3 символа")
        return data
