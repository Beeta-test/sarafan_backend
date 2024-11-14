import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from product.models import Product, Category, SubCategory


User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def category():
    return Category.objects.create(name='Test Category', slug='test-category')


@pytest.fixture
def subcategory(category):
    return SubCategory.objects.create(
        name='Test SubCategory', slug='test-subcategory', category=category
    )


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="password")


@pytest.fixture
def product(subcategory, category, user):
    return Product.objects.create(
        name='Test Product',
        slug='test-product',
        price='10.00',
        subcategory=subcategory,
        category=category,
        author=user
    )


@pytest.mark.django_db
def test_create_product(api_client, category, subcategory, user):
    product_data = {
        'name': 'New Product',
        'slug': 'new-product',
        'price': '20.00',
        'author': user.id,
        'subcategory': subcategory.id,
        'category': category.id,
    }
    url = reverse('product-list')
    response = api_client.post(url, product_data)
    print(response.json())
    assert response.status_code == status.HTTP_201_CREATED
    assert Product.objects.count() == 1
    assert Product.objects.first().name == 'New Product'


@pytest.mark.django_db
def test_category_list_status(api_client):
    url = reverse('category-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_subcategory_list_status(api_client):
    url = reverse('subcategory-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_delete_product(api_client, product, user):
    product.author = user
    product.save()
    api_client.force_authenticate(user=user)
    url = reverse('product-detail', args=[product.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_add_product_to_shopping_list(api_client, product, user):
    product.author = user
    product.save()
    api_client.force_authenticate(user=user)
    url = reverse('product-shopping-list', args=[product.id])
    response = api_client.post(url)
    assert response.status_code == status.HTTP_201_CREATED
