from django.db import models
from django.contrib.auth import get_user_model

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
        verbose_name='Категория'
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
    image = models.ImageField('Изображение', upload_to='products/images')
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
