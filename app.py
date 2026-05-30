from fastapi import FastAPI
from pydantic import BaseModel
import mlflow.sklearn
import os
from dotenv import load_dotenv

load_dotenv()

# Pydantic model — defines the shape of incoming request
# FastAPI validates every request against this automatically
# if runtime or year is missing or wrong type → automatic 422 error
class PredictRequest(BaseModel):
    runtime: float
    year: float

# Pydantic model for the response
class PredictResponse(BaseModel):
    prediction: str
    prediction_code: int

app = FastAPI(title="Movies Type Classifier", version="1.0")

# load model once at startup — not on every request
# loading from DagsHub MLflow registry
os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("DAGSHUB_USERNAME")
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("DAGSHUB_TOKEN")
mlflow.set_tracking_uri("https://dagshub.com/farazrajput112/MLops.mlflow")

model = mlflow.sklearn.load_model("models:/MoviesTypeClassifier@production")

@app.get("/")
def home():
    return {"message": "ML API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# POST because we're sending data in the request body
# GET is for fetching, POST is for sending data
@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    # model expects a 2D array — [[runtime, year]]
    features = [[request.runtime, request.year]]
    prediction_code = int(model.predict(features)[0])
    
    # map numeric prediction back to label
    label_map = {0: "movie", 1: "series"}
    prediction = label_map.get(prediction_code, "unknown")
    
    return PredictResponse(
        prediction=prediction,
        prediction_code=prediction_code
    )