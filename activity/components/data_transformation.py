from activity.entity.artifact_entity import (DataIngestionArtifact,
                                           DataTransformationArtifact)
from activity.entity.config_entity import DataTransformationConfig

import os,sys
from activity.constant.training_pipeline import TARGET_COLUMN
from activity.exception import ActivityException
from activity.logger import logging
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from activity.ml.model.estimator import TargetValueMapping
from activity.utils.main_utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:      
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise ActivityException(e, sys) from e
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise ActivityException(e,sys) from e

    @classmethod
    def get_data_transformer_object(cls) -> Pipeline:
        '''
        pipeline object to transform the dataset
        '''
        logging.info(
             "Entered get_data_transformer_object method of DataTransformation class"
        )
        try:
            logging.info("Got numerical cols from schema config")
            
            simple_imputer = SimpleImputer(strategy="constant", fill_value=0)
            standard_scaler = StandardScaler()
            
            preprocessor = Pipeline(
                steps=[("Imputer", simple_imputer), ("StandardScaler", standard_scaler)]
            )

            logging.info("Created preprocessor object from ColumnTransformer")

            logging.info(
                "Exited get_data_transformer_object method of DataTransformation class"
            )
            return preprocessor
        
        except Exception as e:
            raise ActivityException(e,sys) from e

    def initiate_data_transformation(self,) -> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")
            preprocessor = self.get_data_transformer_object()
            logging.info("Got the preprocessor object")

            train_df = DataTransformation.read_data(
                file_path=self.data_ingestion_artifact.trained_file_path
            )
            test_df = DataTransformation.read_data(
                file_path=self.data_ingestion_artifact.test_file_path
            )

            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            
            #Train Target Encoding
            target_feature_train_df = target_feature_train_df.replace(
                TargetValueMapping().to_dict()
            )

            logging.info("Got train features and test features of Training dataset")

            
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)

            target_feature_test_df = test_df[TARGET_COLUMN]

            #Test Target Encoding
            target_feature_test_df = target_feature_test_df.replace(
                TargetValueMapping().to_dict()
            )

            logging.info("Got train features and test features of Testing dataset")

            logging.info(
                "Applying preprocessing object on training dataframe and testing dataframe"
            ) 

            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)

            logging.info(
                "Used the preprocessor object to fit transform the train features"
            )

            input_feature_test_arr = preprocessor.transform(input_feature_test_df)

            logging.info(
                "Used the preprocessor object to transform the test features"
            )

            logging.info("Creating train array and test array")

            train_arr = np.c_[
                np.array(input_feature_train_arr), np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                np.array(input_feature_test_arr), np.array(target_feature_test_df)
            ]

            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessor,
            )
            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path,
                array=train_arr,
            )
            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path,
                array=test_arr,
            )
            
            logging.info("Created train array and test array")

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            logging.info("Saved the preprocessor object")

            logging.info(
                "Exited initiate_data_transformation method of Data_Transformation class"
            )
            
            return data_transformation_artifact

        except Exception as e:
            raise ActivityException(e,sys) from e