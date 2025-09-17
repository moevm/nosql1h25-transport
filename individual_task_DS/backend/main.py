from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime, timedelta, time
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
car_collection = db.cars

class ServiceEpisode(BaseModel):
    date: str
    description: str
    replaced_parts: List[str] = []
    mileage: Optional[int] = None
    cost: Optional[float] = None

class Car(BaseModel):
    name: str
    model: str
    license_plate: str
    category: Optional[str] = None
    year: int
    service_history: List[ServiceEpisode] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@app.get("/cars", response_model=List[Car])
async def get_cars(
    name: Optional[str] = None,
    model: Optional[str] = None,
    license_plate: Optional[str] = None,
    category: Optional[str] = Query(None),
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    created_from: Optional[str] = None,
    created_to: Optional[str] = None,
    updated_from: Optional[str] = None,
    updated_to: Optional[str] = None
):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if model:
        query["model"] = {"$regex": model, "$options": "i"}
    if license_plate:
        query["license_plate"] = {"$regex": license_plate, "$options": "i"}
    if category:
        query["category"] = {"$regex": category, "$options": "i"}
    if min_year or max_year:
        query["year"] = {}
        if min_year: query["year"]["$gte"] = min_year
        if max_year: query["year"]["$lte"] = max_year
    if created_from or created_to:
        query["created_at"] = {}
        if created_from: query["created_at"]["$gte"] = datetime.fromisoformat(
            created_from)
        if created_to: query["created_at"]["$lte"] = datetime.fromisoformat(created_to)
    if updated_from or updated_to:
        query["updated_at"] = {}
        if updated_from: query["updated_at"]["$gte"] = datetime.fromisoformat(
            updated_from)
        if updated_to: query["updated_at"]["$lte"] = datetime.fromisoformat(updated_to)

    cars = await car_collection.find(query).to_list(200)
    for c in cars:
        c.pop("_id", None)
    return cars

@app.post("/cars")
async def create_car(car: Car):
    car.created_at = datetime.utcnow() + timedelta(hours=3)
    car.updated_at = datetime.utcnow() + timedelta(hours=3)
    await car_collection.insert_one(car.dict())
    return {"message": "Car added"}

@app.put("/cars/{license_plate}")
async def update_car(license_plate: str, car: Car):
    existing = await car_collection.find_one({"license_plate": license_plate})
    if not existing:
        raise HTTPException(status_code=404, detail="Car not found")

    car.created_at = existing.get("created_at")
    car.updated_at = datetime.utcnow() + timedelta(hours=3)

    result = await car_collection.update_one(
        {"license_plate": license_plate},
        {"$set": car.dict()}
    )
    return {"message": "Car updated"}

@app.delete("/cars/{license_plate}")
async def delete_car(license_plate: str):
    result = await car_collection.delete_one({"license_plate": license_plate})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Car deleted"}

@app.get("/service_search")
async def service_search(
    description: Optional[str] = None,
    replaced_part: Optional[str] = None,
    min_date: Optional[str] = None,
    max_date: Optional[str] = None,
    min_mileage: Optional[int] = None,
    max_mileage: Optional[int] = None,
    min_cost: Optional[float] = None,
    max_cost: Optional[float] = None
):
    cond = {}

    if description:
        cond["description"] = {"$regex": description, "$options": "i"}
    if replaced_part:
        cond["replaced_parts"] = {"$elemMatch": {"$regex": replaced_part, "$options": "i"}}
    if min_date or max_date:
        cond["date"] = {}
        if min_date:
            cond["date"]["$gte"] = datetime.fromisoformat(min_date)
        if max_date:
            cond["date"]["$lte"] = datetime.fromisoformat(max_date)
    if min_mileage or max_mileage:
        cond["mileage"] = {}
        if min_mileage:
            cond["mileage"]["$gte"] = min_mileage
        if max_mileage:
            cond["mileage"]["$lte"] = max_mileage
    if min_cost or max_cost:
        cond["cost"] = {}
        if min_cost:
            cond["cost"]["$gte"] = min_cost
        if max_cost:
            cond["cost"]["$lte"] = max_cost

    query = {}
    if cond:
        query["service_history"] = {"$elemMatch": cond}

    cars = await car_collection.find(query).to_list(200)

    for c in cars:
        c.pop("_id", None)
    return cars


@app.get("/cars/export")
async def export_cars():
    cars = await car_collection.find().to_list(100)
    for c in cars:
        c.pop("_id", None)
    return cars

@app.post("/cars/import")
async def import_cars(cars: List[Any] = Body(...)):
    cleaned = []
    for c in cars:
        c.pop("_id", None)
        try:
            car = Car(**c)
            car.created_at = car.created_at or datetime.utcnow()
            car.updated_at = datetime.utcnow()
            cleaned.append(car.dict())
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid car: {c}, error: {e}")
    await car_collection.delete_many({})
    await car_collection.insert_many(cleaned)
    return {"message": "Cars imported"}

@app.get("/cars/{license_plate}")
async def get_car(license_plate: str):
    car = await car_collection.find_one({"license_plate": license_plate})
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    car.pop("_id", None)
    return car