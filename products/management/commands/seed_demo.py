from django.core.management.base import BaseCommand
from django.db import transaction
from products.models import Category, Product

CATEGORIES = [
    ("electronics", "Electronics"),
    ("clothing", "Clothing"),
    ("accessories", "Accessories"),
    ("home-kitchen", "Home & Kitchen"),
]

DEMO_PRODUCTS = [
    {
        "name": "Wireless Headphones",
        "slug": "wireless-headphones",
        "category": "electronics",
        "price": 79.99,
        "description": "Comfortable over-ear wireless headphones with noise isolation.",
    },
    {
        "name": "Smartphone Case",
        "slug": "smartphone-case",
        "category": "accessories",
        "price": 14.99,
        "description": "Shock-absorbing TPU case with raised bezels for screen & camera.",
    },
    {
        "name": "Ceramic Mug Set",
        "slug": "ceramic-mug-set",
        "category": "home-kitchen",
        "price": 24.50,
        "description": "Set of 4 ceramic mugs, dishwasher safe.",
    },
    {
        "name": "Graphic T-Shirt",
        "slug": "graphic-tshirt",
        "category": "clothing",
        "price": 19.99,
        "description": "Soft cotton tee with a minimal graphic print.",
    },
    {
        "name": "Running Shoes",
        "slug": "running-shoes",
        "category": "clothing",
        "price": 59.00,
        "description": "Lightweight running shoes with breathable mesh upper.",
    },
    {
        "name": "Bluetooth Speaker",
        "slug": "bluetooth-speaker",
        "category": "electronics",
        "price": 39.99,
        "description": "Portable speaker with strong bass and 12h battery life.",
    },
    {
        "name": "Leather Wallet",
        "slug": "leather-wallet",
        "category": "accessories",
        "price": 29.00,
        "description": "Slim, RFID-blocking genuine leather wallet.",
    },
    {
        "name": "Stainless Steel Knife Set",
        "slug": "knife-set",
        "category": "home-kitchen",
        "price": 48.75,
        "description": "6-piece stainless-steel knife set with wooden block.",
    },
]

class Command(BaseCommand):
    help = "Seed demo categories and products (hotlink images via templates fallbacks)."

    @transaction.atomic
    def handle(self, *args, **options):
        slug_to_cat = {}
        for slug, name in CATEGORIES:
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name})
            slug_to_cat[slug] = cat
        created = 0
        for p in DEMO_PRODUCTS:
            Product.objects.update_or_create(
                slug=p["slug"],
                defaults={
                    "name": p["name"],
                    "category": slug_to_cat[p["category"]],
                    "price": p["price"],
                    "description": p["description"],
                    "available": True,
                    "stock": 20,
                },
            )
            created += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded/updated {created} demo products."))
