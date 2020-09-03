from pyspark.sql import SparkSession
import click
import mlflow
import numpy as np
import pandas as pd
from typing import Dict, Tuple
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split

spark = SparkSession.builder.master("local[8]").getOrCreate()

def get_param_grid(penalty: str) -> Dict:
    param_grids = {
        "l1" : {
            'C' : np.logspace(-5,5,11),
            "penalty" : ['l1'],
            "solver" : ['saga']
        },
        "l2" : {
            'C' : np.logspace(-5,5,11),
            "penalty" : ['l2']
        },
        "elasticnet" : {
            'C' : np.logspace(-5,5,11),
            "penalty" : ['elasticnet'],
            'l1_ratio' : np.linspace(0,1,11),
            "solver" : ['saga']
        }
    }
    return param_grids[penalty]

def preprocessing(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    ss = StandardScaler()
    le = LabelEncoder()
    features = df.drop("lifestyle", axis=1)
    target = df["lifestyle"]
    target = le.fit_transform(target)

    X_train, X_test, y_train, y_test = train_test_split(features, target)

    X_train_ss = ss.fit_transform(X_train)
    X_test_ss = ss.transform(X_test)

    return (
        X_train_ss,
        X_test_ss,
        y_train,
        y_test
    )

@click.command(help="train a linear model on the data")
@click.option("--penalty", help="l1|l2|elasticnet")
@click.option("--username", help="username unique to dbacademy on this workspace")
@click.option("--max-iter", help="maximum iterations for logistic regression fit")
@click.option("--experiment-name", help="name associated with an mlflow experiment")
def experiment(username: str, penalty: str, max_iter: int, experiment_name: int):

    projectPath     = f"/dbacademy/{username}/mlmodels/profile/"
    goldPath = projectPath + "gold/"
    ht_augmented_path = goldPath + "ht_augmented"

    ht_augmented_df = spark.read.format("delta").load(ht_augmented_path)
    ht_augmented_pandas_df = ht_augmented_df.toPandas()

    (
        X_train,
        X_test,
        y_train,
        y_test
    ) = preprocessing(ht_augmented_pandas_df)

    param_grid = get_param_grid(penalty)

    mlflow.set_tracking_uri("databricks")
    mlflow.set_experiment(experiment_name=experiment_name)
    with mlflow.start_run():
      gs = GridSearchCV(LogisticRegression(max_iter=int(max_iter)), param_grid)
      gs.fit(X_train, y_train)

      train_acc = gs.score(X_train, y_train)
      test_acc = gs.score(X_test, y_test)

      mlflow.sklearn.log_model(gs.best_estimator_, "model")

      for param, value in gs.best_params_.items():
          mlflow.log_param(param, value)
      mlflow.log_metric("train acc", train_acc)
      mlflow.log_metric("test acc", test_acc)

if __name__ == '__main__':
    experiment()
