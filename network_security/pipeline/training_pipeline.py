import os
import sys


from network_security.exception.exception import networkSecurityException
from network_security.logging.logger import logging

from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_valildation import dataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_trainer import ModelTrainer

from network_security.entity.configentity import (
  TrainingPipelineConfig,
  DataIngestionConfig,
  dataValidationConfig,
  DataTransformationConifg,
  ModelTrainerConfig
)

from network_security.entity.artifact_entity import (
  DataIngestionArtifact,
  DataTransformationArtifact,
  DataValidationArtifact,
  ModelTrainerArtifacts
)


class TrainingPipeline:
  def __init__(self):
    self.training_pipeline_config=TrainingPipelineConfig()
    
  def start_data_ingestion(self):
    try:
      self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
      
      logging.info("start data ingestion")
      data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
      
      data_ingestion_artifact = DataIngestion.initiate_data_ingestion()
      logging.info(f"data initiated completed and artifact: {data_ingestion_artifact}")
      return data_ingestion_artifact
    except Exception as e:
      raise networkSecurityException(e, sys)
      
  def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
    try:
      datavalidationconfig = dataValidationConfig(training_pipeline_config = self.training_pipeline_config)
      data_validation = dataValidation(dataingestionartifact=data_ingestion_artifact, dataValidationconfig=datavalidationconfig)
      logging.info("initiate data validation")
      data_validation_artifact = data_validation.initiate_data_validation()
      logging.info(f"initiated completed and artifact: {data_validation_artifact}")
      return data_validation_artifact
    except Exception as e:
      raise networkSecurityException(e,sys)
    
  def start_data_transformation(self, data_validation_artifact: DataValidationArtifact):
    try:
      data_transformation_config = DataTransformationConifg(trainingpipelineconfig=self.training_pipeline_config)
      data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=data_transformation_config)
      logging.info("initiate data transformation")
      data_transformation_artifact = data_transformation.initiate_data_transformation()
      logging.info(f"initiated completed and artifact {data_transformation_artifact}")
      return data_transformation_artifact
    except Exception as e:
      raise networkSecurityException(e, sys)
    
  def start_model_trainer(self, data_transformation_artifact: DataTransformation) ->ModelTrainerArtifacts:
    try:
      logging.info("model training started")
      model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
      model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
      model_trainer_artifacts = model_trainer.initiate_model_trainer()
      logging.info(f"model training completed and artifact {model_trainer_artifacts}")
      return model_trainer_artifacts
    except Exception as e:
      raise networkSecurityException(e, sys)
    
  def runPipeline(self):
    try:
      data_ingestion_artifact = self.start_data_ingestion()
      data_validataion_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
      data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validataion_artifact)
      model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
      return model_trainer_artifact
    except Exception as e:
      raise networkSecurityException(e, sys)
    