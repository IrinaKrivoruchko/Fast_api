from typing import List

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from py_model import ProductCreate, ProductResponse, CategoryCreate, CategoryResponse
from alchemy_models import Product, Category, get_db
from starlette.responses import JSONResponse
from dummyjson_parser import run_parse_tasks

# init fast api app
app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

# crud operation for User model
@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/product_create", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    test_val = product.model_dump()
    db_product = Product(**test_val)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/products", response_model=List[ProductResponse])
def read_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    if products is None:
        raise HTTPException(status_code=404, detail="not found")
    return products


@app.post("/category_create/", response_model=CategoryResponse)
def create_category(post: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(**post.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for attr, value in product.dict().items():
        setattr(db_product, attr, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return "ok"

@app.post("/dummysaver")
def dummy_parser(task: BackgroundTasks, db: Session = Depends(get_db)):
    run_parse_tasks(task, db)
    return JSONResponse({"task": "Start parse dummyjson"})

if __name__ == "__main__":
    import uvicorn
    from alchemy_models import SessionLocal

    uvicorn.run(app, host="127.0.0.1", port=8000)
