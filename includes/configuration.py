# Databricks notebook source
# MAGIC %md Define Data Paths.

# COMMAND ----------

# TODO
# username = FILL_THIS_IN
# experiment_id = None

# COMMAND ----------

# ANSWER
username = "dbacademy"
experiment_id = None

# COMMAND ----------

projectPath     = f"/dbacademy/{username}/mlmodels/profile/"
landingPath     = projectPath + "landing/"
silverDailyPath = projectPath + "daily/"
dimUserPath     = projectPath + "users/"
goldPath        = projectPath + "gold/"

# COMMAND ----------

# SOURCE_ONLY
local = False

import os
HOME = os.environ["HOME"]
if HOME == '/home/jovyan':
  local = True
  from includes.dbutils import DatabricksUtilitiesEmulator
  dbutils = DatabricksUtilitiesEmulator()
  from pyspark import sql

  os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages "io.delta:delta-core_2.11:0.5.0" pyspark-shell'

  spark = sql.SparkSession.builder \
          .master("local[8]") \
          .getOrCreate()

  projectPath     = f"dbacademy/mlmodels/profile/"
  landingPath     = projectPath + "landing/"
  silverDailyPath = projectPath + "daily/"
  dimUserPath     = projectPath + "users/"
  goldPath        = projectPath + "gold/"

  def display(df):
    return df.show()

# COMMAND ----------

# MAGIC %md Configure Database

# COMMAND ----------

spark.sql(f"CREATE DATABASE IF NOT EXISTS dbacademy_{username}")
spark.sql(f"USE dbacademy_{username}");
