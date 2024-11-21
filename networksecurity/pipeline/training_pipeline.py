import os
import sys
from dotenv import load_dotenv
load_dotenv()
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    TrainingPipelineConfig
)
from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)
from networksecurity.constants.training_pipeline import TRAINING_BUCKET_NAME
from networksecurity.cloud.s3_syncer import S3Sync

class TrainingPipeline:
    def __init__(self) -> None:
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3Sync(
            self.training_pipeline_config.aws_access_key,
            self.training_pipeline_config.aws_secret_key,
            self.training_pipeline_config.training_bucket_region,
            self.training_pipeline_config.training_bucket_name
        )

    def start_data_ingestion(self):
        try:
            logging.info("Initiate the data ingestion")
            data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_validation(self, data_ingestion_artifact : DataIngestionArtifact):
        try:
            logging.info("Initiate the data validation")
            data_validation_config = DataValidationConfig(self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Data validation completed")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_transformation(self, data_validation_artifact : DataValidationArtifact):
        try:
            logging.info("Initiate the data transformation")
            data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            data_transformation = DataTransformation(data_transformation_config, data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Data transformation completed")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_model_training(self, data_transformation_artifact : DataTransformationArtifact):
        try:
            logging.info("Initiate the model training")
            model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
            model_trainer_artifcat = model_trainer.initiate_model_trainer()
            logging.info("Model training completed")
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    ## local artifact is going to s3 bucket    
    def sync_artifact_dir_to_s3(self):
        try:
            self.s3_sync.upload_directory(local_folder=self.training_pipeline_config.artifact_name, s3_folder=self.training_pipeline_config.artifact_name)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    ## local final model is getting pushed to s3 bucket
    def sync_saved_model_dir_to_s3(self):
        try:
            self.s3_sync.upload_directory(self.training_pipeline_config.model_dir, self.training_pipeline_config.model_dir)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def run_pipeline(self):
        try:
            logging.info("Training pipeline started")
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact = self.start_model_training(data_transformation_artifact)

            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
            logging.info("Training pipeline completed")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)