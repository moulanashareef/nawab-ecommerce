from django.contrib import admin

from .models import Category, Order, OrderItem, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "product_count")
    search_fields = ("name", "description")

    @admin.display(description="Products")
    def product_count(self, obj):
        return obj.products.count()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "rating", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("name", "description")
    list_editable = ("price", "stock", "rating")
    readonly_fields = ("created_at",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("subtotal",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_id",
        "full_name",
        "email",
        "phone",
        "total_amount",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "order_id",
        "full_name",
        "email",
        "phone",
        "user__username",
    )

    readonly_fields = (
        "order_id",
        "created_at",
        "total_amount",
    )

    list_editable = ("status",)

    fieldsets = (
        (
            "Order Information",
            {
                "fields": (
                    "order_id",
                    "user",
                    "status",
                    "total_amount",
                    "created_at",
                )
            },
        ),
        (
            "Customer Details",
            {
                "fields": (
                    "full_name",
                    "email",
                    "phone",
                    "address",
                    "city",
                    "state",
                    "postal_code",
                )
            },
        ),
    )

    inlines = (OrderItemInline,)
