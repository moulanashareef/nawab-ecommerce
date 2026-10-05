# Generated manually for the Nawab project.
from decimal import Decimal
import uuid

from django.conf import settings
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


def generate_order_id():
    return f"ORD-{uuid.uuid4().hex[:12].upper()}"


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
            options={"ordering": ["name"], "verbose_name_plural": "Categories"},
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal("0.00"))])),
                ("image", models.ImageField(blank=True, null=True, upload_to="products/")),
                ("stock", models.PositiveIntegerField(default=0)),
                ("rating", models.DecimalField(decimal_places=1, default=4.5, max_digits=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="products", to="store.category")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order_id", models.CharField(editable=False, max_length=24, unique=True)),
                ("full_name", models.CharField(max_length=150)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=20)),
                ("address", models.TextField()),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("postal_code", models.CharField(max_length=20)),
                ("total_amount", models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal("0.00"))])),
                ("status", models.CharField(choices=[("Pending", "Pending"), ("Processing", "Processing"), ("Shipped", "Shipped"), ("Delivered", "Delivered"), ("Cancelled", "Cancelled")], default="Pending", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="orders", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ("price", models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal("0.00"))])),
                ("subtotal", models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal("0.00"))])),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="store.order")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="order_items", to="store.product")),
            ],
            options={"constraints": [models.CheckConstraint(condition=models.Q(quantity__gte=1), name="order_item_quantity_gte_1")]},
        ),
        migrations.AddIndex(model_name="product", index=models.Index(fields=["category", "-created_at"], name="store_produc_categor_2dfe30_idx")),
        migrations.AddIndex(model_name="product", index=models.Index(fields=["price"], name="store_produc_price_0f6f0f_idx")),
        migrations.AddIndex(model_name="order", index=models.Index(fields=["user", "-created_at"], name="store_order_user_id_0d9d1e_idx")),
        migrations.AddIndex(model_name="order", index=models.Index(fields=["status"], name="store_order_status_9b9c8f_idx")),
    ]
