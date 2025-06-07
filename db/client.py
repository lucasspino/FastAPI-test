from dotenv import load_dotenv
import os
from pymongo import MongoClient
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
# base de datos local
# db_client = MongoClient().local
# BD Atlas

db_client = MongoClient(MONGO_URI).test
