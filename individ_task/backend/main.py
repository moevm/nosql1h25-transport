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

db = client.auto_db
car_collection = db.cars

class Car(BaseModel):
    registration_number: str
    category: str
    model: str 
    year: int
    

@app.get("/cars", response_model=List[Car])
async def get_cars(
    type_registration_number: Optional[str] = Query(None),
    type_category: Optional[str] = Query(None),
    type_model: Optional[str] = Query(None),
    type_year: Optional[int] = Query(None)
):
    query = {}
    if type_registration_number:
        query["registration_number"] = {"$regex": type_registration_number, "$options": "i"}  
    if type_category:
        query["category"] = {"$regex": type_category, "$options": "i"}
    if type_model:
        query["model"] = {"$regex": type_model, "$options": "i"}
    if type_year:
        query["year"] = {"$regex": type_year, "$options": "i"}
    cars = await car_collection.find(query).to_list(100)
    return cars

@app.get("/cars/{registration_number}", response_model=Car)
async def get_cars_by_registration_number(registration_number: str):
    cars_item = await car_collection.find_one({"registration_number": registration_number})
    if not cars_item:
        raise HTTPException(status_code=404, detail="Customer not found")
    return cars_item

@app.post("/cars")
async def create_car(car: Car):
    await car_collection.insert_one(car.dict())
    return {"message": "Customer added"}

