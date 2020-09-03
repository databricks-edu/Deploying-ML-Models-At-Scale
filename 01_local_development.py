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
