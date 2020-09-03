from pyspark.sql import SparkSession
from pyspark.sql.functions import mean, col
import click

spark = SparkSession.builder.master("local[8]").getOrCreate()
dbutils = DBUtils(spark.sparkContext)

@click.command(help="transform loaded data to prepare for machine learning")
@click.option("--username", help="username unique to dbacademy on this workspace")
def etl(username: str):

    projectPath     = f"/dbacademy/{username}/mlmodels/profile/"
    silverDailyPath = projectPath + "daily/"
    dimUserPath     = projectPath + "users/"
    goldPath = projectPath + "gold/"

    health_profile_df = spark.read.format("delta").load(silverDailyPath)
    user_profile_df = spark.read.format("delta").load(dimUserPath)

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
    dbutils.fs.rm(ht_augmented_path, recurse=True)
    (
      health_tracker_augmented_df.write
      .mode("overwrite")
      .format("delta")
      .save(ht_augmented_path)
    )

if __name__ == '__main__':
    etl()
