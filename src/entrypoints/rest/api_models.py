from typing import Literal, Tuple

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    """POST /predict_sentiment response model"""

    text: str = Field(
        ...,
        description="Text desired to analyzed",
        examples=["I love my new phone, I would by it again for sure!"],
    )


class PredictResponse(BaseModel):
    """POST /predict_sentiment response model"""

    result: Literal["POSITIVE", "NEGATIVE"] = Field(
        ..., description="The model classification result"
    )
    logits: Tuple[float, float] = Field(..., description="Logits output for each label")
