import os
import sys
import pandas as pd
from fastapi import FastAPI
import uvicorn
from schema.input_data import Student
import joblib
from src.exception import CustomException
from src.logger import logging


app = FastAPI()

PREPROCESSOR_PATH = os.path.join("artifacts", "preprocessor.pkl")
MODEL_PATH = os.path.join("artifacts", "model.pkl")

try:
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    model = joblib.load(MODEL_PATH)
except Exception as exc:
    logging.error("Failed to load artifacts", exc_info=exc)
    raise CustomException(exc, sys)





@app.post("/predict")
def predict(data: Student):
    try:
        data = data.model_dump(by_alias=True)
        input_df = pd.DataFrame([data])
        features = preprocessor.transform(input_df)
        prediction = model.predict(features)
        return {"prediction": int(prediction[0])}
    except Exception as exc:
        logging.error("Prediction failed", exc_info=exc)
        raise CustomException(exc, sys)


@app.get("/")
def home():
    return {"message": "An Api to predict Students Score"}

@app.get("/health")
def health():
    return {"status":"ok"}

if __name__ == "__main__":
    uvicorn.run(app)