from rest_framework import viewsets, decorators, permissions, response, status

from product.models import Product, Category, SubCategory, ShoppingList
from .permissions import IsAuthorOrReadOnly
from .paginations import LimitPageNumberPagination
from .serializers import CategorySerializer, SubCategorySerializer, ProductSerializer, ShoppingListSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitPageNumberPagination


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitPageNumberPagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitPageNumberPagination

    def remove_item(self, model, request, pk=None):
        product = self.get_object()
        user = request.user

        delete_count, _ = model.objects.filter(
            user=user, product=product).delete()

        if not delete_count:
            return response.Response(
                (f'Запись с пользователем {user.id}'
                 f'и продуктом {product.id} не найдена.'),
                status=status.HTTP_400_BAD_REQUEST
            )

        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def add_to_list(self, serializer_class, request, product):
        user = request.user
        serializer = serializer_class(
            data={'user': user.id, 'product': product.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    @decorators.action(
        detail=True,
        methods=['post'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def shopping_list(self, request, pk=None):
        product = self.get_object()
        return self.add_to_list(ShoppingListSerializer, request, product)

    @shopping_list.mapping.delete
    def remove_from_shopping_cart(self, request, pk=None):
        return self.remove_item(ShoppingList, request, pk)