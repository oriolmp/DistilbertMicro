from unittest.mock import AsyncMock, MagicMock

import pytest
from transformers import (DistilBertForSequenceClassification,
                          DistilBertTokenizer)

from src.domain.exceptions import IncompleteConfiguration, MissingConfiguration
from src.service_layer.model_manager import ModelManager


class TestModelManager:

    @pytest.mark.parametrize(
        "config, raised_exception",
        [
            (
                {
                    "tokenizer": {"pretrained_model_name_or_path": "dummy"},
                    "model": {"pretrained_model_name_or_path": "dummy"},
                },
                None,
            ),
            ({"bad": "config"}, IncompleteConfiguration),
            ({}, MissingConfiguration),
        ],
    )
    def test_init(self, config, raised_exception, monkeypatch):

        if raised_exception:
            with pytest.raises(raised_exception):
                manager = ModelManager(config=config)
        else:

            def mock_get_model(*args, **kwargs):
                return MagicMock()

            monkeypatch.setattr(DistilBertTokenizer, "from_pretrained", mock_get_model)
            monkeypatch.setattr(
                DistilBertForSequenceClassification, "from_pretrained", mock_get_model
            )

            assert isinstance(ModelManager(config=config), ModelManager)

    @pytest.mark.asyncio
    async def test_consume_model(self, monkeypatch):

        def mock_get_tokenizer(*args, **kwargs):
            mocked_tokenizer = MagicMock()

            def mock_call(*args, **kwargs):
                return {"dummy": "dummy"}

            mock_get_tokenizer.__call__ = mock_call()

            return mocked_tokenizer

        def mock_get_model(*args, **kwargs):

            mocked_model = MagicMock()
            mocked_model.config.id2label.return_value = "POSITIVE"
            return mocked_model()

        monkeypatch.setattr(DistilBertTokenizer, "from_pretrained", mock_get_tokenizer)
        monkeypatch.setattr(
            DistilBertForSequenceClassification, "from_pretrained", mock_get_model
        )

        manager = ModelManager(
            config={
                "tokenizer": {"pretrained_model_name_or_path": "dummy"},
                "model": {"pretrained_model_name_or_path": "dummy"},
            }
        )

        assert await manager.consume_model("dummy") is not None
