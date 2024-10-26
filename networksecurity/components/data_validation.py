from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file

import os
import sys
import numpy as np
import pymongo
import pandas as pd
from typing import List
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig) -> None:
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def validate_number_of_columns(self, dataframe:pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config['columns'])
            logging.info(f"Required number of columns : {number_of_columns}")
            logging.info(f"Dataframe has columns : {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            else:
                return False
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def validate_number_of_numerical_columns(self, dataframe:pd.DataFrame) -> bool:
        try:
            number_of_numerical_columns = len(self._schema_config['numerical_columns'])
            numeber_of_numerical_columns_dataframe = len(dataframe.select_dtypes(include=['int','float']).columns)
            logging.info(f"Required number of numerical columns : {number_of_numerical_columns}")
            logging.info(f"Dataframe has numerical columns : {numeber_of_numerical_columns_dataframe}")
            if numeber_of_numerical_columns_dataframe == number_of_numerical_columns:
                return True
            else:
                return False
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def detect_dataset_drift(self, base_df: pd.DataFrame, current_df:pd.DataFrame,threshold=0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]

                is_same_dist  = ks_2samp(data1=d1,data2=2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column:{
                    "p_value": float(is_same_dist.pvalue),
                    "drift_status": is_found
                }})
            drift_report_filepath = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_filepath)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_filepath, content=report)
            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)



    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            ## Read the data from train and test
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            ## Validate number of columns
            status = self.validate_number_of_columns(dataframe=train_df)
            if not status:
                error_message = f"Train dataframe doesnot contain all columns. \n"
            
            status = self.validate_number_of_columns(dataframe=test_df)
            if not status:
                error_message = f"{error_message} Test dataframe doesnot contain all columns. \n"

            ## Validate numerical columns
                        ## Validate number of columns
            status = self.validate_number_of_numerical_columns(dataframe=train_df)
            if not status:
                error_message = f"Train dataframe doesnot contain all numerical columns. \n"
            
            status = self.validate_number_of_numerical_columns(dataframe=test_df)
            if not status:
                error_message = f"{error_message} Test dataframe doesnot contain all numerical columns. \n"

            ## Check data drift
            status = self.detect_dataset_drift(base_df=train_df, current_df=test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_df.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True
            )
            test_df.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                valid_test_file_path = self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path = None,
                invalid_test_file_path = None,
                drift_report_file_path = self.data_validation_config.drift_report_file_path
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)