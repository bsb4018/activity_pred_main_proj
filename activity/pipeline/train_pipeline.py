import sys

from activity.components.data_ingestion import DataIngestion
from activity.components.data_validation import DataValidation
from activity.components.data_transformation import DataTransformation
from activity.components.model_trainer import ModelTrainer
from activity.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig, ModelTrainerConfig, TrainingPipelineConfig
from activity.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact
from activity.exception import ActivityException
from activity.logger import logging

class TrainPipeline:
    is_pipeline_running=False
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info(
              "Entered the start_data_ingestion method of TrainPipeline class"
            )
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            
            logging.info("Starting data ingestion")
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion completed and artifact: {data_ingestion_artifact}")
            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )
            return data_ingestion_artifact
    
        except Exception as e:
            raise ActivityException(e, sys) from e
    

    def start_data_validation(
        self, data_ingestion_artifact: DataIngestionArtifact
    ) -> DataValidationArtifact:
      
        try:
            logging.info("Entered the start_data_validation method of TrainPipeline class")
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=data_validation_config
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
        self, data_validation_artifact:DataValidationArtifact
    ) -> DataTransformationArtifact:
        try:
            logging.info("Entered the start_data_transformation method of TrainPipeline class")
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)

            data_transformation = DataTransformation(
               data_validation_artifact = data_validation_artifact,
               data_transformation_config = data_transformation_config,
            )
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            
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
            TrainPipeline.is_pipeline_running=True
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)

        except Exception as e:
            raise ActivityException(e, sys) from e