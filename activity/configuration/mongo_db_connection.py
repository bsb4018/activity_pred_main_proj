import os
import sys
import certifi
import pymongo

from activity.constant.database import DATABASE_NAME
from activity.constant.env_variable import MONGODB_URL_KEY
from activity.exception import ActivityException

ca = certifi.where() #Reference the installed certificate authority(CA) bundle


class MongoDBClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, \
                    tlsCAFile = ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise ActivityException(e, sys)    
