import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
def test_get_products_list(api_client):
    url = reverse('product-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert 'results' in response.json()

@pytest.mark.django_db
def test_add_product_to_cart(api_client, user, product):
    url = reverse('cartitem-list')
    api_client.force_authenticate(user=user)
    data = {
        'product': product.id,
        'quantity': 2
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
