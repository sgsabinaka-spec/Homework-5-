from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListAPIView.as_view()),
    path('categories//', views.CategoryDetailAPIView.as_view()),
    
    path('products/', views.ProductListAPIView.as_view()),
    path('products//', views.ProductDetailAPIView.as_view()),
    
    path('reviews/', views.ReviewListAPIView.as_view()),
    path('reviews//', views.ReviewDetailAPIView.as_view()),
]