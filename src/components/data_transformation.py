"""
Data Transformation Module

This module handles the preprocessing and transformation of data for machine learning.
It includes pipelines for numerical and categorical features with appropriate imputation,
encoding, and scaling strategies.
"""

import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from pandas.core.arrays import categorical

# sklearn imports for data preprocessing
from sklearn.compose import ColumnTransformer  # For applying different transformers to different columns
from sklearn.impute import SimpleImputer  # For handling missing values
from sklearn.pipeline import Pipeline  # For chaining multiple preprocessing steps
from sklearn.preprocessing import OneHotEncoder, StandardScaler  # For encoding categorical features and scaling

# Custom imports for error handling and logging
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

# @dataclass decorator automatically generates __init__, __repr__, and other special methods
# This makes the configuration class cleaner and easier to use
@dataclass
class DataTransformationConfig:
    """
    Configuration class for data transformation.
    Stores the file path where the preprocessor object will be saved.
    """
    preprocessor_obj_file_path = os.path.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    """
    Class responsible for creating data transformation pipelines.
    
    This class creates separate preprocessing pipelines for numerical and categorical features,
    which are then combined using ColumnTransformer to handle different data types appropriately.
    """
    
    def __init__(self):
        """
        Initialize the DataTransformation class with configuration settings.
        """
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        Creates and returns a data transformer object with preprocessing pipelines.
        
        This method defines:
        1. Numerical columns pipeline: handles missing values with median imputation and standard scaling
        2. Categorical columns pipeline: handles missing values with mode imputation, one-hot encoding, and scaling
        
        Returns:
            ColumnTransformer: A transformer object that applies different pipelines to different column types
        
        Why median for numerical features?
        - Median is robust to outliers (unlike mean)
        - Preserves the distribution better for skewed data
        - Represents a meaningful central value for continuous features
        
        Why mode (most_frequent) for categorical features?
        - Mean and median don't make sense for categorical data
        - Mode represents the most common category
        - Preserves the original distribution of categories
        """
        try:
            # Define numerical columns (continuous/discrete numeric features)
            numerical_columns = ["writing_score", "reading_score"]
            
            # Define categorical columns (nominal/ordinal features)
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            # Pipeline for numerical features
            # Steps are applied sequentially: imputation -> scaling
            num_pipeline = Pipeline(
                steps = [
                    # Step 1: Impute missing values using median strategy
                    # Median is chosen because it's robust to outliers and works well for skewed distributions
                    ("imputer", SimpleImputer(strategy="median")),
                    
                    # Step 2: Standardize features (mean=0, std=1)
                    # This ensures all numerical features are on the same scale for better model performance
                    ("scaler", StandardScaler())
                ]
            )

            logging.info(f"Numerical columns: {numerical_columns}")

            # Pipeline for categorical features
            # Steps are applied sequentially: imputation -> encoding -> scaling
            cat_pipeline = Pipeline(
                steps = [
                    # Step 1: Impute missing values using most_frequent (mode) strategy
                    # Mode is the only meaningful central tendency measure for categorical data
                    # It replaces missing values with the most frequently occurring category
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    
                    # Step 2: One-hot encode categorical features
                    # Converts categorical variables into binary (0/1) columns
                    # Each category becomes a separate binary feature
                    ("one_hot_encoder", OneHotEncoder()),
                    
                    # Step 3: Standardize the encoded features
                    # Even after one-hot encoding, scaling helps with model convergence and performance
                    # with_mean must be False because one-hot output is sparse; centering would densify.
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )
            
            logging.info(f"Categorical columns: {categorical_columns}")
            
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            
            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = "math_score"
            numerical_columns = ["writing_score", "reading_score"]\

            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e, sys)