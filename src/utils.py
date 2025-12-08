import os
import sys
import dill
import numpy as np
import pandas as pd

from src.exception import CustomException

def save_object(file_path, obj): # target path and object to serialize
    try:
        # compute the directory path of the target path (empty if only filename provided).
        dir_path = os.path.dirname(file_path)

        # Ensure the directory exists so the file write won't fail.
        os.makedirs(dir_path, exist_ok=True)

        # Open the target path in binary write mode and serialize the object with dill.
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    
    except Exception as e:
        # Standardize error handling with project-specific exception wrapper.
        raise CustomException(e, sys)