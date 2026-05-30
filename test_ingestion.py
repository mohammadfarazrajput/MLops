from src.data_ingestion import DataIngestion
import logging
import os
os.makedirs("logs", exist_ok=True)
logging.basicConfig(level=logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(os.path.join("logs", "ingestion.logs"))
stream_handler = logging.StreamHandler()
detailed_log = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
file_handler.setFormatter(detailed_log)
stream_handler.setFormatter(detailed_log)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

DI = DataIngestion(db_name = "sample_mflix", collection_name="movies")
DI.connect()
df = DI.get_data(limit = 5)
DI.close()
print(df.shape)
print(df.columns.to_list())
print(df.head(3))


