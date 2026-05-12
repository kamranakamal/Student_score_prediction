import os
import streamlit as st
import requests
from Backend.schema.input_data import Student
from typing import get_args, get_origin, Literal
from pydantic import BaseModel

def get_literal_values(model: type[BaseModel], field_name: str):
    field = model.model_fields[field_name]
    annotation = field.annotation

    if get_origin(annotation) is Literal:
        return list(get_args(annotation))

    return None

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict")

gender_val = get_literal_values(Student, "gender")
race_val = get_literal_values(Student, "race_ethnicity")
lvl_edu = get_literal_values(Student, "parental_level_of_education")

gender = st.selectbox("Gender", options=gender_val)
race_ethnicity = st.selectbox(
    "Race/Ethnicity",
    race_val)

parental_level_of_education = st.selectbox("Parents Level of Education",lvl_edu) # type: ignore

lunch = st.selectbox("Lunch", ["standard", "free/reduced"])
test_preparation_course = st.selectbox(
    "Test Preparation Course", ["none", "completed"]
)
reading_score = st.slider("Reading Score", 0, 100)
writing_score = st.slider("Writing Score", 0, 100)


data = {
    "gender": gender,
    "race_ethnicity": race_ethnicity,
    "parental_level_of_education": parental_level_of_education,
    "lunch": lunch,
    "test_preparation_course": test_preparation_course,
    "reading_score": reading_score,
    "writing_score": writing_score,
}

if st.button("predict"):
    try:
        response = requests.post(API_URL, json=data, timeout=10)
        response.raise_for_status()
        output = response.json().get("prediction")
        if output is None:
            st.error("No prediction returned from API")
        else:
            if output > 100:
                output = 100
            st.success(f"Predicted Math score is {output}")
    except Exception as exc:
        st.error(f"Prediction failed: {exc}")
    