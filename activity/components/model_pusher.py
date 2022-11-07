
from activity.exception import ActivityException
from activity.logger import logging
from activity.entity.artifact_entity import ModelPusherArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from activity.entity.config_entity import ModelEvaluationConfig,ModelPusherConfig
import os,sys
import shutil
from activity.ml.metric.classification_metric import get_classification_score
from activity.utils.main_utils import save_object,load_object,write_yaml_file

class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig,
                       model_eval_artifact: ModelEvaluationArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.model_eval_artifact = model_eval_artifact
        except Exception as e:
            raise ActivityException(e,sys) from e

    def initiate_model_pusher(self,) -> ModelPusherArtifact:
        try:
            trained_model_path = self.model_eval_artifact.trained_model_path
            
            #Pushing the trained model in the model storage space
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path),exist_ok=True)
            shutil.copy(src=trained_model_path, dst=model_file_path)

            #Pushing the trained model in a the saved path for production
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path),exist_ok=True)
            shutil.copy(src=trained_model_path, dst=saved_model_path)

            #Prepare artifact
            model_pusher_artifact = ModelPusherArtifact(saved_model_path=saved_model_path, model_file_path=model_file_path)
            return model_pusher_artifact

        except Exception as e:
            raise ActivityException(e,sys) from e

