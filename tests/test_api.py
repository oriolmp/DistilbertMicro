import pytest
from unittest.mock import AsyncMock
from src.entrypoints.cli import app

class TestAPI:

    @pytest.mark.parametrize(
            "request_input, mocked_model_response, expected_status_code",
            [
                ({"text": "dummy"}, ["POSITIVE", [0.0, 0.0]], 200),
                ({"bad": "input"}, None, 422),
                ({"text": "dummy"}, "bad output", 500)
            ]
    )
    @pytest.mark.asyncio
    async def test_predict_sentiment(self, client, request_input, mocked_model_response, expected_status_code):
        
        model_manager_mock = AsyncMock()
        model_manager_mock.consume_model.return_value = mocked_model_response

        with app.container.model_consumer.override(model_manager_mock):
            response = await client.post("/predict_sentiment", json=request_input)
            assert response.status_code == expected_status_code