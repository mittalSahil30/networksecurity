from network_security.constants.training_pipeline import MODEL_FILE_NAME, SAVED_MODEL_DIR

import os, sys

from network_security.exception.exception import networkSecurityException
from network_security.logging.logger import logging


class NetworkModel:
  def __init__(self, preprocessor, model):
    try:
      self.preprocessor = preprocessor
      self.model = model
    except Exception as e:
      raise networkSecurityException(e, sys)
    
  def predict(self, x):
    try:
      x_transform = self.preprocessor.transform(x)
      y_hat = self.model.predict(x_transform)
      return y_hat
    except Exception as e:
      raise networkSecurityException(e, sys)