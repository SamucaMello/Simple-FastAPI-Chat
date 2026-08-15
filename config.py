import importlib
import inspect
from os import getenv
from pathlib import Path
from beanie import Document 
from dotenv import load_dotenv; load_dotenv()


def get_beanie_models():
    models = []
    models_path = Path("src/models")

    for file in models_path.glob("*.py"):
        if file.name.startswith("_"):
            continue

        module = importlib.import_module(
            f"src.models.{file.stem}"
        )

        for _, cls in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(cls, Document)
                and cls is not Document
                and cls.__module__ == module.__name__
            ):
                models.append(cls)
    return models
        






MONGO_URI       = getenv("MONGO_URI")
JWT_SECRET      = getenv("JWT_SECRET")
BEANIE_MODELS   = get_beanie_models()


