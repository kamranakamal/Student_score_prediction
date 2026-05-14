import os
import sys
import pandas as pd
from fastapi import FastAPI
import uvicorn
from Backend.schema.input_data import Student
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
        prediction_value = prediction[0]
        if prediction_value >= 100:
            prediction_value = 100
        elif prediction_value < 0:
            prediction_value = 0
        return {"prediction": int(prediction_value)}
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