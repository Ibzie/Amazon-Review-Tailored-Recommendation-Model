from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, BooleanType, IntegerType
from pyspark.sql.functions import col, lower, regexp_replace
import json

# create a Spark session
spark = SparkSession.builder \
    .appName("Write data to MongoDB") \
    .config("spark.mongodb.output.uri", "mongodb://localhost:27017/") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27017/")\
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1")\
    .getOrCreate()

# create a Spark context
sc = spark.sparkContext

# read data from input file
input_file = "All_Amazon_Review.json.gz"
raw_data = sc.textFile(input_file)

# parse JSON data and filter out any empty records
parsed_data = raw_data.map(lambda line: json.loads(line)).filter(lambda x: x is not None)


# define the schema for the DataFrame
schema = StructType([
    StructField("overall", DoubleType(), False),
    StructField("verified", BooleanType(), False),
    StructField("asin", StringType(), False),
    StructField("summary", StringType(), True),
    StructField("unixReviewTime", IntegerType(), False)
])

# create a DataFrame from the parsed data and schema
df = spark.createDataFrame(parsed_data, schema=schema)

# clean the data
df = df.withColumn("summary", lower(col("summary")))  # Convert Review Text to lowercase
df = df.withColumn("summary", regexp_replace(col("summary"), "[^a-zA-Z0-9\\s]", ""))  # Remove punctuation
df = df.dropna()
# df = df.repartition(8)

# write the DataFrame to MongoDB using the Spark connector
df.write.format("com.mongodb.spark.sql.DefaultSource")\
        .option("uri", "mongodb://localhost:27017/amazon.reviews")\
        .mode("overwrite")\
        .save()

# stop the Spark context
sc.stop()
