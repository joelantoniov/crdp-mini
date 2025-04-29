from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, substring, when
from pyspark.sql.types import StructType, StructField, StringType, FloatType

# Initialize Spark session with Cassandra connector configuration
spark = SparkSession.builder \
    .appName("CRDPStreaming") \
    .config("spark.cassandra.connection.host", "cassandra") \
    .config("spark.cassandra.connection.port", "9042") \
    .getOrCreate()

# Define schema for the incoming Kafka data
schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("temperature", FloatType(), True),
    StructField("humidity", FloatType(), True),
    StructField("pressure", FloatType(), True),
    StructField("region", StringType(), True)
])

# Read streaming data from Kafka and include the topic name
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka-broker:9092") \
    .option("subscribe", "crdp-sensors-jakarta,crdp-sensors-nyc,crdp-sensors-london,crdp-sensors-sydney,crdp-sensors-saopaulo") \
    .load()

# Extract the Kafka message value and topic
df = df.selectExpr("CAST(value AS STRING)", "topic") \
    .select(from_json(col("value"), schema).alias("data"), col("topic")) \
    .select("data.*", "topic")

# Ensure all required columns are present
# If 'region' is null, derive it from the topic name
df = df.withColumn("region", 
                   col("region").cast("string")) \
       .withColumn("region", 
                   when(col("region").isNull(), substring(col("topic"), 13, 100)) \
                   .otherwise(col("region")))  # Fixed to start at 13

# Derive 'hour' from 'timestamp' (format: "YYYY-MM-DDTHH")
df = df.withColumn("hour", substring(col("timestamp"), 1, 13))

# Ensure 'timestamp' exists and is not null
df = df.filter(col("timestamp").isNotNull())

# Perform processing (e.g., calculate flood risk)
df = df.withColumn("flood_risk", col("humidity") * 0.01)

# Prepare the DataFrame for Cassandra
df = df.select(
    col("region"),
    col("hour"),
    col("timestamp"),
    col("temperature").alias("avg_temperature"),
    col("humidity").alias("avg_humidity"),
    col("pressure").alias("avg_pressure"),
    col("flood_risk")
)

# Write the processed data to Cassandra with a trigger
query = df \
    .writeStream \
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", "crdp") \
    .option("table", "sensor_metrics_v1") \
    .option("checkpointLocation", "/tmp/checkpoints") \
    .trigger(processingTime="10 seconds") \
    .start()

# Await termination
query.awaitTermination()
