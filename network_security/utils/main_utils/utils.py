import yaml
from network_security.exception.exception import networkSecurityException
from network_security.logging.logger import logging
import os, sys
import dill
import pandas as pd
import numpy as np
import pickle

def read_yaml_file(file_path: str)->dict:
  try: 
    with open(file_path, "rb") as yaml_file:
      return yaml.safe_load(yaml_file)
  except Exception as e:
    raise networkSecurityException(e, sys)
  
def write_yaml_file(file_path: str, content: object, replace: bool = False)->None:
  try:
    if replace:
      if os.path.exists(file_path):
        os.remove(file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
      yaml.dump(content, file)
  except Exception as e:
    raise networkSecurityException(e, sys)