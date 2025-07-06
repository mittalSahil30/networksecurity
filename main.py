from network_security.components.data_ingestion import DataIngestion
from network_security.exception.exception import networkSecurityException
from network_security.logging.logger import  logging
from network_security.entity.configentity import DataIngestionConfig
from network_security.entity.configentity import TrainingPipelineConfig
import sys


if __name__=='__main__':
  try:
    trainingPipelineconfig = TrainingPipelineConfig()
    dataingestionconfig = DataIngestionConfig(trainingPipelineconfig)
    dataIngestion = DataIngestion(dataingestionconfig)
    
    dataingestionartifact = dataIngestion.initiate_data_ingestion()
    print(dataingestionartifact)
    
    logging.info("Initiate data ingestion")
   
  except Exception as e:
    raise networkSecurityException(e,sys)