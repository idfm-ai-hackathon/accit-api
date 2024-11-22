import importlib
import os
from typing import Any


def get_model(model_name: str, params: dict[str, Any]):
    model_package, *module_path = params["class"].split(".")

    module = importlib.import_module(model_package)
    for path in module_path:
        module = getattr(module, path)

    fill_secrets_from_env(model_name, params)

    return module(**params)


def fill_secrets_from_env(model_name: str, params: dict[str, Any]):
    for key, value in params.items():
        if value == "SECRET":
            params[key] = os.getenv(f"{model_name.upper()}_{key.upper()}")
