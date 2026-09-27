from pyspark.sql import functions as F

orders = spark.read.format("delta").load("Tables/silver/orders")
customers = spark.read.format("delta").load("Tables/silver/customers")

gold = (
    orders.filter(F.col("status") == "COMPLETED")
    .join(customers.select("customer_id", "country_code"), "customer_id", "left")
    .withColumn("order_date", F.to_date("order_timestamp"))
    .groupBy("order_date", "country_code")
    .agg(
        F.sum("net_revenue").alias("net_revenue"),
        F.countDistinct("order_id").alias("orders"),
        F.countDistinct("customer_id").alias("active_customers"),
    )
)
gold.write.format("delta").mode("overwrite").save("Tables/gold/daily_sales")
