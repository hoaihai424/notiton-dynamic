from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

@app.get("/customers")
async def read_customer():
    pass

@app.get("/customers/{customer_id}")    
async def read_customer(customer_id: int):
    pass

@app.get("/customers/{customer_id}/database")
async def read_customer_database(customer_id: int):
    pass

@app.post("/customers")
async def create_customer():
    pass

@app.put("/customers/{customer_id}")
async def update_customer(customer_id: int):
    pass

