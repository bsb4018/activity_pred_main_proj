import sys

from activity.components.data_ingestion import DataIngestion
from activity.components.data_validation import DataValidation
from activity.components.data_transformation import DataTransformation
from activity.components.model_trainer import ModelTrainer
from activity.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig, ModelTrainerConfig
from activity.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact
from activity.exception import ActivityException
from activity.logger import logging

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info(
              "Entered the start_data_ingestion method of TrainPipeline class"
            )
            logging.info("Getting the data from mongodb")
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train_set and test_set from mongodb")
            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )
            return data_ingestion_artifact
    
        except Exception as e:
            raise ActivityException(e, sys) from e
    

    def start_data_validation(
        self, data_ingestion_artifact: DataIngestionArtifact
    ) -> DataValidationArtifact:
        
        logging.info("Entered the start_data_validation method of TrainPipeline class")
  
        try:
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")
            logging.info(
                "Exited the start_data_validation method of TrainPipeline class"
            )

            return data_validation_artifact

        except Exception as e:
            raise ActivityException(e,sys) from e

    def start_data_transformation(
        self, data_ingestion_artifact: DataIngestionArtifact
    ) -> DataTransformationArtifact:
        try:
            data_transformation = DataTransformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_transformation_config=self.data_transformation_config,
            )
            data_transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )
            return data_transformation_artifact
        except Exception as e:
            raise ActivityException(e, sys) from e

    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except  Exception as e:
            raise  ActivityException(e,sys)

   
    def run_pipeline(self,) -> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact
            )
            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact
            )
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)

        except Exception as e:
            raise ActivityException(e, sys) from e