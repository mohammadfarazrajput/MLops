from pymongo import MongoClient
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

class DataIngestion():
    def __init__(self, db_name: str, collection_name:str):
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None

    def connect(self):
        uri = os.getenv("MONGO_URI")
        self.client = MongoClient(uri)
        logger.info("Connection Established")
        logger.info(f"Databases: {self.client.list_database_names()}")

    def get_data(self, limit: int = 100) -> pd.DataFrame:
        database = self.client[self.db_name]
        collection = database[self.collection_name]
        logger.info(f"DB: '{self.db_name}' | Collection: '{self.collection_name}'")
        logger.info(f"Count: {collection.count_documents({})}")
        items = collection.find().limit(limit)
        data = list(items)
        df = pd.DataFrame(data)
        df.drop(columns=["_id"], inplace=True, errors="ignore")
        logger.info(f"Extracted {len(df)}entries from {self.collection_name}")
        return df
    def close(self):
        if self.client:
            self.client.close()
            logger.info("Connection Closed")
            