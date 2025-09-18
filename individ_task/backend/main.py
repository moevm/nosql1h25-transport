from fastapi import FastAPI, HTTPException, Query, Body
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import date
import motor.motor_asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongodb:27017")

db = client.transport_db
customer_collection = db.customers

class Customer(BaseModel):
    login: str
    password: str
    name: str 
    address: str
    contact_information: str
    comments: Optional[str] = None

@app.get("/customers", response_model=List[Customer])
async def get_customers(
    type_name: Optional[str] = Query(None),
    type_contact_information: Optional[str] = Query(None),
    type_address: Optional[str] = Query(None),
    type_comments: Optional[str] = Query(None)
):
    query = {}
    if type_name:
        query["name"] = {"$regex": type_name, "$options": "i"}  
    if type_contact_information:
        query["contact_information"] = {"$regex": type_contact_information, "$options": "i"}
    if type_address:
        query["address"] = {"$regex": type_address, "$options": "i"}
    if type_comments:
        query["comments"] = {"$regex": type_comments, "$options": "i"}
    customers = await customer_collection.find(query).to_list(100)
    return customers

@app.get("/customers/{name}", response_model=Customer)
async def get_customers_by_name(name: str):
    customers_item = await customer_collection.find_one({"name": name})
    if not customers_item:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customers_item

@app.post("/customers")
async def create_customer(customer: Customer):
    await customer_collection.insert_one(customer.dict())
    return {"message": "Customer added"}

@app.put("/customers/{name}")
async def update_customer(name: str, customer: Customer):
    result = await customer_collection.update_one({"name": name}, {"$set": customer.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer updated"}

@app.delete("/customers/{name}")
async def delete_customer(name: str):
    result = await customer_collection.delete_one({"name": name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted"}

@app.get("/customers/export")
async def export_customers():
    customers = await customer_collection.find().to_list(100)
    for d in customers:
        d.pop("_id", None)
    return customers

@app.post("/customers/import")
async def import_customers(customers: List[Any] = Body(...)):
    cleaned_customers = []
    for d in customers:
        d.pop("_id", None)
        try:
            customer = Customer(**d)
            cleaned_customers.append(customer.dict())
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid customer data: {d}, error: {e}")
    await customer_collection.delete_many({})
    await customer_collection.insert_many(cleaned_customers)
    return {"message": "Customers imported"} 




tc_collection = db.tcs

class TC(BaseModel):
    type_tc: str 
    registration_number: str
    is_available: bool
    comments: Optional[str] = None

@app.get("/tcs", response_model=List[TC])
async def get_tcs(
    type_registration_number: Optional[str] = Query(None),
    type_tcs: Optional[str] = Query(None),
    is_available: Optional[bool] = Query(None),
    type_comments: Optional[str] = Query(None)
):
    query = {}
    if type_tcs:
        query["type_tc"] = {"$regex": type_tcs, "$options": "i"} 
    if type_registration_number:
        query["registration_number"] = {"$regex": type_registration_number, "$options": "i"} 
    if is_available is not None:
        query["is_available"] = is_available
    if type_comments:
        query["comments"] = {"$regex": type_comments, "$options": "i"}
    tcs = await tc_collection.find(query).to_list(100)
    return tcs

@app.get("/tcs/{registration_number}", response_model=TC)
async def get_tcs_by_registration_number(registration_number: str):
    tcs_item = await tc_collection.find_one({"registration_number": registration_number})
    if not tcs_item:
        raise HTTPException(status_code=404, detail="TC not found")
    return tcs_item

@app.post("/tcs")
async def create_tc(tc: TC):
    await tc_collection.insert_one(tc.dict())
    return {"message": "TC added"}

@app.put("/tcs/{registration_number}")
async def update_tc(registration_number: str, tc: TC):
    result = await tc_collection.update_one({"registration_number": registration_number}, {"$set": tc.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="TC not found")
    return {"message": "TC updated"}

@app.delete("/tcs/{registration_number}")
async def delete_tc(registration_number: str):
    result = await tc_collection.delete_one({"registration_number": registration_number})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="TC not found")
    return {"message": "TC deleted"}

@app.get("/tcs/export")
async def export_tcs():
    tcs = await tc_collection.find().to_list(100)
    for d in tcs:
        d.pop("_id", None)
    return tcs

@app.post("/tcs/import")
async def import_tcs(tcs: List[Any] = Body(...)):
    cleaned_tcs = []
    for d in tcs:
        d.pop("_id", None)
        try:
            tc = TC(**d)
            cleaned_tcs.append(tc.dict())
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid tc data: {d}, error: {e}")
    await tc_collection.delete_many({})
    await tc_collection.insert_many(cleaned_tcs)
    return {"message": "Tcs imported"} 



rent_collection = db.rents

class Rent(BaseModel):
    rent_id: str 
    date_of_begining: str
    date_of_ending: str
    order_name: str
    tc_registration_number: str

@app.get("/rents", response_model=List[Rent])
async def get_rents(
    type_order_name: Optional[str] = Query(None),
    type_registration_number: Optional[str] = Query(None),
    type_rent_id: Optional[str] = Query(None),
    date_of_begining_to: Optional[str] = Query(None),
    date_of_begining_from: Optional[str] = Query(None),
    date_of_ending_to: Optional[str] = Query(None),
    date_of_ending_from: Optional[str] = Query(None)
):
    query = {}
    if type_order_name:
        query["order_name"] = {"$regex": type_order_name, "$options": "i"} 
    if type_registration_number:
        query["registration_number"] = {"$regex": type_registration_number, "$options": "i"} 
    if type_rent_id:
        query["rent_id"] = {"$regex": type_rent_id, "$options": "i"} 
    if date_of_begining_from:
        query["date_of_begining"] = {"$gte": date_of_begining_from}
    if date_of_begining_to:
        query["date_of_begining"] = {"$lte": date_of_begining_to}
    if date_of_ending_from:
        query["date_of_ending"] = {"$gte": date_of_ending_from}
    if date_of_ending_to:
        query["date_of_ending"] = {"$lte": date_of_ending_to}
    rents = await rent_collection.find(query).to_list(100)
    return rents

@app.get("/rents/{rent_id}", response_model=Rent)
async def get_rents_by_rent_id(rent_id: str):
    rents_item = await rent_collection.find_one({"rent_id": rent_id})
    if not rents_item:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return rents_item

@app.post("/rents")
async def create_rent(rent: Rent):
    await rent_collection.insert_one(rent.dict())
    return {"message": "Transaction added"}

@app.put("/rents/{rent_id}")
async def update_rent(rent_id: str, rent: Rent):
    result = await rent_collection.update_one({"rent_id": rent_id}, {"$set": rent.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction updated"}

@app.delete("/rents/{rent_id}")
async def delete_rent(rent_id: str):
    result = await rent_collection.delete_one({"rent_id": rent_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted"}

@app.get("/rents/export")
async def export_rents():
    rents = await rent_collection.find().to_list(100)
    for d in rents:
        d.pop("_id", None)
    return rents

@app.post("/rents/import")
async def import_rents(rents: List[Any] = Body(...)):
    cleaned_rents = []
    for d in rents:
        d.pop("_id", None)
        try:
            rent = Rent(**d)
            cleaned_rents.append(rent.dict())
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid transaction data: {d}, error: {e}")
    await rent_collection.delete_many({})
    await rent_collection.insert_many(cleaned_rents)
    return {"message": "Transactions imported"} 
