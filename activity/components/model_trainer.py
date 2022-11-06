import os,sys

from activity.exception import ActivityException
from activity.logger import logging
from activity.utils.main_utils import (load_numpy_array_data, load_object,
                                     save_object)
from activity.entity.artifact_entity import (DataTransformationArtifact,
                                           ModelTrainerArtifact)
from activity.entity.config_entity import ModelTrainerConfig
from activity.ml.metric.classification_metric import get_classification_score
from activity.ml.model.estimator import ActivityModel
from sklearn import svm

class ModelTrainer:
    def __init__(
        self,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_config: ModelTrainerConfig,
    ):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config


    def train_model(self, x_train, y_train):
        try:
            lin_svc = svm.LinearSVC(penalty='l2', loss='squared_hinge', C =  0.9412, multi_class='ovr',random_state=44)
            lin_svc.fit(x_train, y_train)
            return lin_svc
        except Exception as e:
            raise e

    def initiate_model_trainer(self) -> ModelTrainerArtifact:

        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            #Load transformed data
            train_arr = load_numpy_array_data(
                file_path = self.data_transformation_artifact.transformed_train_file_path
            )
            test_arr = load_numpy_array_data(
                file_path = self.data_transformation_artifact.transformed_test_file_path
            )
            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            )

            model = self.train_model(x_train, y_train)
            y_train_pred = model.predict(x_train)
            classification_train_metric = get_classification_score(y_true = y_train, y_pred = y_train_pred)

            if classification_train_metric.f1_score<=self.model_trainer_config.expected_accuracy:
                raise Exception("Trained model is not good to provide expected accuracy")

            y_test_pred = model.predict(x_test)
            classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)

            #Overfitting and Underfitting
            diff = abs(classification_train_metric.f1_score-classification_test_metric.f1_score)
            
            if diff>self.model_trainer_config.overfitting_underfitting_threshold:
                raise Exception("Model is not good try to do more experimentation.")

            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)
            sensor_model = ActivityModel(preprocessor=preprocessor,model=model)
            save_object(self.model_trainer_config.trained_model_file_path, obj=sensor_model)

            #Model Trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path, 
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric)
            
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise ActivityException(e,sys) from e
