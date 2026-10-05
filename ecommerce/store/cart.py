from decimal import Decimal

from .models import Product

SESSION_KEY = "cart"


def _get_cart(session):
    cart = session.get(SESSION_KEY, {})
    return {str(k): int(v) for k, v in cart.items()}


def save_cart(session, cart):
    session[SESSION_KEY] = cart
    session.modified = True


def cart_count(session):
    return sum(_get_cart(session).values())


def add_to_cart(session, product_id, quantity=1):
    cart = _get_cart(session)
    key = str(product_id)
    cart[key] = cart.get(key, 0) + int(quantity)
    save_cart(session, cart)


def set_quantity(session, product_id, quantity):
    cart = _get_cart(session)
    key = str(product_id)
    if quantity <= 0:
        cart.pop(key, None)
    else:
        cart[key] = int(quantity)
    save_cart(session, cart)


def remove_from_cart(session, product_id):
    cart = _get_cart(session)
    cart.pop(str(product_id), None)
    save_cart(session, cart)


def clear_cart(session):
    session.pop(SESSION_KEY, None)
    session.modified = True


def get_cart_items(session):
    cart = _get_cart(session)
    products = Product.objects.filter(id__in=cart.keys()).select_related("category")
    by_id = {str(product.id): product for product in products}
    items = []
    total = Decimal("0.00")
    changed = False
    for key, quantity in cart.items():
        product = by_id.get(key)
        if not product:
            changed = True
            continue
        safe_quantity = min(quantity, product.stock)
        if safe_quantity != quantity:
            changed = True
        if safe_quantity <= 0:
            continue
        subtotal = product.price * safe_quantity
        total += subtotal
        items.append({"product": product, "quantity": safe_quantity, "subtotal": subtotal})
    if changed:
        new_cart = {str(item["product"].id): item["quantity"] for item in items}
        save_cart(session, new_cart)
    return items, total
