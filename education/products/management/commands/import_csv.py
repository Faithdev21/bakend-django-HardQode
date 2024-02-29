from csv import DictReader

from django.core.management import BaseCommand
from django.db import IntegrityError

from products.models import Product, User


class Command(BaseCommand):
    """Load CSV data into database"""
    def handle(self, *args, **kwargs):
        for row in DictReader(open('./data/products.csv', encoding='utf-8')):
            try:
                ingredient = Product(
                    title=row['title'],
                    start_date=row['start_date'],
                    cost=row['cost'],
                    min_group_users=row['min_group_users'],
                    max_group_users=row['max_group_users'],
                    creator_id=row['creator_id']
                )
                ingredient.save()
            except IntegrityError:
                print("Product with same title already created!")
        print("Products ready!")

        for row in DictReader(open('./data/users.csv', encoding='utf-8')):
            try:
                user = User(
                    password=row['password'],
                    email=row['email'],
                    username=row['username']
                )
                user.save()
            except IntegrityError:
                print("User with same data already created!")
        print("Users ready!")
