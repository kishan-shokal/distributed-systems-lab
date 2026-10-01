from django.db.models import Q
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from .models import (
    Brand,
    Category,
    Product,
    ProductImage,
    ProductReview,
    ProductSpecification,
)

from .serializers import (
    BrandSerializer,
    CategorySerializer,
    ProductDetailSerializer,
    ProductImageSerializer,
    ProductListSerializer,
    ProductReviewSerializer,
    ProductSpecificationSerializer,
)


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    filter_backends = [OrderingFilter]
    ordering_fields = ["name", "created_at"]
    ordering = ["id"]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    filter_backends = [OrderingFilter]
    ordering_fields = ["name", "created_at"]
    ordering = ["id"]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    filter_backends = [OrderingFilter]

    ordering_fields = [
        "id",
        "name",
        "price",
        "created_at",
    ]

    ordering = ["id"]

    def get_serializer_class(self):
        if self.action in ["list"]:
            return ProductListSerializer

        return ProductDetailSerializer

    def get_queryset(self):
        queryset = Product.objects.all()

        # Detail/list optimization
        if self.action == "retrieve":
            queryset = queryset.select_related(
                "brand",
                "category",
            ).prefetch_related(
                "specifications",
                "images",
                "reviews",
            )

        elif self.action == "list":
            queryset = queryset.select_related(
                "brand",
                "category",
            )

        # category filtering
        category = self.request.query_params.get("category")

        if category:
            queryset = queryset.filter(
                category_id=category
            )

        # brand filtering
        brand = self.request.query_params.get("brand")

        if brand:
            queryset = queryset.filter(
                brand_id=brand
            )

        # active products
        is_active = self.request.query_params.get("is_active")

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        # price filtering
        min_price = self.request.query_params.get("min_price")

        if min_price:
            queryset = queryset.filter(
                price__gte=min_price
            )

        max_price = self.request.query_params.get("max_price")

        if max_price:
            queryset = queryset.filter(
                price__lte=max_price
            )

        # search
        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
                | Q(sku__icontains=search)
            )

        return queryset


class ProductSpecificationViewSet(viewsets.ModelViewSet):
    queryset = ProductSpecification.objects.all()
    serializer_class = ProductSpecificationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        product_id = self.request.query_params.get("product")

        if product_id:
            queryset = queryset.filter(
                product_id=product_id
            )

        return queryset


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        product_id = self.request.query_params.get("product")

        if product_id:
            queryset = queryset.filter(
                product_id=product_id
            )

        return queryset


class ProductReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        product_id = self.request.query_params.get("product")

        if product_id:
            queryset = queryset.filter(
                product_id=product_id
            )

        return queryset