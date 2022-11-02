import os
import path
import sys
import dill
import numpy as np
import yaml

from activity.exception import ActivityException
from activity.logger import logging

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
            
    except Exception as e:
        raise ActivityException(e,sys) from e
