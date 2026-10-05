from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category, Order, OrderItem, Product

User = get_user_model()


class StoreFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="tester", email="tester@example.com", password="StrongPass123!")
        cls.category = Category.objects.create(name="Electronics", description="Demo")
        cls.product = Product.objects.create(
            name="Test Headphones",
            category=cls.category,
            description="A test product.",
            price=Decimal("1200.00"),
            stock=5,
            rating=Decimal("4.5"),
        )

    def test_public_catalog_pages(self):
        self.assertEqual(self.client.get(reverse("home")).status_code, 200)
        self.assertEqual(self.client.get(reverse("products")).status_code, 200)
        self.assertEqual(self.client.get(reverse("product_detail", args=[self.product.pk])).status_code, 200)

    def test_registration(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login_by_email(self):
        response = self.client.post(reverse("login"), {"username": "tester@example.com", "password": "StrongPass123!"})
        self.assertRedirects(response, reverse("profile"))

    def test_cart_add_and_update(self):
        response = self.client.post(reverse("add_cart", args=[self.product.pk]), {"quantity": 2, "next": reverse("cart")})
        self.assertRedirects(response, reverse("cart"))
        cart = self.client.session["cart"]
        self.assertEqual(cart[str(self.product.pk)], 2)
        self.client.post(reverse("update_cart", args=[self.product.pk]), {"quantity": 3})
        self.assertEqual(self.client.session["cart"][str(self.product.pk)], 3)

    def test_checkout_creates_order_and_reduces_stock(self):
        self.client.login(username="tester", password="StrongPass123!")
        self.client.post(reverse("add_cart", args=[self.product.pk]), {"quantity": 2, "next": reverse("cart")})
        response = self.client.post(reverse("checkout"), {
            "full_name": "Test User",
            "email": "tester@example.com",
            "phone": "9876543210",
            "address": "123 Test Street",
            "city": "Hyderabad",
            "state": "Telangana",
            "postal_code": "500001",
        })
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.total_amount, Decimal("2400.00"))
        self.assertEqual(OrderItem.objects.get(order=order).quantity, 2)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

    def test_order_detail_is_private_to_owner(self):
        order = Order.objects.create(user=self.user, full_name="Test User", email=self.user.email, phone="9876543210", address="A", city="B", state="C", postal_code="500001", total_amount=Decimal("0.00"))
        other = User.objects.create_user(username="other", password="StrongPass123!")
        self.client.login(username="other", password="StrongPass123!")
        response = self.client.get(reverse("order_detail", args=[order.order_id]))
        self.assertEqual(response.status_code, 404)
