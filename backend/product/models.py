# models.py

from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Brand(TimestampedModel):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=180, unique=True)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "brands"
        indexes = [
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name


class Category(TimestampedModel):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "categories"
        indexes = [
            models.Index(fields=["parent"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["parent", "is_active"]),
        ]

    def __str__(self):
        return self.name


class Product(TimestampedModel):
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350, unique=True)

    description = models.TextField()

    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="products",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    stock = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "products"

        indexes = [
            models.Index(fields=["category", "is_active"]),
            models.Index(fields=["brand", "is_active"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["price"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.name


class ProductSpecification(TimestampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="specifications",
    )

    key = models.CharField(max_length=150)
    value = models.TextField()

    class Meta:
        db_table = "product_specifications"

        constraints = [
            models.UniqueConstraint(
                fields=["product", "key"],
                name="unique_product_specification",
            )
        ]

        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["key"]),
        ]

    def __str__(self):
        return f"{self.product_id}: {self.key}"


class ProductImage(TimestampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image_url = models.URLField(max_length=1000)

    alt_text = models.CharField(
        max_length=300,
        blank=True,
    )

    position = models.PositiveIntegerField(default=0)

    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = "product_images"

        indexes = [
            models.Index(fields=["product", "position"]),
            models.Index(fields=["product", "is_primary"]),
        ]

        ordering = ["position"]

    def __str__(self):
        return f"{self.product_id} - image {self.position}"


class ProductReview(TimestampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    rating = models.PositiveSmallIntegerField()

    title = models.CharField(
        max_length=300,
        blank=True,
    )

    body = models.TextField()

    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = "product_reviews"

        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["product", "rating"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.product_id} - {self.rating}"