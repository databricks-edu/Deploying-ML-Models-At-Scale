export MLFLOW_TRACKING_URI=databricks
export EXPERIMENT_ID=2430152573816303
mlflow run https://github.com/databricks-edu/Deploying-ML-Models-At-Scale \
  --version databricks \
  --backend databricks \
  --backend-config data/cluster.json \
  --experiment-id $EXPERIMENT_ID \
  --entry-point load_data \
  --param-list username=joshuacook \
  --param-list filename=user_profile_data.snappy.parquet \
  --param-list kind=user
