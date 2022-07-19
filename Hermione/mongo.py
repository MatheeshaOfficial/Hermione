import asyncio
import sys

# from motor import motor_asyncio
from Hermione import MONGO_DB_URI 
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from Hermione.conf import get_int_key, get_str_key


MONGO_PORT = 27017
MONGO_DB_URI = get_str_key("MONGO_DB_URI")
MONGO_DB = "Hermione"


client = MongoClient()
client = MongoClient(MONGO_DB_URI, MONGO_PORT)[MONGO_DB]
# motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI, MONGO_PORT)
motor = MongoClient(MONGO_URI, MONGO_PORT)
db = motor[MONGO_DB]
db = client["Hermione"]
try:
    asyncio.get_event_loop().run_until_complete(motor.server_info())
except ServerSelectionTimeoutError:
    sys.exit(log.critical("Can't connect to mongodb! Exiting..."))
