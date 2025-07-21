"""API endpoints definition"""

from fastapi import APIRouter, HTTPException

from src.entrypoints.rest.api_impl import predict_sentiment_impl
from src.entrypoints.rest.api_models import PredictRequest, PredictResponse

router = APIRouter()


@router.get("/")
def home_page() -> str:
    """Home page message"""
    return "Welcome!"


@router.get("/health")
def health() -> str:
    """Health check"""
    return "OK"


@router.post("/predict_sentiment", response_model=PredictResponse)
async def predict_sentiment(
    predict_input: PredictRequest,
) -> PredictResponse:
    """Endpoint responsible for predicting text sentiment"""

    try:
        return await predict_sentiment_impl(predict_input)
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Error while processing query: {exc}"
        ) from exc
