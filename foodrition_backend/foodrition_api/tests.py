from django.test import TestCase
from .services.ml_model import ModelFactory
from django.core.cache import cache


class MLModelTest(TestCase):

    def test_loading_model_to_cache(self):
        model_map, model = ModelFactory.load_model_in_cache()
        assert(hasattr(model, 'predict'))
        assert(isinstance(model_map, dict))

        # Make also sure that it lands in cache
        model = cache.get(ModelFactory.model_cache_key)     
        model_map = cache.get(ModelFactory.map_cache_key)
        assert(hasattr(model, 'predict'))
        assert(isinstance(model_map, dict))
