import pytest

from product.models import Category, SubCategory, Product


@pytest.fixture
def category():
    return Category.objects.create(name='Test Category', slug='test-category')


@pytest.fixture
def subcategory(category):
    return SubCategory.objects.create(
        name='Test SubCategory', slug='test-subcategory', category=category
    )


@pytest.fixture
def product(subcategory, category):
    return Product.objects.create(
        name='Test Product',
        slug='test-product',
        image='path/to/image.jpg',
        price='10.00',
        subcategory=subcategory,
        category=category
    )
