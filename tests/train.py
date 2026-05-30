from src.data_ingestion import DataIngestion
from src.model_trainer import ModelTrainer
import logging
import os
from mlflow import MlflowClient

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

ingestion = DataIngestion(db_name="sample_mflix", collection_name="movies")
ingestion.connect()
df = ingestion.get_data(limit=1000)
ingestion.close()

# train with two different param sets so we have runs to compare
trainer = ModelTrainer(experiment_name="movies-type-classifier")

trainer.train(df, params={"n_estimators": 100, "max_depth": 5})
trainer.train(df, params={"n_estimators": 200, "max_depth": 10})
trainer.train(df, params={"n_estimators": 50,  "max_depth": 3})
client = MlflowClient(tracking_uri="sqlite:///mlflow.db")
client.set_registered_model_alias(
    name="MoviesTypeClassifier",
    alias="production",
    version="3"
)