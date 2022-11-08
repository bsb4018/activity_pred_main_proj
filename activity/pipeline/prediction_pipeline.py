import sys
from activity.exception import ActivityException
from activity.logger import logging
from pandas import DataFrame
import pandas as pd
from activity.ml.model.estimator import ModelResolver,TargetValueMapping
from activity.constant.training_pipeline import SAVED_MODEL_DIR
from activity.constant.prediction_pipeline import FROM_S3_SAVED_MODEL_DIR
from activity.constant.s3_bucket import TRAINING_BUCKET_NAME
from activity.utils.main_utils import load_object
from activity.cloud_storage.s3_syncer import S3Sync

class PredictionPipeline:
    def __init__(self):
        self.model_resolver_local = ModelResolver(model_dir=SAVED_MODEL_DIR)
        self.model_resolver_s3 = ModelResolver(model_dir=FROM_S3_SAVED_MODEL_DIR)
        self.s3_sync = S3Sync()
    
    def sync_model_from_s3_to_local_dir(self):
        try:
            logging.info("Entered the sync_model_from_s3_to_local_dir method of PredictionPipeline class")
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/{FROM_S3_SAVED_MODEL_DIR}"
            self.s3_sync.sync_folder_from_s3(folder = FROM_S3_SAVED_MODEL_DIR, aws_buket_url=aws_bucket_url)
            logging.info("Performed Syncing of saved models in S3 bucket to local")
        
        except Exception as e:
            raise ActivityException(e, sys) from e
    
    def predict_from_local(self, df:DataFrame):
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
    
    def predict_from_s3(self, df:DataFrame):
        
        try:
            logging.info("Entered the predict_from_s3 method of PredictionPipeline class")
            self.sync_model_from_s3_to_local_dir()
            model_resolver = self.model_resolver_s3
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
        
        

