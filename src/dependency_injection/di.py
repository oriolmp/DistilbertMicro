"""Containers module."""

from dependency_injector import containers, providers

from src.service_layer.model_manager import ModelManager


class Container(containers.DeclarativeContainer):

    wiring_config: containers.WiringConfiguration = containers.WiringConfiguration(
        modules=["src.entrypoints.rest.api"]
    )
    config = providers.Configuration(yaml_files=["src/config.yaml"])

    model_consumer: ModelManager = providers.Resource(ModelManager, config=config)
