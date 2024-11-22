import importlib
import os

from app.models.config import LLMConfig


def get_model(model_name: str, params: LLMConfig):
    model_package, *module_path = params.model_class.split(".")

    module = importlib.import_module(model_package)
    for path in module_path:
        module = getattr(module, path)

    fill_secrets_from_env(model_name, params)

    return module(**params.model_dump(exclude=["model_class"]))


def fill_secrets_from_env(model_name: str, params: LLMConfig):
    for key, value in params.model_dump().items():
        if value == "SECRET":
            setattr(params, key, os.getenv(f"{model_name.upper()}_{key.upper()}"))
