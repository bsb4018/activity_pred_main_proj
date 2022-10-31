from re import A
import sys
import numpy as np
import pandas as pd
from typing import Optional
from activity.configuration.mongo_db_connection import MongoDBClient
from activity.constant.database import DATABASE_NAME
from activity.exception import ActivityException

class ActivityData:
    """
    export mongodb record to pandas dataframe
    """
    def __init__(self):

        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise ActivityException(e, sys)

        def export_collection_as_dataframe(self,\
            collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:

            try:
                if database_name is None:
                    collection = self.mongo_client.database[collection_name]
                else:
                    collection = self.mongo_client[database_name][collection_name]
            
                #Find all the records -> make a list -> create a dataframe
                df = pd.DataFrame(list(collection.find())) 
                if "_id" in df.columns.to_list():
                    df = df.drop(columns=['_id'], axis=1) #drop the id field created by mongodb
            
                df.replace({"na": np.nan}, inplace=True) # replace the na with nan
                return df

            except Exception as e:
                raise ActivityException(e, sys)
