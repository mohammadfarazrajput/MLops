from src.data_ingestion import DataIngestion
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
DI = DataIngestion(db_name = "sample_mflix", collection_name="movies")
DI.connect()
df = DI.get_data(limit = 5)
DI.close()
print(df.shape)
print(df.columns.to_list())
print(df.head(3))


