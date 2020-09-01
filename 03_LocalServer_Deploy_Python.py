# Databricks notebook source
# MAGIC %md ## Launch local server - Programmatic with Python
# MAGIC * Launch MLflow scoring server: `mlflow models serve`
# MAGIC * Invoke server with data to predict

# COMMAND ----------

# MAGIC %md ### Setup

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()
host_name = dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().get("browserHostName").get()
dbutils.fs.put("file:///root/.databrickscfg",f"[DEFAULT]\nhost=https://{host_name}\ntoken = "+token,overwrite=True)

# COMMAND ----------

# MAGIC %md ### Launch scoring server

# COMMAND ----------

# MAGIC %md #### Define functions

# COMMAND ----------

import sys
from subprocess import Popen
def run_local_webserver(model_uri, port):
    cmd = f"mlflow models serve --port {port} --model-uri {model_uri}"
    print("Command:",cmd)
    cmd = cmd.split(" ")
    #return Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, universal_newlines=True)
    return Popen(cmd, universal_newlines=True)

# COMMAND ----------

import requests
def call_server(api_uri, data):
    headers = { "Content-Type": "application/json" }
    rsp = requests.post(api_uri, headers=headers, data=data)
    print(f"call_server: status_code={rsp.status_code}")
    if rsp.status_code < 200 or rsp.status_code > 299:
        return None
    return rsp.text

# COMMAND ----------

import time
import requests
sleep_time = 2
iterations = 10000
def wait_until_ready(uri, data):
    start = time.time()
    for j in range(iterations):
        rsp = None
        try:
            rsp = call_server(uri, data)
        except requests.exceptions.ConnectionError as e:
            print(f"Calling scoring server: {j}/{iterations}")
        if rsp is not None:
            print(f"Done waiting for {time.time()-start:5.2f} seconds")
            return rsp
        time.sleep(sleep_time)
    raise Exception(f"ERROR: Timed out after {iterations} iterations waiting for server to launch")

# COMMAND ----------

# MAGIC %md #### Launch the server

# COMMAND ----------

proc = run_local_webserver(model_uri, 54322)
proc.pid

# COMMAND ----------

# MAGIC %md #### Wait until the server is ready

# COMMAND ----------

data = '{ "columns": [ "fixed acidity", "volatile acidity", "citric acid", "residual sugar", "chlorides", "free sulfur dioxide", "total sulfur dioxide", "density", "pH", "sulphates", "alcohol" ], "data": [ [ 7,   0.27, 0.36, 20.7, 0.045, 45, 170, 1.001,  3,    0.45,  8.8 ], [ 6.3, 0.3,  0.34,  1.6, 0.049, 14, 132, 0.994,  3.3,  0.49,  9.5 ], [ 8.1, 0.28, 0.4,   6.9, 0.05,  30,  97, 0.9951, 3.26, 0.44, 10.1 ] ] }'

# COMMAND ----------

uri = "http://localhost:54322/invocations"
wait_until_ready(uri, data)

# COMMAND ----------

# MAGIC %sh ps -fae | grep python | grep -v PythonShell

# COMMAND ----------

# MAGIC %md ### Call scoring server with data for prediction

# COMMAND ----------

# MAGIC %sh
# MAGIC curl -s http://0.0.0.0:54322/invocations \
# MAGIC -H 'Content-Type: application/json' \
# MAGIC -d '{ "columns": [ "fixed acidity", "volatile acidity", "citric acid", "residual sugar", "chlorides", "free sulfur dioxide", "total sulfur dioxide", "density", "pH", "sulphates", "alcohol" ], "data": [ [ 7,   0.27, 0.36, 20.7, 0.045, 45, 170, 1.001,  3,    0.45,  8.8 ], [ 6.3, 0.3,  0.34,  1.6, 0.049, 14, 132, 0.994,  3.3,  0.49,  9.5 ], [ 8.1, 0.28, 0.4,   6.9, 0.05,  30,  97, 0.9951, 3.26, 0.44, 10.1 ] ] }
# MAGIC '
