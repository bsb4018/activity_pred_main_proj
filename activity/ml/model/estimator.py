import os,sys
from pandas import DataFrame
from activity.exception import ActivityException
from activity.logger import logging
from sklearn.pipeline import Pipeline
from activity.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME

class TargetValueMapping:
    def __init__(self):
        try:
            self.LAYING: int = 0
            self.SITTING: int = 1
            self.STANDING: int = 2
            self.WALKING: int = 3
            self.WALKING_DOWNSTAIRS: int = 4
            self.WALKING_UPSTAIRS: int = 5

        except Exception as e:
            raise e

    def to_dict(self):
        try:
            return self.__dict__
        except Exception as e:
            raise e    

    def reverse_mapping(self):
        try:
            mapping_response = self.to_dict()
            return dict(zip(mapping_response.values(), mapping_response.keys()))
        except Exception as e:
            raise e

class ActivityModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise e
    
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise e


class ModelResolver:
    def __init__(self, model_dir=SAVED_MODEL_DIR):
        try:
            self.model_dir = model_dir

        except Exception as e:
            raise e

    def get_best_model_path(self,) -> str:
        try:
            timestamps = list(map(int, os.listdir(self.model_dir)))
            latest_timestamp = max(timestamps)
            latest_model_path = os.path.join(self.model_dir, f"{latest_timestamp}", MODEL_FILE_NAME)
            return latest_model_path       
        
        except Exception as e:
            raise e

    def is_model_exists(self) -> bool:
        try:
            if not os.path.exists(self.model_dir):
                return False

            timestamps = os.listdir(self.model_dir)
            if len(timestamps) == 0:
                return False

            latest_model_path = self.get_best_model_path()
            if not os.path.exists(latest_model_path):
                return False

            return True

        except Exception as e:
            raise e