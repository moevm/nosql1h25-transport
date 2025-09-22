import asyncio
from main import car_collection, master_collection
from main import garage_collection, flight_collection

initial_cars = [
    {
        
        "registration_number": "28A9O",
        "category": "ivanov5940",
        "model": "3495jk34m4k",
        "year": "2020"
    },
    {
        "registration_number": "454KY8",
        "category": "ivanov5940",
        "model": "3495jk34m4k",
        "year": "2022"
    }
]

initial_masters = [
    {
        "name": "203idf",
        "qualification": "грузовик",
        "experience_years": "20",
        "is_available": True,
        "comments": "Работает по выходным"
    },
    {
        "name": "5603idf",
        "qualification": "грузовик",
        "experience_years": "2",
        "is_available": True,
        "comments": "Работает по выходным"
    }
]

initial_garages = [
    {
        "garage_id": "202344idf",
        "address": "2025-11-2023:55",
        "is_available": True,
        "comments": "Работает по выходным"
    
    },
    {
        "garage_id": "56744id",
        "address": "2025-11-2323:17",
        "is_available": True,
        "comments": "Работает по выходным"
    }
]


initial_flights = [
    {
        "flight_id": "202344idf",
        "master_name": "202344idf",
        "registration_number": "202344idf",
        "garage_id": "202344idf",
        "date_of_begining": "2025-11-2023:55",
        "date_of_ending": "2025-11-2023:55",
        "comments": "Работает по выходным"
    
    },
    {
        "flight_id": "202344idf",
        "master_name": "202344idf",
        "registration_number": "202344idf",
        "garage_id": "202344idf",
        "date_of_begining": "2025-11-2023:55",
        "date_of_ending": "2025-11-2023:55",
        "comments": "Работает по выходным"
    }
]

async def seed():
   
    await car_collection.delete_many({})
    await car_collection.insert_many(initial_cars)
    await master_collection.delete_many({})
    await master_collection.insert_many(initial_masters)
    await garage_collection.delete_many({})
    await garage_collection.insert_many(initial_garages)
    await flight_collection.delete_many({})
    await flight_collection.insert_many(initial_flights)


if __name__ == '__main__':
    asyncio.run(seed()) 