@app.put("/cars/{registration_number}")
async def update_car(registration_number: str, car: Car):
    result = await car_collection.update_one({"registration_number": registration_number}, {"$set": car.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer updated"}

@app.delete("/cars/{registration_number}")
async def delete_car(registration_number: str):
    result = await car_collection.delete_one({"registration_number": registration_number})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted"}

@app.get("/cars/export")
async def export_cars():
    cars = await car_collection.find().to_list(100)
    for d in cars:
        d.pop("_id", None)
    return cars

@app.post("/cars/import")
async def import_cars(cars: List[Any] = Body(...)):
    cleaned_cars = []
    for d in cars:
        d.pop("_id", None)
        try:
            car = Car(**d)
            cleaned_cars.append(car.dict())
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid customer data: {d}, error: {e}")
    await car_collection.delete_many({})
    await car_collection.insert_many(cleaned_cars)
    return {"message": "Customers imported"} 




master_collection = db.masters

class Master(BaseModel):
    name: str
    qualification: str
    experience_years: int
    is_available: bool
    comments: Optional[str] = None
    
    

@app.get("/masters", response_model=List[Master])
async def get_masters(
    type_name: Optional[str] = Query(None),
    type_comments: Optional[str] = Query(None),
    type_qualification: Optional[str] = Query(None),
    min_experience: Optional[int] = Query(None),
    max_experience: Optional[int] = Query(None),
    is_available: Optional[bool] = Query(None)
):
    query = {}
    if type_name:
        query["name"] = {"$regex": type_name, "$options": "i"}
    if type_comments:
        query["comments"] = {"$regex": type_comments, "$options": "i"}
    if type_qualification:
        query["qualification"] = {"$regex": type_qualification, "$options": "i"}
    if min_experience is not None or max_experience is not None:
        query["experience_years"] = {}
        if min_experience is not None:
            query["experience_years"]["$gte"] = min_experience
        if max_experience is not None:
            query["experience_years"]["$lte"] = max_experience
    if is_available is not None:
        query["is_available"] = is_available
    masters = await master_collection.find(query).to_list(100)
    return masters

@app.post("/masters")
async def create_master(master: Master):
    await master_collection.insert_one(master.dict())
    return {"message": "Driver added"}

@app.put("/masters/{name}")
async def update_master(name: str, master: Master):
    existing = await master_collection.find_one({"name": name})
    if not existing:
        raise HTTPException(status_code=404, detail="Driver not found")

   
    result = await master_collection.update_one({"name": name},{"$set": master.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Driver not found")
    return {"message": "Driver updated"}

@app.delete("/masters/{name}")
async def delete_master(name: str):
    result = await master_collection.delete_one({"name": name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Driver not found")
    return {"message": "Driver deleted"}

@app.get("/masters/export")
async def export_masters():
    masters = await master_collection.find().to_list(100)
    for d in masters:
        d.pop("_id", None)
    return masters

@app.post("/masters/import")
async def import_masters(masters: List[Any] = Body(...)):
    cleaned_masters = []
    for d in masters:
        d.pop("_id", None)
        try:
            master = Master(**d)
            cleaned_masters.append(master.dict())
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid driver data: {d}, error: {e}")
    await master_collection.delete_many({})
    await master_collection.insert_many(cleaned_masters)
    return {"message": "Drivers imported"}



garage_collection = db.garages

class Garage(BaseModel):
    garage_id: str 
    address: str
    is_available: bool
    comments: Optional[str] = None

@app.get("/garages", response_model=List[Garage])
async def get_garages(
    type_garage_id: Optional[str] = Query(None),
    type_address: Optional[str] = Query(None),
    available: Optional[str] = Query(None),
    type_comments: Optional[str] = Query(None)
):
    query = {}
    if type_garage_id:
        query["garage_id"] = {"$regex": type_garage_id, "$options": "i"} 
    if type_address:
        query["address"] = {"$regex": type_address, "$options": "i"} 
    if available:
        query["is_available"] = {"$regex": available, "$options": "i"} 
    if type_comments:
        query["comments"] = {"$gte": type_comments}
    
    garages = await garage_collection.find(query).to_list(100)
    return garages

@app.get("/garages/{garage_id}", response_model=Garage)
async def get_garages_by_rent_id(garage_id: str):
    garages_item = await garage_collection.find_one({"garage_id": garage_id})
    if not garages_item:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return garages_item

@app.post("/garages")
async def create_garage(garage: Garage):
    await garage_collection.insert_one(garage.dict())
    return {"message": "Transaction added"}

@app.put("/garages/{garage_id}")
async def update_garage(garage_id: str, garage: Garage):
    result = await garage_collection.update_one({"garage_id": garage_id}, {"$set": garage.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction updated"}

@app.delete("/garages/{garage_id}")
async def delete_garage(garage_id: str):
    result = await garage_collection.delete_one({"garage_id": garage_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted"}

@app.get("/garages/export")
async def export_garages():
    garages = await garage_collection.find().to_list(100)
    for d in garages:
        d.pop("_id", None)
    return garages

@app.post("/garages/import")
async def import_garages(garages: List[Any] = Body(...)):
    cleaned_garages = []
    for d in garages:
        d.pop("_id", None)
        try:
            garage = Garage(**d)
            cleaned_garages.append(garage.dict())
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid transaction data: {d}, error: {e}")
    await garage_collection.delete_many({})
    await garage_collection.insert_many(cleaned_garages)
    return {"message": "Transactions imported"} 



flight_collection = db.flights

class Flight(BaseModel):
    flight_id: str 
    master_name: str
    registration_number: str
    garage_id: str
    date_of_begining: str
    date_of_ending: str
    comments: Optional[str] = None

@app.get("/flights", response_model=List[Flight])
async def get_flights(
    type_flight_id: Optional[str] = Query(None),
    type_master_name: Optional[str] = Query(None),
    type_registration_number: Optional[str] = Query(None),
    type_garage_id: Optional[str] = Query(None),
    type_date_of_begining_from: Optional[str] = Query(None),
    type_date_of_begining_to: Optional[str] = Query(None),
    type_date_of_ending_from: Optional[str] = Query(None),
    type_date_of_ending_to: Optional[str] = Query(None),
    type_comments: Optional[str] = Query(None)
):
    query = {}
    if type_flight_id:
        query["flight_id"] = {"$regex": type_flight_id, "$options": "i"} 
    if type_master_name:
        query["master_name"] = {"$regex": type_master_name, "$options": "i"} 
    if type_registration_number:
        query["registration_number"] = {"$regex": type_registration_number, "$options": "i"} 
    if type_garage_id:
        query["garage_id"] = {"$regex": type_garage_id, "$options": "i"} 
    if type_date_of_begining_from:
        query["date_of_begining"] = {"$regex": type_date_of_begining_from, "$options": "i"} 
    if type_date_of_begining_to:
        query["date_of_begining"] = {"$regex": type_date_of_begining_to, "$options": "i"} 
    if type_date_of_ending_from:
        query["date_of_ending"] = {"$regex": type_date_of_ending_from, "$options": "i"} 
    if type_date_of_ending_to:
        query["date_of_ending"] = {"$regex": type_date_of_ending_to, "$options": "i"} 
    if type_comments:
        query["comments"] = {"$regex": type_comments, "$options": "i"}
    flights = await flight_collection.find(query).to_list(100)
    return flights

@app.get("/flights/{flight_id}", response_model=Flight)
async def get_flights_by_flight_id(flight_id: str):
    flights_item = await flight_collection.find_one({"flight_id": flight_id})
    if not flights_item:
        raise HTTPException(status_code=404, detail="TC not found")
    return flights_item

@app.post("/flights")
async def create_flight(flight: Flight):
    await flight_collection.insert_one(flight.dict())
    return {"message": "TC added"}

@app.put("/flights/{flight_id}")
async def update_flight(flight_id: str, flight: Flight):
    result = await flight_collection.update_one({"flight_id": flight_id}, {"$set": flight.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="TC not found")
    return {"message": "TC updated"}

@app.delete("/flights/{flight_id}")
async def delete_flight(flight_id: str):
    result = await flight_collection.delete_one({"flight_id": flight_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="TC not found")
    return {"message": "TC deleted"}

@app.get("/flights/export")
async def export_flights():
    flights = await flight_collection.find().to_list(100)
    for d in flights:
        d.pop("_id", None)
    return flights

@app.post("/flights/import")
async def import_flights(flights: List[Any] = Body(...)):
    cleaned_flights = []
    for d in flights:
        d.pop("_id", None)
        try:
            flight = Flight(**d)
            cleaned_flights.append(flight.dict())
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid tc data: {d}, error: {e}")
    await flight_collection.delete_many({})
    await flight_collection.insert_many(cleaned_flights)
    return {"message": "Tcs imported"} 