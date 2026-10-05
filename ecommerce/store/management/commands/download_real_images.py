import os
import re
import ssl
from urllib.request import Request, urlopen
from django.core.management.base import BaseCommand
from django.conf import settings
from store.models import Product


def slugify(value):
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "product"


class Command(BaseCommand):
    help = "Download the 150 real Pexels product photos locally and switch products to /media/ URLs."

    def handle(self, *args, **options):
        products = Product.objects.exclude(image__isnull=True).exclude(image="").order_by("category__name", "name")
        target = os.path.join(settings.MEDIA_ROOT, "products")
        os.makedirs(target, exist_ok=True)
        ok = 0
        failed = 0
        for product in products:
            url = product.image
            if not url.startswith("http"):
                continue
            filename = slugify(product.name) + ".jpg"
            path = os.path.join(target, filename)
            try:
                req = Request(url, headers={"User-Agent": "Nawab Ecommerce Demo/1.0"})
                with urlopen(req, timeout=30) as response, open(path, "wb") as f:
                    f.write(response.read())
                product.image = settings.MEDIA_URL + "products/" + filename
                product.save(update_fields=["image"])
                ok += 1
                self.stdout.write(self.style.SUCCESS(f"Downloaded: {product.name}"))
            except Exception as exc:
                failed += 1
                self.stdout.write(self.style.WARNING(f"Failed: {product.name} — {exc}"))
        self.stdout.write(self.style.SUCCESS(f"Real product photos downloaded: {ok}; failed: {failed}."))
