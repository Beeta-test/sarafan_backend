import pytest
from django.urls import reverse
from rest_framework import status
from product.models import Product, ShoppingList
from .conftest import product, subcategory, category


@pytest.mark.django_db
def test_create_product(api_client, category, subcategory):
    product_data = {
        'name': 'New Product',
        'slug': 'new-product',
        'image': 'path/to/image.jpg',
        'price': '20.00',
        'subcategory': subcategory.id,
        'category': category.id,
    }
    url = reverse('product-list')
    response = api_client.post(url, product_data)
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
def test_delete_product(api_client, product):
    url = reverse('product-detail', args=[product.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Product.objects.count() == 0


@pytest.mark.django_db
def test_add_product_to_shopping_list(api_client, product):
    url = reverse('product-shopping_list', args=[product.id])
    response = api_client.post(url)
    assert response.status_code == status.HTTP_201_CREATED
    assert ShoppingList.objects.count() == 1
    shopping_item = ShoppingList.objects.first()
    assert shopping_item.product == product
