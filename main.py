from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_valildation import dataValidation
from network_security.exception.exception import networkSecurityException
from network_security.logging.logger import  logging
from network_security.entity.configentity import DataIngestionConfig, dataValidationConfig
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

  except Exception as e:
    raise networkSecurityException(e,sys)