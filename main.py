from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import json

app = FastAPI()

class ProductParial(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None

class Product(BaseModel):
    name: str
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
        with open("products.json", 'r') as f:
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


@app.patch("/update_product_partial/{product_id}")
def partial_update_product(product_id: int, product:ProductParial):
    try:
        with open('products.json', 'r') as f:
            data = json.load(f)
    except:
        return {"error": "product empty"}
    
    for i in data:
        if i["id"] == product_id:
            if product.name is not None:
                i["name"] = product.name
            if product.price is not None:
                i['price'] = product.price
            
            with open("products.json", 'w') as f:
                json.dump(data, f, indent=4)
            return {"SUCCESS update_product": i}
            
    return {"error": "product not found"}


@app.delete("/delete_product/{product_id}")
def delete_product(product_id: int):
    try:
        with open("products.json", 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        return {"error": "file not found"}
    
    for i, p in enumerate(data):
        if p["id"] == product_id:
            delete_p = data.pop(i)
            with open("products.json", 'w') as f:
                json.dump(data, f, indent=4)
            return {"SUCCESS": f'object deleted {delete_p}'}
    return {"error": "product not found"}


############# employees ///////


class Employee(BaseModel):
    fullname: str
    year: int

class PartialEmployee(BaseModel):
    fullname: Optional[str] = None
    year: Optional[int] = None


@app.get("/all_employees")
def get_employees():
    try:
        with open("employees.json", 'r') as f:
            data = json.load(f)
    except:
        data = []
    
    return data


@app.post('/create_employee')
def create_employee(employee: Employee):
    try:
        with open('employees.json', 'r') as f:
            data = json.load(f)
    except:
        data = []
    
    new_id = len(data) + 1

    employee_data = {
        "id": new_id,
        "fullname": employee.fullname,
        "year": employee.year
    }

    data.append(employee_data)

    with open("employees.json", 'w') as f:
        json.dump(data, f, indent=4)
    return {"SUCCESS object added": employee_data}


@app.put("/update_employee/{employee_id}")
def update_employee(employee_id: int, employee: Employee):
    try:
        with open("employees.json", 'r') as f:
            data = json.load(f)
    except:
        return {"error": "No employee found"}
    
    for i in data:
        if i["id"] == employee_id:
            i["fullname"] = employee.fullname
            i["year"] = employee.year

            with open("employees.json", 'w') as f:
                json.dump(data, f, indent=4)
            return {"SUCCESS oject added": i}
    return {"error": "object not found"}


@app.patch("/update_partial_employee/{employee_id}")
def partial_employee_update(employee_id: int, employee: PartialEmployee):
    try:
        with open("employees.json", 'r') as f:
            data = json.load(f)
    except:
        return {"error": "NO employee found"}

    for i in data:
        if i["id"] == employee_id:
            if employee.fullname is not None:
                i["fullname"] = employee.fullname
            if employee.year is not None:
                i["year"] = employee.year
            
            with open("employees.json", 'w') as f:
                json.dump(data, f, indent=4)
            return {'success': i}
        
    return {'error': 'employee not found'}


@app.delete("/delete_employee/{employee_id}")
def delete_employee(employee_id: int):
    try:
        with open("employees.json", 'r') as f:
            data = json.load(f)
    except:
        return {"error": "Employee not found"}
    
    for i, p, in enumerate(data):
        if p["id"] == employee_id:
            delete_employee = data.pop(i)

            with open("employees.json", 'w') as f:
                json.dump(data, f, indent=4)
            return {"success object_deleted": delete_employee}
    return {"error": "object not found"}