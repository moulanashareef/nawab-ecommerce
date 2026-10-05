from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.product_list, name="products"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("products/<int:pk>/add/", views.add_cart, name="add_cart"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/<int:pk>/update/", views.update_cart, name="update_cart"),
    path("cart/<int:pk>/remove/", views.remove_cart, name="remove_cart"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.orders, name="orders"),
    path("orders/<str:order_id>/", views.order_detail, name="order_detail"),
    path("orders/<str:order_id>/cancel/", views.cancel_order, name="cancel_order"),
    path("order-success/<str:order_id>/", views.order_success, name="order_success"),
]