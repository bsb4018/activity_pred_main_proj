import sys
from activity.exception import ActivityException
from activity.logger import logging
from pandas import DataFrame
from activity.components.model_prediction import ModelPrediction
class PredictionPipeline:
    def __init__(self):
        try:
            self.model_prediction_component = ModelPrediction()
        except Exception as e:
            raise ActivityException(e,sys) from e

    def predict(self, df:DataFrame):
        try:
            logging.info("Entered the predict method of PredictionPipeline class")
            prediction_result = self.model_prediction_component.predict_activity(df)
            return prediction_result

        except Exception as e:
            raise ActivityException(e,sys) from e
    
        

