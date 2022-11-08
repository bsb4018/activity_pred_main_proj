
from pandas import DataFrame
import pandas as pd
from activity.ml.model.estimator import ModelResolver,TargetValueMapping
from activity.constant.training_pipeline import SAVED_MODEL_DIR
from activity.utils.main_utils import load_object

class PredictionPipeline:
    def __init__(self):
        pass
    
    
    def predict(self, df:DataFrame):
        
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
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
