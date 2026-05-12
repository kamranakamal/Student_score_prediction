from pydantic import BaseModel, Field
from pydantic import ConfigDict
from typing import Annotated, Literal



class Student(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    gender: Annotated[Literal["male", "female"], Field(..., alias="gender")]
    race_ethnicity: Annotated[Literal["group B", "group C", "group A", "group D", "group E"], Field(..., alias="race/ethnicity")]
    parental_level_of_education: Annotated[Literal["bachelor's degree","some college","master's degree","associate's degree","high school", "some high school",], Field(..., alias="parental level of education")]
    lunch: Annotated[Literal["standard", "free/reduced"], Field(..., alias="lunch")]
    test_preparation_course: Annotated[Literal["none", "completed"], Field(..., alias="test preparation course")]
    reading_score: Annotated[int, Field(..., alias="reading score", ge=0, le=100)]
    writing_score: Annotated[int, Field(..., alias="writing score", ge=0, le=100)]