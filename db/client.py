from pymongo import MongoClient

# base de datos local
# db_client = MongoClient().local
# BD Atlas
URL = "mongodb+srv://lucaspino07:61D7wZSFfz3NeWR7@cluster0.bisbkqy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
db_client = MongoClient(URL).test
