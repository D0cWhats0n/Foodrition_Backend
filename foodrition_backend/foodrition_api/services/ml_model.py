from keras.models import model_from_json
from keras.applications.resnet50 import preprocess_input
import json
import cv2
from os.path import join, dirname
import tensorflow as tf
import numpy as np


class food_prediction():
    def __init__(self, pred_id: int, food_class: str, nutr_class: str, nutr_ndb_no: int):
        self.pred_id = int(pred_id)
        self.food_class = food_class
        self.nutr_class = nutr_class
        self.nutr_ndb_no = int(nutr_ndb_no)


class ModelFactory:
    model_folder = join(dirname(__file__), 'model')  # get current directory'
    img_res = (224, 224)
    graph = None
    model = None
    nutr_descr_map = None
    nutr_ndb_map = None
    model_map = None
    
    @staticmethod
    def predict(img):
        img_res = ModelFactory.img_res

        model = ModelFactory.model
        model_map = ModelFactory.model_map
        nutr_descr_map = ModelFactory.nutr_descr_map
        nutr_ndb_map = ModelFactory.nutr_ndb_map
    
        with ModelFactory.graph.as_default():

            img = cv2.imdecode(np.fromstring(img.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            img = cv2.resize(img, ModelFactory.img_res)
            img = preprocess_input(img)

            predict_vec = model.predict(img.reshape(-1, img_res[0], img_res[1], 3))[0]
            predict_id = np.argmax(predict_vec)

            print(f"Predicted class {predict_id} with precentage {predict_vec[predict_id]*100}%")
            pred = food_prediction(predict_id, model_map[predict_id], nutr_descr_map[predict_id], 
                                   nutr_ndb_map[predict_id])
            return pred

    @staticmethod    
    def load_model_and_maps():
        ''' Loads model and necessary maps to. Has to be called in service startup 
            before predictions can be made. '''
        model_folder = ModelFactory.model_folder

        try:
            print("Trying to load model in cache")
            model_json_file = open(join(model_folder, "model.json"), 'r')
            model_json = model_json_file.read()
            model_json_file.close()
            
            ModelFactory.model = model_from_json(model_json)
            
            # load weights for model
            ModelFactory.model.load_weights(join(model_folder, "model.h5"))
            # Set graph for async predict
            # (see issue https://github.com/keras-team/keras/issues/2397)
            ModelFactory.graph = tf.get_default_graph()

            with open(join(model_folder, 'clf_map.json')) as map_file:
                ModelFactory.model_map = json.load(map_file)
                ModelFactory.model_map = {int(key): value for (key, value) in
                                          ModelFactory.model_map.items()}
                print("model_map: ", ModelFactory.model_map)

            with open(join(model_folder, 'nutrition_map.json')) as map_file:
                ModelFactory.nutr_descr_map = json.load(map_file)
                ModelFactory.nutr_descr_map = {int(key): value for (key, value) in
                                               ModelFactory.nutr_descr_map.items()}

            with open(join(model_folder, 'nutrition_map_NDB.json')) as map_file:
                ModelFactory.nutr_ndb_map = json.load(map_file)
                ModelFactory.nutr_ndb_map = {int(key): value for (key, value) in
                                             ModelFactory.nutr_ndb_map.items()}
        
        except TypeError:
            print("Can't load model from file! ")
            raise

            

