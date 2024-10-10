from django.db import models

from services.base.models import TimeStampModel


class Category(models.TextChoices):
    ELECTRONICS = 'electronics', 'Electronics'
    FASHION = 'fashion', 'Fashion'
    BOOKS = 'books', 'Books'
    FOOD = 'food', 'Food'
    TOYS = 'toys', 'Toys'


class Product(TimeStampModel):
    name = models.CharField(
        max_length=255,
        verbose_name="Название продукта"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание продукта"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена продукта"
    )
    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        verbose_name="Категория продукта"
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name="Изображение продукта"
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name
