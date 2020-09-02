export MLFLOW_TRACKING_URI=databricks
export EXPERIMENT_ID=2430152573816303
mlflow run . \
  --backend databricks \
  --backend-config data/cluster.json \
  --experiment-id $EXPERIMENT_ID \
  --param-list username=joshuacook \
  --param-list penalty=l1 \
  --param-list local=False \
  --param-list use_conda=True
