from django.core.cache import cache
import keras.model import model_from_json
from keras.applications.resnet50 import preprocess_input
import json
import cv2
from os.path import join, dirname


class ModelFactory(object):
    model_cache_key = 'model_cache'
    map_cache_key = 'map_cache'
    model_folder = join(dirname(__file__), './model')  # get current directory'
    img_res = (224, 224)

    @staticmethod
    def predict(img):

        model = cache.get(ModelFactory.model_cache_key)     # get model from cache
        model_map = cache.get(ModelFactory.map_cache_key)

        # Load and cache model if not done yet
        if model is None:
            ModelFactory.model_map, ModelFactory.model = _load_model_in_cache()

        img = cv2.resize(img, ModelFactory.img_res)
        img = preprocess_input(img)

        return model_map[model.predict(img)]


    @staticmethod    
    def _load_model_in_cache():
        model_folder = ModelFactory.model_folder
        model_cache_key = ModelFactory.model_cache_key
        map_cache_key = ModelFactory.map_cache_key

        try:
            model_json_file = open(join(model_folder, "model.json"), 'r')
            model_json = model_json_file.read()
            model_json_file.close()
            
            model = model_from_json(model_json)
            
            # load weights for model
            model.load_weights(join(model_folder, "model.h5"))

            # save in the cache
            cache.set(model_cache_key, model, None) 

            with open(join(model_folder, 'map.json')) as map_file:
                model_map = json.load(map_file)
                cache.set(map_cache_key)
            
            return (model_map, model)

        except ValueError:
            print("Can't load model from file! ")
            raise

            

