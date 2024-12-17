from fastapi import FastAPI, Depends, HTTPException
from notion import *

app = FastAPI()

#read
@app.get("/customers")
async def read_customer():
    display_db()

@app.get("/customers/{customer_id}")    
async def read_customer(customer_id: int):
    get_customer_data(customer_id)

#create
@app.post("/customers/{customer_id}")
async def create_customer(customer_id: str, data: dict):
    db = read_db()

    if db == None:
        create_customer(customer_id, data)
        return {"message": "Customer created successfully"}
    else:
        for i in range(len(db)):
            if db[i]["child_database"]["title"] == customer_id:
                raise HTTPException(status_code=404, detail="Customer already exists")
        create_customer(customer_id, data)
        return {"message": "Customer created successfully"}

@app.post("/customers/{customer_id}")   
async def add_data(customer_id: str, data: dict):
    db = read_db()

    if db == None:
        raise HTTPException(status_code=404, detail="Database not found")
    else:
        for i in range(len(db)):
            if db[i]["child_database"]["title"] == customer_id:
                add_data(customer_id, data)
                return {"message": "Data added successfully"}
        raise HTTPException(status_code=404, detail="Customer not found")
    

#update
@app.put("/customers/{customer_id}")
async def update_customer(customer_id: int):
    pass

#delete
@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int):
    pass
