import requests

Categories_URL = 'https://dummyjson.com/products/categories'

def get_categories():
    resp = requests.get(Categories_URL)
    return resp.json()

