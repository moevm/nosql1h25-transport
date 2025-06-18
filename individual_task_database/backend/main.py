from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from bson import ObjectId
from datetime import datetime
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
db = client.driver_db
driver_collection = db.drivers

class Driver(BaseModel):
    name: str
    license_categories: List[str]
    experience_years: int
    is_available: bool
    comments: Optional[str] = None
    date_of_birth: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@app.get("/drivers", response_model=List[Driver])
async def get_drivers(
    name: Optional[str] = Query(None),
    comment: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    min_experience: Optional[int] = Query(None),
    max_experience: Optional[int] = Query(None),
    is_available: Optional[bool] = Query(None)
):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if comment:
        query["comments"] = {"$regex": comment, "$options": "i"}
    if category:
        query["license_categories"] = {"$regex": category, "$options": "i"}
    if min_experience is not None or max_experience is not None:
        query["experience_years"] = {}
        if min_experience is not None:
            query["experience_years"]["$gte"] = min_experience
        if max_experience is not None:
            query["experience_years"]["$lte"] = max_experience
    if is_available is not None:
        query["is_available"] = is_available
    drivers = await driver_collection.find(query).to_list(100)
    return drivers

@app.post("/drivers")
async def create_driver(driver: Driver):
    driver.created_at = datetime.utcnow()
    driver.updated_at = datetime.utcnow()
    await driver_collection.insert_one(driver.dict())
    return {"message": "Driver added"}

@app.put("/drivers/{name}")
async def update_driver(name: str, driver: Driver):
    existing = await driver_collection.find_one({"name": name})
    if not existing:
        raise HTTPException(status_code=404, detail="Driver not found")

    # сохраняем оригинальную дату создания
    driver.created_at = existing.get("created_at")
    driver.updated_at = datetime.utcnow()

    result = await driver_collection.update_one({"name": name},
                                                {"$set": driver.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Driver not found")
    return {"message": "Driver updated"}

@app.delete("/drivers/{name}")
async def delete_driver(name: str):
    result = await driver_collection.delete_one({"name": name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Driver not found")
    return {"message": "Driver deleted"}

@app.get("/drivers/export")
async def export_drivers():
    drivers = await driver_collection.find().to_list(100)
    for d in drivers:
        d.pop("_id", None)
    return drivers

@app.post("/drivers/import")
async def import_drivers(drivers: List[Any] = Body(...)):
    cleaned_drivers = []
    for d in drivers:
        d.pop("_id", None)
        try:
            driver = Driver(**d)
            driver.created_at = driver.created_at or datetime.utcnow()
            driver.updated_at = datetime.utcnow()
            cleaned_drivers.append(driver.dict())
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid driver data: {d}, error: {e}")
    await driver_collection.delete_many({})
    await driver_collection.insert_many(cleaned_drivers)
    return {"message": "Drivers imported"}