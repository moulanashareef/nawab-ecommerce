# Nawab

A portfolio-ready simple e-commerce application built with Django, SQLite, HTML5, CSS3 and vanilla JavaScript.

## Features

- Responsive premium storefront
- Product catalog with search, category, price and sorting filters
- Product details and related products
- Session-based shopping cart with stock-aware quantity controls
- Django registration, login (username or email), logout and profile
- Authenticated checkout with server-side validation
- Database-backed orders and order items
- Customer order history and protected order details
- Django Admin management for products, categories and orders
- Demo data command with 150 realistic products (30 per category)
- Friendly empty/error states and responsive navigation
- CSRF protection, Django password hashing and authorization checks

## Technologies Used

- HTML5
- CSS3
- JavaScript (vanilla)
- Python
- Django
- SQLite


## Installation

### 1. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Add demo catalog data

```bash
python manage.py seed_demo
```

### 5. Create an admin user

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser. The admin panel is at http://127.0.0.1:8000/admin/.

## Environment Variables

For production, set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, and `DJANGO_ALLOWED_HOSTS`.

```bash
DJANGO_SECRET_KEY="replace-me"
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS="example.com,www.example.com"
```

Do not commit secrets, `db.sqlite3`, media uploads, virtual environments or Python cache files.

## Project Structure

```text
ecommerce/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── ecommerce/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── store/
│   ├── migrations/
│   ├── management/commands/seed_demo.py
│   ├── static/store/css/style.css
│   ├── static/store/js/app.js
│   ├── static/store/images/product-placeholder.svg
│   ├── admin.py
│   ├── apps.py
│   ├── cart.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   ├── registration/
│   └── store/
└── media/
```

## Testing Checklist

Before submission, run:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Then manually verify registration, login/logout, product browsing, search/filter/sort, cart updates, checkout, order history, admin CRUD and responsive layouts.

## GitHub Upload

```bash
git init
git add .
git commit -m "Build premium Django e-commerce store"
git branch -M main
git remote add origin <repository-url>
git push -u origin main
```

Do not add `venv/`, `db.sqlite3`, `media/`, `staticfiles/`, `.env` or secrets.

## Future Improvements

- Payment gateway integration
- Product reviews and verified ratings
- Wishlist and saved carts
- Coupon/discount system
- Email order confirmations
- Pagination and richer product search
- Production object storage for media
- Automated tests and CI/CD


## Product Images

The demo catalog uses real photographs hosted by Pexels. Product image fields store the Pexels image URLs so the project does not bundle generated placeholder product art. Pexels states that its photos are free to use for personal and commercial projects under the Pexels license; do not imply brand/person endorsement and review any depicted trademark or person before commercial use.
