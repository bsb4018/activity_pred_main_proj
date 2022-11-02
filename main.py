from activity.configuration.mongo_db_connection import MongoDBClient
from activity.exception import ActivityException
import os,sys
from activity.logger import logging
from activity.pipeline import train_pipeline
from activity.pipeline.train_pipeline import TrainPipeline

if __name__ == '__main__':
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)
