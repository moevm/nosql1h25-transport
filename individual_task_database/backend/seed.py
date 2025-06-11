import asyncio
from main import driver_collection

initial_drivers = [
    {
        "name": "Иванов И.И.",
        "license_categories": ["B", "C"],
        "experience_years": 5,
        "is_available": True,
        "comments": "Работает по выходным"
    },
    {
        "name": "Петров П.П.",
        "license_categories": ["B"],
        "experience_years": 2,
        "is_available": False,
        "comments": "В отпуске до июля"
    }
]

async def seed():
    await driver_collection.delete_many({})
    await driver_collection.insert_many(initial_drivers)

if __name__ == '__main__':
    asyncio.run(seed())