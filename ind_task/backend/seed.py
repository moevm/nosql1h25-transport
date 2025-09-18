import asyncio
from main import customer_collection
from main import tc_collection
from main import rent_collection

initial_customers = [
    {
        
        "name": "Иванов И.И.",
        "login": "ivanov5940",
        "password": "3495jk34m4k",
        "contact_information": "+7 9213449013",
        "address": "г.Санкт-Петербург, ул.Ташкентская, д.7",
        "comments": "ТС заберу сам"
    },
    {
        "login": "petrov_34",
        "password": "234k3mfmr",
        "name": "Петров П.П.",
        "contact_information": "+7 9213449013",
        "address": "г.Санкт-Петербург, ул.Будапештская, д.9",
        "comments": "Лучше писать смс вместо звонков"
    }
]

initial_tcs = [
    {
        "registration_number": "203idf",
        "type_tc": "грузовик",
        "is_available": True,
        "comments": "Работает по выходным"
    },
    {
        "registration_number": "203ids",
        "type_tc": "грузовик",
        "is_available": True,
        "comments": "Работает по выходным"
    }
]

initial_rents = [
    {
        "rent_id": "202344idf",
        "date_of_begining": "2025-11-20",
        "date_of_ending": "2025-11-25",
        "order_name": "Иванов Иван Иванович",
        "tc_registration_number": "1299AO"
    
    },
    {
        "rent_id": "56744id",
        "date_of_begining": "2025-11-23",
        "date_of_ending": "2025-12-07",
        "order_name": "Стеклов Антон Викторович",
        "tc_registration_number": "1293ATY"
    
    }
]

async def seed():
   
    await customer_collection.delete_many({})
    await customer_collection.insert_many(initial_customers)
    await tc_collection.delete_many({})
    await tc_collection.insert_many(initial_tcs)
    await rent_collection.delete_many({})
    await rent_collection.insert_many(initial_rents)


if __name__ == '__main__':
    asyncio.run(seed()) 