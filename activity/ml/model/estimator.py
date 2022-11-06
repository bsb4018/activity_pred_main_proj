import sys
from pandas import DataFrame
from activity.exception import ActivityException
from activity.logger import logging
from sklearn.pipeline import Pipeline

class TargetValueMapping:
    def __init__(self):
        self.LAYING: int = 0
        self.SITTING: int = 1
        self.STANDING: int = 2
        self.WALKING: int = 3
        self.WALKING_DOWNSTAIRS: int = 4
        self.WALKING_UPSTAIRS: int = 5

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))


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