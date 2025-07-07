from network_security.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from network_security.entity.configentity import dataValidationConfig
from network_security.constants.training_pipeline import SCHEMA_FILE_PATH
from network_security.exception.exception import networkSecurityException
from network_security.logging.logger import logging
from scipy.stats import ks_2samp
import pandas as pd
import os, sys
from network_security.utils.main_utils.utils import read_yaml_file, write_yaml_file

class dataValidation:
  def __init__(self, dataingestionartifact:DataIngestionArtifact, dataValidationconfig: dataValidationConfig):
    try:
      self.data_ingestion_artifact = dataingestionartifact
      self.dataValidationConfig = dataValidationconfig
      self._schemaconfig = read_yaml_file(SCHEMA_FILE_PATH)
      
    except Exception as e:
      raise networkSecurityException(e, sys)
  
  @staticmethod
  def read_data(file_path)->pd.DataFrame:
    try:
      return pd.read_csv(file_path)
    
    except Exception as e:
      raise networkSecurityException(e, sys)

  def validate_no_of_columns(self, dataFrame: pd.DataFrame)->bool:
    try:
       number_of_columns=len(self._schemaconfig)
       
       logging.info(f"Required number of columns: {number_of_columns}")
       logging.info(f"DataFrame has columns: {len(dataFrame.columns)}")
       
       if len(dataFrame.columns) == number_of_columns:
         return True
       return False
    except Exception as e:
      raise networkSecurityException(e, sys)
    
  def validate_numerical_columns(self, dataframe: pd.DataFrame) -> bool:
    try:
      no_of_numerical_columns = len(self._schemaconfig["numerical_columns"])
      
      ls = [column for column in dataframe.columns if dataframe[column].dtype != 'O']
      
      if len(ls) == no_of_numerical_columns:
        return True
      return False
    except Exception as e:
      raise networkSecurityException(e, sys)
    
  def detect_datset_drift(self, base_df, current_df, threshold = 0.05)->bool:
    try:
      status = True
      report = {}
      for column in base_df.columns:
        d1 = base_df[column]
        d2 = current_df[column]
        is_sample= ks_2samp(d1, d2)
        if threshold <= is_sample.pvalue:
          is_found=False
        else:
          is_found = True
          status = False
        report.update({column: {
          "pvalue":float(is_sample.pvalue),
          "drift_status":is_found
        }})
        
      drift_report_file_path = self.dataValidationConfig.drift_report_file_path
      # create directory
      
      dir_path = os.path.dirname(drift_report_file_path)
      os.makedirs(dir_path, exist_ok = True)
      write_yaml_file(file_path=drift_report_file_path, content=report)
      
      return status
    except Exception as e:
      raise networkSecurityException(e, sys)
    
    
  def initiate_data_validation(self) -> DataValidationArtifact:
    
    try:
      train_file_path = self.data_ingestion_artifact.trained_file_path
      test_file_path = self.data_ingestion_artifact.test_file_path
      
      ## reading data from path
      train_dataFrame = dataValidation.read_data(train_file_path)
      test_dataFrame = dataValidation.read_data(test_file_path)
      
      ## validate the number of columns
      
      status = self.validate_no_of_columns(dataFrame=train_dataFrame)
      if not status:
        error_message = f"Train DataFrame does not contain all columns.\n"
        
      status = self.validate_no_of_columns(dataFrame=test_dataFrame)
      if not status:
        error_message = f" Train DataFrame does not contain all columns.\n"
        
      status = self.validate_numerical_columns(dataframe=train_dataFrame)
      if not status:
        error_message = f"Train DataFrame does not contain all numerical columns.\n"
        
      status = self.validate_numerical_columns(dataframe=test_dataFrame)
      if not status:
        error_message = f" Train DataFrame does not contain all numerical columns.\n"
        
      ## let's check datadrift
      status = self.detect_datset_drift(base_df=train_dataFrame, current_df=test_dataFrame)
      dir_path = os.path.dirname(self.dataValidationConfig.valid_train_file_path)
      os.makedirs(dir_path, exist_ok=True)
      
      train_dataFrame.to_csv(self.dataValidationConfig.valid_train_file_path, index= False, header=True)
      
      test_dataFrame.to_csv(self.dataValidationConfig.valid_test_file_path, index= False, header=True)
      
      data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.dataValidationConfig.drift_report_file_path,
            )
      return data_validation_artifact
    except Exception as e:
      raise networkSecurityException(e, sys)
    
