from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, obj):
        return obj.products.count()

    def validate_name(self, value):
        if len(value) < 2:
            raise ValidationError("Название категории должно содержать минимум 2 символа.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, value):
        if value <= 0:
            raise ValidationError("Цена товара должна быть больше нуля.")
        return value

    def validate_title(self, value):
        if len(value) < 3:
            raise ValidationError("Название товара слишком короткое (минимум 3 символа).")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_stars(self, value):
        if not (1 <= value <= 5):
            raise ValidationError("Оценка должна быть в диапазоне от 1 до 5.")
        return value
        
    def validate_text(self, value):
        if len(value.strip()) == 0:
            raise ValidationError("Текст отзыва не может быть пустым.")
        return value


class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'rating']

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            total_stars = sum([review.stars for review in reviews])
            return round(total_stars / len(reviews), 2)
        return 0