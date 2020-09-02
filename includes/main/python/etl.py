from pyspark.sql import SparkSession
from pyspark.sql.functions import mean, col
import click

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

@click.command(help="transform loaded data to prepare for machine learning")
@click.option("--username", help="username unique to dbacademy on this workspace")
@click.option("--local", help="True|False")
def etl(username: str, local: bool):

    spark = configure_spark(username, local)
    projectPath     = f"/dbacademy/{username}/mlmodels/profile/"
    if local:
        projectPath = "data/"
    silverDailyPath = projectPath + "daily/"
    dimUserPath     = projectPath + "users/"
    goldPath = projectPath + "gold/"

    health_profile_df = spark.read.format("delta").load(silverDailyPath)
    user_profile_df = spark.read.format("delta").load(dimUserPath)
    if local:
        health_profile_df = health_profile_df.sample(0.03)

    health_tracker_agg_df = (
        health_profile_df.groupBy("_id")
        .agg(
            mean("BMI").alias("mean_BMI"),
            mean("active_heartrate").alias("mean_active_heartrate"),
            mean("resting_heartrate").alias("mean_resting_heartrate"),
            mean("VO2_max").alias("mean_VO2_max"),
            mean("workout_minutes").alias("mean_workout_minutes")
        )
    )

    health_tracker_augmented_df = (
      health_tracker_agg_df
      .join(user_profile_df, "_id")
    )

    health_tracker_augmented_df = (
      health_tracker_augmented_df
      .select(
        "mean_BMI",
        "mean_active_heartrate",
        "mean_resting_heartrate",
        "mean_VO2_max",
        "lifestyle"
      )
    )

    ht_augmented_path = goldPath + "ht_augmented"
    health_tracker_augmented_df.write.mode("overwrite").format("delta").save(ht_augmented_path)

if __name__ == '__main__':
    etl()
