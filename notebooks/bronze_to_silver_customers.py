from pyspark.sql import functions as F

bronze = spark.read.format("delta").load("Tables/bronze/customers")

silver = (
    bronze
    .filter(F.col("customer_id").isNotNull())
    .withColumn("email", F.lower(F.trim("email")))
    .withColumn("customer_name", F.trim("customer_name"))
    .withColumn("country_code", F.upper(F.trim("country_code")))
    .withColumn("dq_email_valid", F.col("email").rlike(r"^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$"))
    .dropDuplicates(["customer_id"])
)

(silver.write.format("delta")
 .mode("overwrite")
 .option("overwriteSchema", "true")
 .save("Tables/silver/customers"))
