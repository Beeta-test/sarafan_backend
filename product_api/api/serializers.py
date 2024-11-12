from rest_framework import serializers

from product.models import Category, SubCategory, Product, ShoppingList


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image')


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'slug', 'image', 'category')


class ProductSerializer(serializers.ModelSerializer):
    image_small = serializers.ImageField(
        source='image.thumbnail.100x100', read_only=True)
    image_medium = serializers.ImageField(
        source='image.thumbnail.300x300', read_only=True)
    image_large = serializers.ImageField(
        source='image.thumbnail.600x600', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'subcategory', 'category', 'price',
                  'image_small', 'image_medium', 'image_large')


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ('user', 'product', 'quantity')

    def validate(self, data):
        '''Проверка на дубликат продукта в корзине.'''

        if ShoppingList.objects.filter(
            user=data['user'], product=data['product']
        ).exists():
            raise serializers.ValidationError("Этот продукт уже в корзине.")
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        product_representation = ProductSerializer(
            instance.product, context={'request': request}
        ).data
        return product_representation
