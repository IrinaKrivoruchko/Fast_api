from fastapi import BackgroundTasks
from dummyjson_api import get_categories

def parse(task: BackgroundTasks):
    task.add_task(parse_products)
    task.add_task(parse_categories)
    print("start")

def parse_products():
    print("parse products")

def parse_categories():
    categories_resp = get_categories()
    print("parse category")