from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

class Product(BaseModel):
    name:str
    price: float
    
@app.get('/all_products')
def get_products():
    try:
        with open("products.json", 'r') as f:
            data = json.load(f)
    except:
        data = []

    return data


@app.post('/create_product')
def create_product(product: Product):
    try:
        with open('products.json') as f:
            data = json.load(f)
    except:
        data = []

    new_id = len(data) + 1

    product_data = {
        "id": new_id,
        "name": product.name,
        "price": product.price
    }

    data.append(product_data)

    with open('products.json', 'w') as f:
        json.dump(data, f, indent=4)
    return {"SUCCESS added_product": product_data}


@app.put("/update_product/{product_id}")
def update_product(product_id: int, product:Product):
    try:
        with open("products.json") as f:
            data = json.load(f)
    except:
        return "product not found"
    
    for i in data:
        if i["id"] == product_id:
            i["name"] = product.name
            i["price"] = product.price

            with open("products.json", 'w') as f:
                json.dump(data, f, indent=4)
            return {"update_product": i}
        
    return {"error": "product not found"}