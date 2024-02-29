from fastapi import BackgroundTasks
import json

from alchemy_models import Category, Product
from dummyjson_api import get_categories_api, get_products_api
from sqlalchemy.orm import Session
from sqlalchemy import func


def run_parse_tasks(task: BackgroundTasks, db: Session):
    task.add_task(parse_products, db)
    task.add_task(parse_categories, db)
    print("start")


def parse_products(db: Session):
    row_count = db.query(func.count()).select_from(Product).scalar()
    if row_count > 0:
        return

    products_resp = get_products_api()
    save_products(products_resp, db)


def parse_categories(db: Session):
    row_count = db.query(func.count()).select_from(Category).scalar()
    if row_count > 0:
        return

    categories_resp = get_categories_api()
    save_categories(categories_resp, db)


def save_categories(categories_resp, db: Session):
    for category_title in categories_resp:
        category = Category(title=category_title)
        db.add(category)

    db.commit()


def save_products(products_resp, db: Session):

    for product_data in products_resp['products']:

        product = Product()

        product.id = product_data['id']
        product.title = product_data['title']
        product.description = product_data['description']
        product.price = product_data['price']
        product.brand = product_data['brand']
        product.category = product_data['category']

        db.add(product)

    db.commit()
