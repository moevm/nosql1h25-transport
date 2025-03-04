from pymongo import MongoClient

# Подключение к локальному серверу MongoDB
client = MongoClient('localhost', 27017)

# Создание базы данных и коллекции
db = client['test_database']
collection = db['test_collection']

# Пример записи данных в коллекцию
data = {
    "name": "Anon",
    "age": 8,
    "city": "Roma"
}
collection.insert_one(data)

# Чтение данных из коллекции
result = collection.find_one({"name": "Anon"})
print("Данные, прочитанные из базы данных:")
print(result)
