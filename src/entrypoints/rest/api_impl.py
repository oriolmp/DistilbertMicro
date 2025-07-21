"""Define all API endpoints logic"""

import logging
from datetime import datetime

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from src.entrypoints.rest.api_models import PredictRequest, PredictResponse
from src.service_layer.model_manager import ModelManager

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@inject
async def predict_sentiment_impl(
    predict_input: PredictRequest,
    model_manager: ModelManager = Depends(Provide["model_consumer"]),
):
    """Predicts text sentiment calling a model"""

    logger.info("Query received")

    start_time = datetime.now()
    predicted_label, logits = await model_manager.consume_model(predict_input.text)
    execution_time = datetime.now() - start_time

    logger.info(
        "Query successfully analyzed. Execution time: %d.%d",
        execution_time.seconds,
        execution_time.microseconds,
    )
    return PredictResponse(result=predicted_label, logits=logits)
