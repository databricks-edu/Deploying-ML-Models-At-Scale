import click
import os

GIT_REPO = "https://github.com/databricks-edu/Deploying-ML-Models-At-Scale"

import mlflow
from mlflow.utils import mlflow_tags
from mlflow.entities import RunStatus
from mlflow.utils.logging_utils import eprint
import six

from mlflow.tracking.fluent import _get_experiment_id

@click.command()
@click.option("--username")
@click.option("--penalty")
@click.option("--local")
@click.option("--use-conda")
def workflow(username: str, penalty: str, local: bool, use_conda: bool) -> bool:

    load_user_data_params = {
        "filename": "user_profile_data.snappy.parquet",
        "kind" : "user",
        "username": username,
        "local": local
    }

    load_event_data_params = {
        "filename": "health_profile_data.snappy.parquet",
        "kind" : "event",
        "username": username,
        "local": local
    }

    etl_params = {
        "username": "joshuacook",
        "local": True
    }

    experiment_params = {
        "username": "joshuacook",
        "penalty": "l1",
        "max_iter": 10000,
        "local": True
    }

    with mlflow.start_run() as active_run:
        load_user_data_run = mlflow.projects.run(
            GIT_REPO, "load_data",
            parameters=load_user_data_params,
            use_conda=use_conda
        )
        load_event_data_run = mlflow.projects.run(
            GIT_REPO, "load_data",
            parameters=load_event_data_params,
            use_conda=use_conda
        )
        etl_run = mlflow.projects.run(
            GIT_REPO, "etl",
            parameters=etl_params,
            use_conda=use_conda
        )
        experiment_run = mlflow.projects.run(
            GIT_REPO, "experiment",
            parameters=experiment_params,
            use_conda=use_conda
        )

if __name__ == "__main__":
    workflow()
