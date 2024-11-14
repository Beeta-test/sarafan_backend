from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from PIL import Image
import os

User = get_user_model()


class Category(models.Model):
    name = models.CharField('Наименование', max_length=256)
    slug = models.SlugField('Идентицикатор', unique=True)
    image = models.ImageField('Изображение', upload_to='category/images')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        default_related_name = 'categories'

    def __str__(self) -> str:
        return self.name


class SubCategory(models.Model):
    name = models.CharField('Наименование', max_length=256)
    slug = models.SlugField('Идентицикатор', unique=True)
    image = models.ImageField('Изображение', upload_to='subcategory/images')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категория',
        null=True,
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        default_related_name = 'subcategories'

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField('Наименование', max_length=256)
    slug = models.SlugField('Идентицикатор', unique=True)
    image_original = models.ImageField(
        'Оригинальное изображение',
        upload_to='products/images'
    )
    image_resized = models.ImageField(
        'Изображение 500x500',
        upload_to='products/images/resized',
        blank=True,
        null=True
    )
    image_thumbnail = models.ImageField(
        'Миниатюра 200x200',
        upload_to='products/images/thumbnail',
        blank=True,
        null=True
    )
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name='products'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image_original:
            self.create_resized_image(self.image_original.path, size=(500, 500), field='image_resized')
            self.create_resized_image(self.image_original.path, size=(200, 200), field='image_thumbnail')
            super().save(*args, **kwargs)

    def create_resized_image(self, image_path, size, field):
        base, ext = os.path.splitext(image_path)
        resized_image_path = f"{base}_{size[0]}x{size[1]}{ext}"
        with Image.open(image_path) as img:
            img = img.resize(size, Image.ANTIALIAS)
            img.save(resized_image_path, 'JPEG', quality=75)
        setattr(self, field, resized_image_path.replace(os.path.dirname(self.image_original.name) + os.sep, ''))

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        default_related_name = 'products'

    def __str__(self) -> str:
        return self.name


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_lists'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='in_shopping_lists'
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_shopping_list'
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user.username} - {self.product.name} (x{self.quantity})'

    def get_total_price(self):
        return self.product.price * self.quantity
