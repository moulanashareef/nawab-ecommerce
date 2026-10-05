from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .cart import add_to_cart, clear_cart, get_cart_items, remove_from_cart, set_quantity
from .forms import CheckoutForm, RegistrationForm
from .models import Category, Order, OrderItem, Product


def home(request):
    products = Product.objects.select_related("category")[:8]
    categories = Category.objects.all()[:6]
    return render(
        request,
        "store/home.html",
        {
            "products": products,
            "categories": categories,
        },
    )


def product_list(request):
    products = Product.objects.select_related("category")
    categories = Category.objects.all()

    query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "").strip()
    sort = request.GET.get("sort", "newest")
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
        )

    if category_id.isdigit():
        products = products.filter(category_id=int(category_id))

    try:
        if min_price:
            products = products.filter(price__gte=Decimal(min_price))

        if max_price:
            products = products.filter(price__lte=Decimal(max_price))

    except InvalidOperation:
        messages.warning(
            request,
            "Price filters must contain valid numbers.",
        )

    sort_map = {
        "price_low": "price",
        "price_high": "-price",
        "rating": "-rating",
        "name": "name",
        "newest": "-created_at",
    }

    products = products.order_by(
        sort_map.get(sort, "-created_at")
    )

    return render(
        request,
        "store/products.html",
        {
            "products": products,
            "categories": categories,
            "query": query,
            "selected_category": category_id,
            "sort": sort,
            "min_price": min_price,
            "max_price": max_price,
        },
    )


def product_detail(request, pk):
    product = get_object_or_404(
        Product.objects.select_related("category"),
        pk=pk,
    )

    related = Product.objects.filter(
        category=product.category
    ).exclude(
        pk=product.pk
    )[:4]

    return render(
        request,
        "store/product_detail.html",
        {
            "product": product,
            "related": related,
        },
    )


def add_cart(request, pk):
    if request.method != "POST":
        return redirect("product_detail", pk=pk)

    product = get_object_or_404(Product, pk=pk)

    if product.stock <= 0:
        messages.error(
            request,
            "This product is currently out of stock.",
        )

        if request.POST.get("next"):
            return redirect(request.POST["next"])

        return redirect("product_detail", pk=pk)

    try:
        quantity = max(
            1,
            int(request.POST.get("quantity", 1)),
        )
    except (TypeError, ValueError):
        quantity = 1

    current = next(
        (
            item["quantity"]
            for item in get_cart_items(request.session)[0]
            if item["product"].id == product.id
        ),
        0,
    )

    if current + quantity > product.stock:
        messages.error(
            request,
            f"Only {product.stock} item(s) are available.",
        )
    else:
        add_to_cart(
            request.session,
            product.id,
            quantity,
        )

        messages.success(
            request,
            f"{product.name} was added to your cart.",
        )

    next_url = request.POST.get("next", "").strip()

    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(next_url)

    return redirect("cart")


def cart_view(request):
    items, total = get_cart_items(request.session)

    return render(
        request,
        "store/cart.html",
        {
            "items": items,
            "total": total,
        },
    )


def update_cart(request, pk):
    if request.method != "POST":
        return redirect("cart")

    product = get_object_or_404(Product, pk=pk)

    try:
        quantity = int(
            request.POST.get("quantity", 1)
        )
    except (TypeError, ValueError):
        quantity = 1

    if quantity > product.stock:
        messages.error(
            request,
            f"Only {product.stock} item(s) are available.",
        )
    else:
        set_quantity(
            request.session,
            pk,
            quantity,
        )

        messages.success(
            request,
            "Cart updated.",
        )

    return redirect("cart")


def remove_cart(request, pk):
    if request.method == "POST":
        remove_from_cart(
            request.session,
            pk,
        )

        messages.success(
            request,
            "Item removed from your cart.",
        )

    return redirect("cart")


def register(request):
    if request.user.is_authenticated:
        return redirect("profile")

    form = RegistrationForm(
        request.POST or None
    )

    if request.method == "POST" and form.is_valid():
        user = form.save()

        login(request, user)

        messages.success(
            request,
            "Your account was created successfully.",
        )

        return redirect("home")

    return render(
        request,
        "registration/register.html",
        {
            "form": form,
        },
    )


@login_required
def profile(request):
    orders = request.user.orders.all()[:8]

    return render(
        request,
        "store/profile.html",
        {
            "orders": orders,
        },
    )


@login_required
def checkout(request):
    items, total = get_cart_items(
        request.session
    )

    if not items:
        messages.info(
            request,
            "Your cart is empty. Add a product before checkout.",
        )

        return redirect("cart")

    initial = {
        "full_name": request.user.get_full_name(),
        "email": request.user.email,
    }

    form = CheckoutForm(
        request.POST or None,
        initial=initial,
    )

    if request.method == "POST" and form.is_valid():

        with transaction.atomic():

            locked_products = {
                p.id: p
                for p in Product.objects.select_for_update().filter(
                    id__in=[
                        i["product"].id
                        for i in items
                    ]
                )
            }

            final_items = []
            final_total = Decimal("0.00")

            for item in items:

                product = locked_products.get(
                    item["product"].id
                )

                if (
                    not product
                    or product.stock < item["quantity"]
                ):
                    messages.error(
                        request,
                        f"{item['product'].name} no longer has enough stock. Please review your cart.",
                    )

                    return redirect("cart")

                subtotal = (
                    product.price
                    * item["quantity"]
                )

                final_items.append(
                    (
                        product,
                        item["quantity"],
                        product.price,
                        subtotal,
                    )
                )

                final_total += subtotal

            order = form.save(
                commit=False
            )

            order.user = request.user
            order.total_amount = final_total

            order.save()

            for (
                product,
                quantity,
                price,
                subtotal,
            ) in final_items:

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price,
                    subtotal=subtotal,
                )

                product.stock -= quantity

                product.save(
                    update_fields=["stock"]
                )

            clear_cart(
                request.session
            )

        return redirect(
            "order_success",
            order_id=order.order_id,
        )

    return render(
        request,
        "store/checkout.html",
        {
            "form": form,
            "items": items,
            "total": total,
        },
    )


@login_required
def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        order_id=order_id,
        user=request.user,
    )

    return render(
        request,
        "store/order_success.html",
        {
            "order": order,
        },
    )


@login_required
def orders(request):
    return render(
        request,
        "store/orders.html",
        {
            "orders": request.user.orders.all(),
        },
    )


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related(
            "items__product"
        ),
        order_id=order_id,
        user=request.user,
    )

    return render(
        request,
        "store/order_detail.html",
        {
            "order": order,
        },
    )


@login_required
def cancel_order(request, order_id):
    if request.method != "POST":
        return redirect(
            "order_detail",
            order_id=order_id,
        )

    order = get_object_or_404(
        Order,
        order_id=order_id,
        user=request.user,
    )

    if order.status != "Pending":
        messages.error(
            request,
            "This order can no longer be cancelled.",
        )

        return redirect(
            "order_detail",
            order_id=order_id,
        )

    order.status = "Cancelled"

    order.save(
        update_fields=["status"]
    )

    messages.success(
        request,
        "Your order has been cancelled successfully.",
    )

    return redirect(
        "order_detail",
        order_id=order_id,
    )