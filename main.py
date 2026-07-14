from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Hello from CIT Backend Course!"}

    from fastapi import FastAPI

app = FastAPI(title="My BackendAPI")

@app.get("/")
def root():
    return{"message":"Hello from CIT Backend Course!"}


from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="My Backend API")

products = [
    {"id": 1, "name": "Laptop", "price": 75000},
    {"id": 2, "name": "Mouse", "price": 1500},
    {"id": 3, "name": "Keyboard", "price": 3500},
]

class ProductCreate(BaseModel):
    name: str
    price: float

@app.get("/")
def root():
    return {"message": "Hello from CIT Backend Course!"}

@app.get("/welcome/{name}")
def welcome(name: str):
    return {"message": f"Welcome, {name}!"}

@app.get("/calculate")
def calculate(a: float, b: float, operation: str = "add"):
    if operation == "add":
        return {"result": a + b}
    elif operation == "subtract":
        return {"result": a - b}
    elif operation == "multiply":
        return {"result": a * b}
    elif operation == "divide":
        if b == 0:
            return {"error": "Division by zero"}
        return {"result": a / b}
    return {"error": "Invalid operation"}

@app.get("/products")
def get_products():
    return products

@app.get("/products/search")
def search_products(q: str):
    return [p for p in products if q.lower() in p["name"].lower()]

@app.get("/products/{product_id}")
def get_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return p
    return {"error": "Product not found"}

@app.post("/products")
def create_product(product: ProductCreate):
    new_id = len(products) + 1
    new_product = {"id": new_id, "name": product.name, "price": product.price}
    products.append(new_product)
    return {"message": "Product created", "product": new_product}