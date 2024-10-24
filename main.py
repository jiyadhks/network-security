from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import os
import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info("Initiate the data ingestion")
        #data_ingestion_artifact = DataIngestionArtifact
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact.train_file_path)
        print(data_ingestion_artifact.test_file_path)
        logging.info("Data initiation completed")
    except Exception as e:
        raise NetworkSecurityException(e, sys)