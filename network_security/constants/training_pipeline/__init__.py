import os
import sys
import numpy as np
import pandas as pd




"""
defing some more constant for training pipeline
"""
TARGET_COLUMN = "RESULT"
PIPELINE_NAME = "NetworkSecurity"
ARTIFACT_DIR  = "Artifacts"
FILE_NAME = "phisingData.csv"

TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME = "test.csv"

"""
Data ingestion constant start with data ingestion var name
"""

DATA_INGESTION_COLLECTION_NAME: str = "networkdata"
DATA_INGESTION_DATABASE_NAME: str = "Sahil"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float= 0.2