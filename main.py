from fastapi import FastAPI, Depends, HTTPException
import notion as nt

app = FastAPI()

#read
@app.get("/customers", tags = ["read"])
async def read_customer():
    res = nt.read_db()

    if res == None:
        return {"message": "No customers found"}
    
    return {"list of customers": nt.display_db()}

@app.get("/customers/{customer_id}", tags = ["read"])    
async def read_customer(customer_id: str):
    res = nt.read_db()

    if res == None:
        return {"message": "No customers found"}
    
    return {"customer data": nt.get_customer_data(customer_id)}

#create
@app.post("/customers/{customer_id}", tags = ["create"])
async def create_customer(customer_id: str, data: dict | None = None):
    db = nt.read_db()

    if db == None:
        nt.create_customer(customer_id, data)
        return {"message": "Customer created successfully"}
    else:
        for i in range(len(db)):
            if db[i]["child_database"]["title"] == customer_id:
                raise HTTPException(status_code=404, detail="Customer already exists")
        nt.create_customer(customer_id, data)
        return {"message": "Customer created successfully"}

@app.post("/customers/{customer_id}/data", tags = ["create"])   
async def add_data(customer_id: str, data: dict):
    db = nt.read_db()

    if db == None:
        raise HTTPException(status_code=404, detail="Database not found")
    else:
        for i in range(len(db)):
            if db[i]["child_database"]["title"] == customer_id:
                nt.add_data(db[i]["id"], data)
                return {"message": "Data added successfully"}
        raise HTTPException(status_code=404, detail="Customer not found")
    
#update
@app.put("/customers/{customer_id}", tags=["update"])
async def rename_customer(customer_id: str, new_customer_id: str):
    db = nt.read_db()

    if db == None:
        raise HTTPException(status_code=404, detail="Database not found")
    else:
        for i in range(len(db)):
            if db[i]["child_database"]["title"] == customer_id:
                success = nt.changeID(new_customer_id, db[i]["id"])
                if not success:
                    raise HTTPException(status_code=400, detail="Failed to rename customer")
                return {"message": "Customer renamed successfully"}

        raise HTTPException(status_code=404, detail="Customer not found")

@app.put("/customers/{customer_id}/data", tags=["update"])
async def update_customer(customer_id: str, data: dict, data_id: str):
    db = nt.read_db()

    if db == None:
        raise HTTPException(status_code=404, detail="Database not found")
    else:
        for i in range(len(db)):
            if db[i]["child_database"]["title"] == customer_id:
                tmp = nt.update_customer_db(db[i]["id"], data, data_id)
                if not tmp:
                    raise HTTPException(status_code=400, detail="Failed to update data")
                return {"message": "Data updated successfully"}
        raise HTTPException(status_code=404, detail="Customer not found")
    

#delete
@app.delete("/customers/{customer_id}", tags=["delete"])
async def delete_customer(customer_id: str):
    db = nt.read_db()
    if db == None:
        raise HTTPException(status_code=404, detail="Database not found")
    else:
        for i in range(len(db)):
            if db[i]["child_database"]["title"] == customer_id:
                tmp = nt.delete_customer_db(db[i]["id"])
                return {"message": "Customer deleted successfully"}
        raise HTTPException(status_code=404, detail="Customer not found")

@app.delete("/customers/{customer_id}/data", tags=["delete"])
async def delete_data(customer_id: str, data_id: str):
    db = nt.read_db()

    if db is None:
        raise HTTPException(status_code=404, detail="Database not found")
    else:
        for i in range(len(db)):
            if db[i]["child_database"]["title"] == customer_id:
                result = nt.delete_data(db[i]["id"], data_id)
                if result["message"] != "Data deleted successfully":
                    raise HTTPException(status_code=400, detail=result["message"])
                return result
        raise HTTPException(status_code=404, detail="Customer not found") 