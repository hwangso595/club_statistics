from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

def get_database():
    MONGODB_URL = os.getenv('MONGODB_URL')

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(MONGODB_URL)

    return client["test_db"]


if __name__ == "__main__":   

    # Get the database
    dbname = get_database()