from pyspark.sql import SparkSession
from pyspark.sql.functions import mean, col
import click

def configure_spark(username: str) -> SparkSession:
    spark = SparkSession.builder.getOrCreate()
    spark.sql(f"CREATE DATABASE IF NOT EXISTS dbacademy_{username}")
    spark.sql(f"USE dbacademy_{username}")
    return spark

@click.command(help="transform loaded data to prepare for machine learning")
@click.option("--username", help="username unique to dbacademy on this workspace")
def etl(username: str):
    spark = configure_spark(username)
    projectPath = f"/dbacademy/{username}/mlmodels/profile/"
    goldPath = projectPath + "gold/"

    user_profile_df = spark.read.table("user_profile_data")
    health_profile_df = spark.read.table("health_profile_data")

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
    health_tracker_augmented_df.write.format("delta").save(ht_augmented_path)

    spark.sql(f"""
    DROP TABLE IF EXISTS ht_augmented
    """)

    spark.sql(f"""
    CREATE TABLE ht_augmented
    USING DELTA
    LOCATION "{ht_augmented_path}"
    """)


if __name__ == '__main__':
    etl()
