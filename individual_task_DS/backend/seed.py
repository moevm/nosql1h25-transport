import asyncio
from main import car_collection, Car, ServiceEpisode
from datetime import datetime, timedelta

initial_cars = [
    Car(
        name="КамАЗ самосвал",
        model="КамАЗ-6520",
        license_plate="А123БВ77",
        category="Грузовой",
        year=2015,
        service_history=[
            ServiceEpisode(date="2025-01-10",
                           description="Плановое ТО, замена масла",
                           replaced_parts=["Масло", "Фильтр"],
                           mileage = 90000,
                           cost = 4000
                           ).dict(),
            ServiceEpisode(date="2025-06-20",
                           description="Ремонт тормозов",
                           replaced_parts=["Тормозные колодки"],
                           mileage = 95000,
                           cost = 20000
                           ).dict()
        ],
        created_at=datetime.utcnow() + timedelta(hours=3),
        updated_at=datetime.utcnow() + timedelta(hours=3)
    ).dict(),
    Car(
        name="Экскаватор",
        model="CAT 320D",
        license_plate="В456ГД98",
        category="Строительная",
        year=2018,
        service_history=[
            ServiceEpisode(date="2025-12-01",
                           description="Замена гидравлического насоса",
                           replaced_parts=["Насос"],
                           mileage = 50000,
                           cost = 8000
                           ).dict()
        ],
        created_at=datetime.utcnow() + timedelta(hours=3),
        updated_at=datetime.utcnow() + timedelta(hours=3)
    ).dict()
]

async def seed():
    await car_collection.delete_many({})
    await car_collection.insert_many(initial_cars)

if __name__ == "__main__":
    asyncio.run(seed())
