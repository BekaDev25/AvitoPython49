"""
avito_app/management/commands/seed_data.py

Наполняет базу тестовыми данными для всех моделей проекта,
включая переводы (en/ru) для полей, зарегистрированных в modeltranslation.

Запуск:
    python manage.py seed_data

Перед запуском создайте пустые файлы:
    avito_app/management/__init__.py
    avito_app/management/commands/__init__.py
"""

from decimal import Decimal

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from avito_app.models import (
    UserProfile,
    Category,
    SubCategory,
    Product,
    ProductImages,
    Review,
)

# Простое "изображение" 1x1 px в base64 (валидный GIF), чтобы ImageField
# не ругался при отсутствии реального файла.
FAKE_IMAGE_CONTENT = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04"
    b"\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D"
    b"\x01\x00;"
)


def fake_image(name: str) -> ContentFile:
    return ContentFile(FAKE_IMAGE_CONTENT, name=name)


class Command(BaseCommand):
    help = "Наполняет базу тестовыми данными (с переводами en/ru) для всех моделей"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Начинаю наполнение базы данными...")

        # ---------------------------------------------------------
        # 1. UserProfile (кастомная модель пользователя)
        # ---------------------------------------------------------
        users_data = [
            {
                "username": "admin_gold",
                "email": "admin_gold@example.com",
                "age": 28,
                "phone_number": "+996700111222",
                "status": "gold",
            },
            {
                "username": "user_silver",
                "email": "user_silver@example.com",
                "age": 34,
                "phone_number": "+996700333444",
                "status": "silver",
            },
            {
                "username": "user_bronze",
                "email": "user_bronze@example.com",
                "age": 22,
                "phone_number": "+996700555666",
                "status": "bronze",
            },
            {
                "username": "user_simple",
                "email": "user_simple@example.com",
                "age": 19,
                "phone_number": "+996700777888",
                "status": "simple",
            },
        ]

        users = []
        for data in users_data:
            user, created = UserProfile.objects.get_or_create(
                username=data["username"],
                defaults={
                    "email": data["email"],
                    "age": data["age"],
                    "phone_number": data["phone_number"],
                    "status": data["status"],
                    "avatar": fake_image(f"{data['username']}_avatar.gif"),
                },
            )
            if created:
                user.set_password("Test12345!")
                user.save()
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f"Создано пользователей: {len(users)}"))

        # ---------------------------------------------------------
        # 2. Category (с переводами category_name)
        # ---------------------------------------------------------
        categories_data = [
            {"en": "Electronics", "ru": "Электроника"},
            {"en": "Clothing", "ru": "Одежда"},
            {"en": "Home & Garden", "ru": "Дом и сад"},
        ]

        categories = []
        for i, cat in enumerate(categories_data, start=1):
            category = Category()
            category.category_name_en = cat["en"]
            category.category_name_ru = cat["ru"]
            category.category_image = fake_image(f"category_{i}.gif")
            category.save()
            categories.append(category)
        self.stdout.write(self.style.SUCCESS(f"Создано категорий: {len(categories)}"))

        # ---------------------------------------------------------
        # 3. SubCategory (с переводами subcategory_name)
        # ---------------------------------------------------------
        subcategories_data = [
            {"category": categories[0], "en": "Smartphones", "ru": "Смартфоны"},
            {"category": categories[0], "en": "Laptops", "ru": "Ноутбуки"},
            {"category": categories[1], "en": "Men's Clothing", "ru": "Мужская одежда"},
            {"category": categories[1], "en": "Women's Clothing", "ru": "Женская одежда"},
            {"category": categories[2], "en": "Furniture", "ru": "Мебель"},
        ]

        subcategories = []
        for i, sub in enumerate(subcategories_data, start=1):
            subcategory = SubCategory()
            subcategory.category = sub["category"]
            subcategory.subcategory_name_en = sub["en"]
            subcategory.subcategory_name_ru = sub["ru"]
            subcategory.subcategory_image = fake_image(f"subcategory_{i}.gif")
            subcategory.save()
            subcategories.append(subcategory)
        self.stdout.write(self.style.SUCCESS(f"Создано подкатегорий: {len(subcategories)}"))

        # ---------------------------------------------------------
        # 4. Products (с переводами product_name и description)
        # ---------------------------------------------------------
        products_data = [
            {
                "subcategory": subcategories[0],
                "name_en": "iPhone 15 Pro",
                "name_ru": "Айфон 15 Про",
                "desc_en": "Latest Apple smartphone with A17 chip",
                "desc_ru": "Новейший смартфон Apple с чипом A17",
                "price": Decimal("999.99"),
                "article_number": 1000001,
            },
            {
                "subcategory": subcategories[1],
                "name_en": "MacBook Air M3",
                "name_ru": "МакБук Эйр М3",
                "desc_en": "Lightweight and powerful laptop",
                "desc_ru": "Легкий и мощный ноутбук",
                "price": Decimal("1299.00"),
                "article_number": 1000002,
            },
            {
                "subcategory": subcategories[2],
                "name_en": "Men's Denim Jacket",
                "name_ru": "Мужская джинсовая куртка",
                "desc_en": "Classic blue denim jacket",
                "desc_ru": "Классическая синяя джинсовая куртка",
                "price": Decimal("59.90"),
                "article_number": 1000003,
            },
            {
                "subcategory": subcategories[3],
                "name_en": "Women's Summer Dress",
                "name_ru": "Женское летнее платье",
                "desc_en": "Light floral summer dress",
                "desc_ru": "Легкое летнее платье с цветочным принтом",
                "price": Decimal("39.50"),
                "article_number": 1000004,
            },
            {
                "subcategory": subcategories[4],
                "name_en": "Wooden Dining Table",
                "name_ru": "Деревянный обеденный стол",
                "desc_en": "Solid oak dining table for 6 people",
                "desc_ru": "Обеденный стол из массива дуба на 6 персон",
                "price": Decimal("450.00"),
                "article_number": 1000005,
            },
        ]

        products = []
        for i, p in enumerate(products_data, start=1):
            product = Product()
            product.subcategory = p["subcategory"]
            product.product_name_en = p["name_en"]
            product.product_name_ru = p["name_ru"]
            product.description_en = p["desc_en"]
            product.description_ru = p["desc_ru"]
            product.product_price = p["price"]
            product.article_number = p["article_number"]
            product.product_type = True
            product.product_image = fake_image(f"product_{i}.gif")
            product.save()
            products.append(product)
        self.stdout.write(self.style.SUCCESS(f"Создано товаров: {len(products)}"))

        # ---------------------------------------------------------
        # 5. ProductImages (доп. изображения к товарам)
        # ---------------------------------------------------------
        product_images_count = 0
        for product in products:
            for j in range(1, 3):  # по 2 доп. фото на товар
                ProductImages.objects.create(
                    product=product,
                    product_image=fake_image(f"{product.product_name_en}_{j}.gif"),
                )
                product_images_count += 1
        self.stdout.write(
            self.style.SUCCESS(f"Создано доп. изображений товаров: {product_images_count}")
        )

        # ---------------------------------------------------------
        # 6. Review (отзывы пользователей на товары)
        # ---------------------------------------------------------
        reviews_data = [
            {"user": users[0], "product": products[0], "stars": "5", "comment": "Отличный телефон!"},
            {"user": users[1], "product": products[0], "stars": "4", "comment": "Хороший, но дорогой."},
            {"user": users[2], "product": products[1], "stars": "5", "comment": "Быстрый и легкий ноутбук."},
            {"user": users[3], "product": products[2], "stars": "3", "comment": "Куртка нормальная, размер маломерит."},
            {"user": users[0], "product": products[3], "stars": "5", "comment": "Прекрасное платье на лето!"},
            {"user": users[1], "product": products[4], "stars": "4", "comment": "Качественный стол, сборка простая."},
        ]

        reviews = []
        for i, r in enumerate(reviews_data, start=1):
            review = Review.objects.create(
                user=r["user"],
                product=r["product"],
                stars=r["stars"],
                comment=r["comment"],
                review_image=fake_image(f"review_{i}.gif"),
            )
            reviews.append(review)
        self.stdout.write(self.style.SUCCESS(f"Создано отзывов: {len(reviews)}"))

        self.stdout.write(self.style.SUCCESS("Наполнение базы данными завершено успешно!"))