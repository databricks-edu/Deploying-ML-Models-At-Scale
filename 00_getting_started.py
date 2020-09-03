# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC # Getting Started

# COMMAND ----------

# MAGIC %md ## Configuration

# COMMAND ----------

# MAGIC %run ./includes/utilities

# COMMAND ----------

# MAGIC %md ## Retrieve and Load the Data
# MAGIC
# MAGIC We will be working with two files:
# MAGIC
# MAGIC - "health_profile_data.snappy.parquet"
# MAGIC - "user_profile_data.snappy.parquet"
# MAGIC
# MAGIC These files can be retrieved and loaded using the utility function `process_file`
# MAGIC
# MAGIC This function takes three arguments:
# MAGIC
# MAGIC - `file_name: str`
# MAGIC    - the name of the file to retrieve
# MAGIC - `path: str`
# MAGIC    - the location to write the file as a Delta table
# MAGIC - `table_name: str`
# MAGIC    - the name of a table to be used in the Metastore to reference the data
# MAGIC
# MAGIC This function does three things:
# MAGIC
# MAGIC 1. Retrieve a file and load it into your Databricks Workspace.
# MAGIC 1. Create a Delta table using the file.
# MAGIC 1. Register the Delta table in the Metastore so that it can be
# MAGIC    referenced using SQL or a PySpark `table` reference.

# COMMAND ----------

# MAGIC %md ### Retrieve and Load the Data
# MAGIC
# MAGIC Retrieve the data using the following arguments:
# MAGIC
# MAGIC | `file_name` | `path` | `table_name` |
# MAGIC |:-:|:-:|:-|
# MAGIC | `health_profile_data.snappy.parquet` | `silverDailyPath` | `health_profile_data` |
# MAGIC | `user_profile_data.snappy.parquet`   | `dimUserPath`     | `user_profile_data`   |

# COMMAND ----------

# TODO
# # Use the utility function `process_file` to retrieve the data
# # Use the arguments in the table above.
#
# process_file(
#   FILL_IN_FILE_NAME,
#   FILL_IN_PATH,
#   FILL_IN_TABLE_NAME
# )
#
# process_file(
#   FILL_IN_FILE_NAME,
#   FILL_IN_PATH,
#   FILL_IN_TABLE_NAME
# )

# COMMAND ----------

# ANSWER
process_file(
  "health_profile_data.snappy.parquet",
  silverDailyPath,
  "health_profile_data"
)
process_file(
  "user_profile_data.snappy.parquet",
  dimUserPath,
  "user_profile_data"
)

# COMMAND ----------

# MAGIC %md ## Data Availability
# MAGIC
# MAGIC In a typical workflow, data will have been made available to you
# MAGIC as tables that can be queried using SQL or PySpark. This function
# MAGIC `process_file` has performed the steps necessary to make the files
# MAGIC available to your workspace so that you can focus on data science.
# MAGIC This mirrors a typical workflow, where the data has been made
# MAGIC available to you by a data engineer.
