from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_valildation import dataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_trainer import ModelTrainer
from network_security.exception.exception import networkSecurityException
from network_security.logging.logger import  logging
from network_security.entity.configentity import DataIngestionConfig, dataValidationConfig, DataTransformationConifg, ModelTrainerConfig
from network_security.entity.configentity import TrainingPipelineConfig
import sys


if __name__=='__main__':
  try:
    trainingPipelineconfig = TrainingPipelineConfig()
    dataingestionconfig = DataIngestionConfig(trainingPipelineconfig)
    dataIngestion = DataIngestion(dataingestionconfig)
    logging.info("Initiate data ingestion")
    dataingestionartifact = dataIngestion.initiate_data_ingestion()
    print(dataingestionartifact)
    logging.info("initiated completed")
    datavalidationconfig = dataValidationConfig(trainingPipelineconfig)
    data_validation = dataValidation(dataingestionartifact, datavalidationconfig)
    logging.info("initiate data validation")
    data_validation_artifact = data_validation.initiate_data_validation()
    logging.info("initiated completed")
    print(data_validation_artifact)
    
    data_transformation_config = DataTransformationConifg(trainingPipelineconfig)
    data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
    logging.info("initiate data transformation")
    data_transformation_artifact = data_transformation.initiate_data_transformation()
    logging.info("initiated completed")
    print(data_transformation_artifact)
    
    logging.info("model training started")
    model_trainer_config = ModelTrainerConfig(trainingPipelineconfig)
    model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
    model_trainer_artifacts = model_trainer.initiate_model_trainer()
    print(model_trainer_artifacts)
    logging.info("model training completed")

  except Exception as e:
    raise networkSecurityException(e,sys)