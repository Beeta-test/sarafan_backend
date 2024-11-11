from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import CategoryViewSet, SubCategoryViewSet, ProductViewSet

router = DefaultRouter()

router.register(
    'category',
    CategoryViewSet,
    basename='category'
)

router.register(
    'subcategory',
    SubCategoryViewSet,
    basename='subcategory'
)

router.register(
    'product',
    ProductViewSet,
    basename='product'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
