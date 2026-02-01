import asyncio
from main import driver_collection, Driver
from datetime import datetime

initial_drivers = [
    Driver(
        name="Иванов И.И.",
        license_categories=["B", "C"],
        experience_years=5,
        is_available=True,
        comments="Работает по выходным",
        date_of_birth="1990-01-01",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    ).dict(),
    Driver(
        name="Петров П.П.",
        license_categories=["B"],
        experience_years=2,
        is_available=False,
        comments="В отпуске до июля",
        date_of_birth="1995-06-15",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    ).dict()
]

async def seed():
    await driver_collection.delete_many({})
    await driver_collection.insert_many(initial_drivers)

if __name__ == '__main__':
    asyncio.run(seed())