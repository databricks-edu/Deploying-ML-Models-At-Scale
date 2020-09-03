from pyspark.sql import SparkSession
from urllib.request import urlretrieve
import click
import os

from pyspark.dbutils import DBUtils

spark = SparkSession.builder.master("local[8]").getOrCreate()
dbutils = DBUtils(spark.sparkContext)

def retrieve_data(file: str, landing_path: str) -> bool:
    """Download file from remote location to driver. Move from driver to DBFS."""

    base_url = "https://files.training.databricks.com/static/data/health-tracker/"
    url = base_url + file
    driverPath = "file:/databricks/driver/" + file
    dbfsPath = landing_path + file
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
@click.option("--filename", help="the name of the remote file")
@click.option("--kind", help="event|user")
@click.option("--username", help="username unique to dbacademy on this workspace")
def load_data(file_name: str, kind: str, username: str) -> bool:

    projectPath     = f"dbfs:/dbacademy/{username}/mlmodels/profile/"
    landing_path    = projectPath + "landing/"
    silverDailyPath = projectPath + "daily/"
    dimUserPath     = projectPath + "users/"

    if kind == "event":
        table_path = silverDailyPath
        table_name = "health_profile_data"
    elif kind == "user":
        table_path = dimUserPath
        table_name = "user_profile_data"
    else:
        raise ArgumentError("`path` variable must be one of `event` or `user`.")

    retrieve_data(file_name, landing_path)
    load_delta_table(spark, file_name, landing_path, table_path)

if __name__ == '__main__':
    load_data()
