from django.core.cache import cache
from keras.models import model_from_json
from keras.applications.resnet50 import preprocess_input
import json
import cv2
from os.path import join, dirname
import tensorflow as tf
import numpy as np


class ModelFactory(object):
    model_cache_key = 'model_cache'
    model_map_cache_key = 'model_map_cache'
    nutr_map_cache_key = 'nutr_map_cache'
    model_folder = join(dirname(__file__), 'model')  # get current directory'
    img_res = (224, 224)
    graph = None

    @staticmethod
    def predict(img):
        img_res = ModelFactory.img_res
    
        with ModelFactory.graph.as_default():
            model = cache.get(ModelFactory.model_cache_key)     # get model from cache
            model_map = cache.get(ModelFactory.model_map_cache_key)
            nutr_map = cache.get(ModelFactory.nutr_map_cache_key)

            img = cv2.imdecode(np.fromstring(img.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            img = cv2.resize(img, ModelFactory.img_res)
            img = preprocess_input(img)

            predict_vec = model.predict(img.reshape(-1, img_res[0], img_res[1], 3))[0]
            predict_id = np.argmax(predict_vec)

            # TODO map to food table for nutrition info
            print(f"Predicted class {predict_id} with precentage {predict_vec[predict_id]*100}%")
            pred_food_class = model_map[predict_id]
            pred_nutr_class = nutr_map[predict_id]
            return (predict_id, pred_food_class, pred_nutr_class)

    @staticmethod    
    def load_model_in_cache():
        ''' Loads model and necessary maps to cache. Has to be called before predictions 
            can be made. '''
        model_folder = ModelFactory.model_folder
        model_cache_key = ModelFactory.model_cache_key
        model_map_cache_key = ModelFactory.model_map_cache_key
        nutr_map_cache_key = ModelFactory.nutr_map_cache_key

        try:
            print("Trying to load model in cache")
            model_json_file = open(join(model_folder, "model.json"), 'r')
            model_json = model_json_file.read()
            model_json_file.close()
            
            model = model_from_json(model_json)
            
            # load weights for model
            model.load_weights(join(model_folder, "model.h5"))
            # Set graph for async predict
            # (see issue https://github.com/keras-team/keras/issues/2397)
            ModelFactory.graph = tf.get_default_graph()
            # save in the cache
            cache.set(model_cache_key, model, None)

            with open(join(model_folder, 'clf_map.json')) as map_file:
                model_map = json.load(map_file)
                model_map = {int(key): value for (key, value) in model_map.items()}
                print("model_map: ",model_map)
                cache.set(model_map_cache_key, model_map)

            with open(join(model_folder, 'nutrition_map.json')) as map_file:
                nutr_map = json.load(map_file)
                nutr_map = {int(key): value for (key, value) in nutr_map.items()}
                cache.set(nutr_map_cache_key, nutr_map)
            
            return (nutr_map, model_map, model)

        except TypeError:
            print("Can't load model from file! ")
            raise

            

