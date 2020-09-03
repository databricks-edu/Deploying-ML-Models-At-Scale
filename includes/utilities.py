# Databricks notebook source
from pyspark.sql import SparkSession
from urllib.request import urlretrieve

# COMMAND ----------

# MAGIC %run ./configuration

# COMMAND ----------

# SOURCE_ONLY
local = False

import os
HOME = os.environ["HOME"]
if HOME == '/home/jovyan':
  get_ipython().run_line_magic('run', 'includes/configuration')
  from includes.dbutils import DatabricksUtilitiesEmulator
  dbutils = DatabricksUtilitiesEmulator()
  from pyspark.sql import SparkSession

# COMMAND ----------

print("Include configuration notebook.")

# COMMAND ----------

def retrieve_data(file: str) -> bool:
  """Download file from remote location to driver. Move from driver to DBFS."""

  base_url = "https://files.training.databricks.com/static/data/health-tracker/"
  url = base_url + file
  driverPath = "file:/databricks/driver/" + file
  dbfsPath   = landingPath + file
  urlretrieve(url, file)
  dbutils.fs.mv(driverPath , dbfsPath)
  return True

def load_delta_table(file: str, delta_table_path: str) -> bool:
  "Load a parquet file as a Delta table."
  parquet_df = spark.read.format("parquet").load(landingPath + file)
  parquet_df.write.format("delta").save(delta_table_path)
  return True

def process_file(file_name: str, path: str,  table_name: str) -> bool:
  """
  1. retrieve file
  2. load as delta table
  3. register table in the metastore
  """

  retrieve_data(file_name)
  print(f"Retrieve {file_name}.")

  load_delta_table(file_name, path)
  print(f"Load {file_name} to {path}")

  spark.sql(f"""
  DROP TABLE IF EXISTS {table_name}
  """)

  spark.sql(f"""
  CREATE TABLE {table_name}
  USING DELTA
  LOCATION "{path}"
  """)

  print(f"Register {table_name} using path: {path}")
