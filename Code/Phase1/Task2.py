from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StructField, FloatType, IntegerType, BooleanType
import matplotlib.pyplot as plt

# Create a SparkSession
spark = SparkSession.builder.appName("AmazonReviewAnalysis").getOrCreate()

# Define the schema of the dataset
schema = StructType([
    StructField("asin", StringType()),
    StructField("overall", FloatType()),
    StructField("reviewText", StringType()),
    StructField("reviewTime", StringType()),
    StructField("reviewerID", StringType()),
    StructField("reviewerName", StringType()),
    StructField("summary", StringType()),
    StructField("unixReviewTime", IntegerType()),
    StructField("verified", BooleanType())
])

# Load the dataset from a JSON file into a DataFrame
dfs = spark.read.json("All_Amazon_Review.json", schema=schema, samplingRatio=0.001)

# Transform the DataFrame to include only the required columns
df_sample = dfs.select("asin", "overall", "reviewText", "reviewTime", "reviewerID", "reviewerName", "summary", "unixReviewTime", "verified")

# Create a Pandas DataFrame for the verified column
verified_pd = df_sample.groupBy("verified").count().toPandas()

# Plot a bar chart of the verified/unverified column
plt.bar(verified_pd["verified"], verified_pd["count"])
plt.xlabel("Verified")
plt.ylabel("Count")
plt.title("Bar chart of verified column")
plt.show()

reviewTimes_pd = df_sample.groupBy("reviewTime").count().toPandas()

plt.scatter(reviewTimes_pd["reviewTime"], reviewTimes_pd["count"], color="red")
plt.xlabel("Review Date")
plt.ylabel("Count")
plt.title("Scatter graph of Review Time")
plt.show()

ratings_pd = df_sample.groupBy("overall").count().toPandas()

plt.bar(ratings_pd["overall"], ratings_pd["count"], color="green")
plt.xlabel("Overall Ratings")
plt.ylabel("Count")
plt.title("Bar graph of Overall Ratings")
plt.show()

# Stop the Spark session
spark.stop()