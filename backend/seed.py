import asyncio
from main import car_collection, master_collection
from main import garage_collection, flight_collection

initial_cars = [
    {
        
        "registration_number": "28A9O",
        "category": "спец техника",
        "model": "JCB 4845-78",
        "year": "2020"
    },
    {
        "registration_number": "454KY8",
        "category": "складская техника",
        "model": "KCB 4845-78",
        "year": "2022"
    }
]

initial_masters = [
    {
        "name": "Иванов Иван Петрович",
        "qualification": "мастер",
        "experience_years": "4",
        "is_available": True,
        "comments": "Работает по выходным"
    },
    {
        "name": "Корнев Николай Юрьевич",
        "qualification": "монтажник",
        "experience_years": "2",
        "is_available": True,
        "comments": "Работает по выходным"
    }
]

initial_garages = [
    {
        "garage_id": "202344idf",
        "address": "г. Сагкт-Петербург, ул. Марата, д. 5",
        "is_available": True,
        "comments": "Работает по выходным"
    
    },
    {
        "garage_id": "56744id",
        "address": "г. Сагкт-Петербург, ул. Лесная, д. 5",
        "is_available": True,
        "comments": "Работает по выходным"
    }
]


initial_flights = [
    {
        "flight_id": "202344idf",
        "master_name": "Петров Иван Иванович",
        "registration_number": "202TF",
        "garage_id": "202344idf",
        "date_of_begining": "2025-11-2023:55",
        "date_of_ending": "2025-11-2023:55",
        "comments": "Работает по выходным"
    
    },
    {
        "flight_id": "202344idf",
        "master_name": "Иванов Петр Иванович",
        "registration_number": "244AT",
        "garage_id": "202iodf",
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