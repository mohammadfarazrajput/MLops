import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import  accuracy_score, f1_score
from sklearn.preprocessing import LabelEncoder
import logging
import pandas as pd
import dagshub
import os
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger("ModelTrainer")

class ModelTrainer():
    def __init__(self, experiment_name):
        self.experiment = experiment_name
        #mlflow.set_tracking_uri("sqlite:///mlflow.db")
        os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("DAGSHUB_USERNAME")
        os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("DAGSHUB_TOKEN")
        
        mlflow.set_tracking_uri("https://dagshub.com/farazrajput112/MLops.mlflow")
        #dagshub.init(repo_owner='farazrajput112', repo_name='MLops', mlflow=True)
        mlflow.set_experiment(self.experiment)
        logger.info(f"Experiment: Model Training Started")
    def train(self, df:pd.DataFrame, params: dict):
        df = df[["runtime", "year", "type"]].dropna()
        le = LabelEncoder()
        df["type_encoded"]= le.fit_transform(df["type"])
        X = df[["runtime", "year"]]
        y = df["type_encoded"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        with mlflow.start_run():
            model = RandomForestClassifier(
                n_estimators=params["n_estimators"],
                max_depth= params["max_depth"],
                random_state=42
            )
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average="weighted")
            mlflow.log_param("n_estimators", params["n_estimators"])
            mlflow.log_param("max_depth", params["max_depth"])

            # log_metric records your outputs
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("f1_score", f1)

            # log_sklearn_model saves the model file as an artifact
            mlflow.sklearn.log_model(model, "random_forest_model", registered_model_name="MoviesTypeClassifier")

            logger.info(f"Run complete — accuracy: {accuracy:.4f}, f1: {f1:.4f}")

        return model
