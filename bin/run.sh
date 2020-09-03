export MLFLOW_TRACKING_URI=databricks
export EXPERIMENT_NAME=/Users/joshua.cook@databricks.com/building-deploying
export EXPERIMENT_ID=976445620797865
export GITHUB_REPO=https://github.com/databricks-edu/Deploying-ML-Models-At-Scale
mlflow run . \
  --backend databricks \
  --backend-config data/cluster.json \
  --experiment-id $EXPERIMENT_ID \
  --entry-point etl \
  --param-list username=joshuacook
mlflow run . \
  --backend databricks \
  --backend-config data/cluster.json \
  --experiment-id $EXPERIMENT_ID \
  --entry-point experiment \
  --param-list username=joshuacook \
  --param-list penalty=l1 \
  --param-list max_iter=10000 \
  --param-list experiment_name=$EXPERIMENT_NAME
