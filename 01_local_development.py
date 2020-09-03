# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC # Local Development

# COMMAND ----------

# MAGIC %md ### Clone the Webinar Project
# MAGIC
# MAGIC The Webinar repo is available at the following location:
# MAGIC
# MAGIC ```
# MAGIC https://github.com/databricks-edu/Deploying-ML-Models-At-Scale
# MAGIC ```
# MAGIC Use `git` to clone the project to your system with this command:
# MAGIC
# MAGIC ```
# MAGIC git clone https://github.com/databricks-edu/Deploying-ML-Models-At-Scale.git
# MAGIC ```
# MAGIC
# MAGIC When it completes cloning, change directories to work in the new project:
# MAGIC
# MAGIC ```
# MAGIC cd Deploying-ML-Models-At-Scale/
# MAGIC ```

# COMMAND ----------

# MAGIC %md ### Configuring Conda
# MAGIC We will use Conda in this webinar both to configure our local and databricks environments while working.
# MAGIC
# MAGIC This webinar will not discuss conda installation and will assume that you already have conda running on your system.
# MAGIC
# MAGIC You can visit [https://docs.conda.io/projects/conda/en/latest/user-guide/install](https://docs.conda.io/projects/conda/en/latest/user-guide/install)
# MAGIC for more information about installing Conda.
# MAGIC
# MAGIC #### Conda Version
# MAGIC
# MAGIC You can see which version of conda you have installed on your system
# MAGIC with the command `conda --version`.
# MAGIC
# MAGIC #### Conda Environment
# MAGIC
# MAGIC Before we begin, you should create a new conda environment
# MAGIC for this webinar.
# MAGIC
# MAGIC You can create the new environment with this command:
# MAGIC
# MAGIC ```
# MAGIC conda create --name building-deploying python=3.7.6
# MAGIC ```

# COMMAND ----------

import sys
sys.version

# COMMAND ----------

# MAGIC %md
# MAGIC #### Activate Conda Environment
# MAGIC
# MAGIC Activate the new conda environment with this command:
# MAGIC ```
# MAGIC conda activate building-deploying
# MAGIC ```

# COMMAND ----------

# MAGIC %md ### Install Databricks Interfaces
# MAGIC
# MAGIC ```
# MAGIC pip install databricks databricks-connect mlflow
# MAGIC ```

# COMMAND ----------

# MAGIC %md ### Configure Databricks CLI
# MAGIC
# MAGIC Use this command to display options available to you with the
# MAGIC Databricks CLI:
# MAGIC
# MAGIC ```
# MAGIC databricks -h
# MAGIC ```
# MAGIC
# MAGIC Use this command to connect the CLI to your Workspace:
# MAGIC
# MAGIC ```
# MAGIC databricks configure
# MAGIC ```
# MAGIC
# MAGIC Use these options:
# MAGIC
# MAGIC - Databricks Host: the URL of your Databricks Workspace
# MAGIC - Username: your username in that Workspace
# MAGIC - Password: An [Access Token](https://docs.databricks.com/dev-tools/api/latest/authentication.html) generated for your Workspace User
# MAGIC
# MAGIC You can view the contents of your Databricks CLI configuration file with this command:
# MAGIC
# MAGIC ```
# MAGIC less ~/.databrickscfg
# MAGIC ```
# MAGIC
# MAGIC Press `q` to exit.

# COMMAND ----------

# MAGIC %md ### Identify Cluster to Use with Databricks Connect
# MAGIC
# MAGIC I used this command to identify the cluster to use with Databricks Connect:
# MAGIC
# MAGIC ```
# MAGIC databricks clusters list | grep joshua
# MAGIC ```

# COMMAND ----------

# MAGIC %md ### Configure Databricks Connect
# MAGIC
# MAGIC Use the command
# MAGIC
# MAGIC ```
# MAGIC databricks-connect configure
# MAGIC ```
# MAGIC
# MAGIC You should be able to use the default options.
# MAGIC
# MAGIC #### Test Databricks Connect
# MAGIC
# MAGIC This may fail if you don't have JDK 8 installed. You can install the
# MAGIC open JDK 8 by visiting this link: https://adoptopenjdk.net/
# MAGIC

# COMMAND ----------

# MAGIC %md ### Test the ETL Spark Job
# MAGIC
# MAGIC Use this command to test the ETL spark job:
# MAGIC
# MAGIC ```
# MAGIC spark-submit includes/main/python/etl.py --username FILL_IN_YOUR_USERNAME
# MAGIC ```

# COMMAND ----------

# MAGIC %md ### Configure MLflow
# MAGIC
# MAGIC Run the following to configure MLflow to use Databricks.
# MAGIC
# MAGIC 1. `export MLFLOW_TRACKING_URI=databricks`
# MAGIC     - this tells MLflow to use Databricks to manage experiments
# MAGIC 1. `mlflow create -n /Users/YOUR_DATABRICKS_USER/building-deploying`
# MAGIC     - this will create a new experiment in the Databricks Workspace
# MAGIC     - make note of the resulting experiment id
# MAGIC 1. `export EXPERIMENT_NAME=/Users/YOUR_DATABRICKS_USER/building-deploying`

# COMMAND ----------

# MAGIC %md ### Install Scikit-Learn in Conda Environment
# MAGIC
# MAGIC ```
# MAGIC pip install sklearn
# MAGIC ```

# COMMAND ----------

# MAGIC %md ### Test the Experiment Spark Job
# MAGIC
# MAGIC Use this command to test the ETL spark job:
# MAGIC
# MAGIC ```
# MAGIC spark-submit includes/main/python/experiment.py --penalty l1 --max-iter 10000 --username joshuacook --experiment-name $EXPERIMENT_NAME
# MAGIC ```
