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
    map_cache_key = 'map_cache'
    model_folder = join(dirname(__file__), 'model')  # get current directory'
    img_res = (224, 224)
    graph = None

    @staticmethod
    def predict(img):
        img_res = ModelFactory.img_res
        if ModelFactory.graph is None:
            # Load and cache model if not done yet, and set ModelFactory.graph
            # (see issue https://github.com/keras-team/keras/issues/2397)
            ModelFactory.model_map, ModelFactory.model = ModelFactory.load_model_in_cache()

        with ModelFactory.graph.as_default():
            model = cache.get(ModelFactory.model_cache_key)     # get model from cache
            model_map = cache.get(ModelFactory.map_cache_key)

            img = cv2.imdecode(np.fromstring(img.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            img = cv2.resize(img, ModelFactory.img_res)
            img = preprocess_input(img)

            predict_vec = model.predict(img.reshape(-1, img_res[0], img_res[1], 3))[0]
            predict_id = np.argmax(predict_vec)
            # TODO map to food table for nutrition info
            print(f"Predicted class {predict_id} with precentage {predict_vec[predict_id]*100}%")
            return predict_id


    @staticmethod    
    def load_model_in_cache():
        model_folder = ModelFactory.model_folder
        model_cache_key = ModelFactory.model_cache_key
        map_cache_key = ModelFactory.map_cache_key

        try:
            print("Trying to load model in cache")
            model_json_file = open(join(model_folder, "model.json"), 'r')
            model_json = model_json_file.read()
            model_json_file.close()
            
            model = model_from_json(model_json)
            
            # load weights for model
            model.load_weights(join(model_folder, "model.h5"))
            ModelFactory.graph = tf.get_default_graph()
            # save in the cache
            cache.set(model_cache_key, model, None)

            with open(join(model_folder, 'map.json')) as map_file:
                model_map = json.load(map_file)
                cache.set(map_cache_key, model_map)
            
            return (model_map, model)

        except TypeError:
            print("Can't load model from file! ")
            raise

            

