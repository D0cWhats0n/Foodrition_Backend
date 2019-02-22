from foodrition_api.services.ml_model import ModelFactory


def foodrition_api_startup_func():
    ModelFactory.load_model_and_maps()