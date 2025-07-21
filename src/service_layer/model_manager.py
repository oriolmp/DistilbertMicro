"""Model initialization and consumption"""

from typing import Dict, Tuple

import torch
from transformers import (DistilBertForSequenceClassification,
                          DistilBertTokenizer)

from src.domain.exceptions import IncompleteConfiguration, MissingConfiguration


class ModelManager:
    """
    Class responsible for the model initialization and consumption

    Args:
        config: app configuration with tokenizer and model parameters
    """

    def __init__(self, config: Dict):

        tokenizer_config, model_config = self.parse_configuration(config)
        try:
            self.tokenizer = DistilBertTokenizer.from_pretrained(**tokenizer_config)
            self.model = DistilBertForSequenceClassification.from_pretrained(
                **model_config
            )
        except TypeError as exc:
            raise IncompleteConfiguration(
                f"Model or tokenizer configuration incorrect: {exc}"
            ) from exc

    @staticmethod
    def parse_configuration(config: Dict) -> Tuple[Dict, Dict]:
        """
        Checks if all necessary configuration is set.
        If all is correct, return tokenizer and model config
        """

        if not config:
            raise MissingConfiguration("Ensure config.yml file is created.")

        tokenizer_config = config.get("tokenizer")
        model_config = config.get("model")

        if not (tokenizer_config and model_config):
            raise IncompleteConfiguration(
                "Tokenizer and model configuration must be filled."
            )

        return tokenizer_config, model_config

    async def consume_model(self, text: str) -> Tuple[str, Tuple[float, float]]:
        """
        Prepares input and calls the model

        Args:
            text: text to analyze

        Returns:
            Tuple with the predicted label and the model calculated logits
        """

        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            output = self.model(**inputs)
            logits = output.logits

        predicted_class_id = logits.argmax().item()
        return self.model.config.id2label[predicted_class_id], logits.tolist()[0]
