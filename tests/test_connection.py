from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()
uri = os.getenv("MONGO_URI")
client = MongoClient(uri, tlsAllowInvalidCertificates=True)
client.admin.command("ping")
print("connnection")
