from rest_framework.routers import DefaultRouter

from .views import (
    BrandViewSet,
    CategoryViewSet,
    ProductImageViewSet,
    ProductReviewViewSet,
    ProductSpecificationViewSet,
    ProductViewSet,
)


router = DefaultRouter()

router.register(
    r"",
    ProductViewSet,
    basename="product",
)

router.register(
    r"brands",
    BrandViewSet,
    basename="brand",
)

router.register(
    r"categories",
    CategoryViewSet,
    basename="category",
)

router.register(
    r"specifications",
    ProductSpecificationViewSet,
    basename="specification",
)

router.register(
    r"images",
    ProductImageViewSet,
    basename="image",
)

router.register(
    r"reviews",
    ProductReviewViewSet,
    basename="review",
)


urlpatterns = router.urls