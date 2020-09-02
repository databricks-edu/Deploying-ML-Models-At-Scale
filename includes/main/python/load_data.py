from pyspark.sql import SparkSession
from urllib.request import urlretrieve
import click
import os

def configure_spark(username: str, local: bool) -> SparkSession:
    if local:
        import os
        print("Configuring Spark for local processing.")
        pyspark_submit_args  = '--packages "io.delta:delta-core_2.12:0.7.0" '
        pyspark_submit_args += 'pyspark-shell'
        os.environ['PYSPARK_SUBMIT_ARGS'] = pyspark_submit_args

    spark = SparkSession.builder.master("local[8]").getOrCreate()
    spark.sql(f"CREATE DATABASE IF NOT EXISTS dbacademy_{username}")
    spark.sql(f"USE dbacademy_{username}")
    return spark

def retrieve_data(file: str, landing_path: str, local: bool) -> bool:
    """Download file from remote location to driver. Move from driver to DBFS."""

    base_url = "https://files.training.databricks.com/static/data/health-tracker/"
    url = base_url + file
    driverPath = "file:/databricks/driver/" + file
    dbfsPath = landing_path + file
    if local:
        urlretrieve(url, landing_path + file)
    else:
        urlretrieve(url, file)
        dbutils.fs.mv(driverPath, dbfsPath)
    return True

def load_delta_table(spark: SparkSession, file_name: str,
                     landing_path: str, delta_table_path: str) -> bool:
    "Load a parquet file as a Delta table."
    parquet_df = spark.read.format("parquet").load(landing_path + file_name)
    parquet_df.write.format("delta").save(delta_table_path)
    return True

@click.command(help="process a remote file to a users dbacademy directory")
@click.option("--file-name", help="the name of the remote file")
@click.option("--kind", help="event|user")
@click.option("--username", help="username unique to dbacademy on this workspace")
@click.option("--local", help="True|False")
def load_data(file_name: str, kind: str, username: str, local: bool) -> bool:

    spark = configure_spark(username, local)

    projectPath     = f"/dbacademy/{username}/mlmodels/profile/"
    if local:
        projectPath = "data/"
    landing_path    = projectPath + "landing/"
    silverDailyPath = projectPath + "daily/"
    dimUserPath     = projectPath + "users/"
    if local:
        os.makedirs(landing_path, exist_ok=True)
        os.makedirs(silverDailyPath, exist_ok=True)
        os.makedirs(dimUserPath, exist_ok=True)

    if kind == "event":
        table_path = silverDailyPath
        table_name = "health_profile_data"
    elif kind == "user":
        table_path = dimUserPath
        table_name = "user_profile_data"
    else:
        raise ArgumentError("`path` variable must be one of `event` or `user`.")

    retrieve_data(file_name, landing_path, local)
    load_delta_table(spark, file_name, landing_path, table_path)

if __name__ == '__main__':
    load_data()
