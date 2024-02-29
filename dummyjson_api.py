import requests

Categories_URL = 'https://dummyjson.com/products/categories'
Products_URL = 'https://dummyjson.com/products'

def get_categories_api():
    resp_cat = requests.get(Categories_URL)
    return resp_cat.json()

def get_products_api():
    resp_prod = requests.get(Products_URL)
    return resp_prod.json()