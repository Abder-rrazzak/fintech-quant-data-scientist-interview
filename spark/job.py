"""Transaction aggregates in Spark when it is installed, otherwise in Pandas.

The Pandas path is the contract for this laboratory. Spark is the same grain
and the same windows, expressed with the DataFrame API when Java and PySpark
are available. A laptop extract does not need a cluster.
"""

from __future__ import annotations

import pandas as pd


def customer_daily_spend(transactions: pd.DataFrame) -> pd.DataFrame:
    """Spend and count by customer and calendar day. The current row is included."""
    frame = transactions.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"])
    frame["day"] = frame["timestamp"].dt.floor("D")
    grouped = (
        frame.groupby(["customer_id", "day"], as_index=False)
        .agg(spend=("amount", "sum"), txn_count=("transaction_id", "count"))
        .sort_values(["customer_id", "day"], kind="mergesort")
    )
    return grouped


def try_spark_daily_spend(transactions: pd.DataFrame):
    """Run the same aggregate in Spark. Returns None when Spark cannot start."""
    try:
        from pyspark.sql import SparkSession
        from pyspark.sql import functions as F
    except ImportError:
        return None
    spark = SparkSession.builder.master("local[1]").appName("fintech-lab").getOrCreate()
    try:
        sdf = spark.createDataFrame(transactions[["customer_id", "transaction_id", "timestamp", "amount"]])
        sdf = sdf.withColumn("day", F.to_date("timestamp"))
        out = (
            sdf.groupBy("customer_id", "day")
            .agg(F.sum("amount").alias("spend"), F.count("transaction_id").alias("txn_count"))
            .orderBy("customer_id", "day")
        )
        return out.toPandas()
    finally:
        spark.stop()
