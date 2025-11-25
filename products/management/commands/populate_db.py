from django.core.management.base import BaseCommand
from products.models import Category, Product


class Command(BaseCommand):
    help = "Populate database with sample categories and products"

    def handle(self, *args, **options):
        # Categories (idempotent with get_or_create)
        electronics, _ = Category.objects.get_or_create(
            slug="electronics",
            defaults={
                "name": "Electronics",
                "description": "Electronic devices and gadgets",
            },
        )
        clothing, _ = Category.objects.get_or_create(
            slug="clothing",
            defaults={
                "name": "Clothing",
                "description": "Fashion and apparel",
            },
        )
        accessories, _ = Category.objects.get_or_create(
            slug="accessories",
            defaults={
                "name": "Accessories",
                "description": "Bags, watches, and more",
            },
        )
        home, _ = Category.objects.get_or_create(
            slug="home-kitchen",
            defaults={
                "name": "Home & Kitchen",
                "description": "Essentials for your home",
            },
        )

        # Helper to avoid duplicates on repeated runs
        def create_product(category, name, slug, description, price, stock):
            Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "category": category,
                    "name": name,
                    "description": description,
                    "price": price,
                    "stock": stock,
                    "available": True,
                },
            )

        # Electronics
        create_product(
            electronics,
            "Laptop",
            "laptop",
            "High-performance laptop for work and gaming.",
            999.99,
            10,
        )
        create_product(
            electronics,
            "Smartphone",
            "smartphone",
            "Latest-generation smartphone with stunning camera.",
            699.99,
            25,
        )
        create_product(
            electronics,
            "Wireless Headphones",
            "wireless-headphones",
            "Noise-cancelling over-ear wireless headphones.",
            149.99,
            40,
        )
        create_product(
            electronics,
            "Smartwatch",
            "smartwatch",
            "Fitness tracking smartwatch with heart-rate monitor.",
            199.99,
            35,
        )

        # Clothing
        create_product(
            clothing,
            "Classic T-Shirt",
            "classic-t-shirt",
            "Soft cotton t-shirt available in multiple colors.",
            19.99,
            80,
        )
        create_product(
            clothing,
            "Denim Jeans",
            "denim-jeans",
            "Slim-fit stretch denim jeans.",
            49.99,
            50,
        )
        create_product(
            clothing,
            "Hoodie",
            "hoodie",
            "Cozy fleece hoodie for everyday wear.",
            39.99,
            60,
        )

        # Accessories
        create_product(
            accessories,
            "Leather Wallet",
            "leather-wallet",
            "Genuine leather slim wallet.",
            29.99,
            70,
        )
        create_product(
            accessories,
            "Backpack",
            "backpack",
            "Water-resistant laptop backpack.",
            59.99,
            45,
        )

        # Home & Kitchen
        create_product(
            home,
            "Ceramic Mug Set",
            "ceramic-mug-set",
            "Set of 4 large ceramic mugs.",
            24.99,
            100,
        )
        create_product(
            home,
            "Non-stick Pan",
            "non-stick-pan",
            "Durable non-stick frying pan.",
            34.99,
            55,
        )

        self.stdout.write(self.style.SUCCESS("Sample categories and products populated successfully."))