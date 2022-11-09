import sys
from activity.exception import ActivityException
from activity.logger import logging
from pandas import DataFrame
from activity.ml.model.estimator import ModelResolver,TargetValueMapping
from activity.constant.training_pipeline import SAVED_MODEL_DIR
from activity.utils.main_utils import load_object
from activity.cloud_storage.s3_syncer import S3Sync

class PredictionPipeline:
    def __init__(self):
        self.model_resolver_local = ModelResolver(model_dir=SAVED_MODEL_DIR)
        self.s3_sync = S3Sync()
    
    def predict(self, df:DataFrame):
        try:
            logging.info("Entered the predict_from_local method of PredictionPipeline class")
            model_resolver = self.model_resolver_local
            if not model_resolver.is_model_exists():
                return []
            best_model_path = model_resolver.get_best_model_path()
            model = load_object(file_path=best_model_path)
            df = df.drop(['subject','Activity'], axis=1, errors='ignore')
            y_pred = model.predict(df)
            df['predicted_column'] = y_pred
            df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
            prediction_result = df['predicted_column'].tolist()
            return prediction_result

        except Exception as e:
            raise ActivityException(e,sys) from e
    
        

