from pyspark.sql import SparkSession
from pyspark import SparkContext 
from pyspark.sql import SQLContext 



sc = SparkSession.builder.appName("ReadCSV").config("spark.hadoop.fs.s3a.access.key", "").config("spark.hadoop.fs.s3a.secret.key", "").config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem").config("spark.sql.warehouse.dir", "s3://bls-data/hive/").config("spark.sql.catalogImplementation","hive").getOrCreate() 

events= sc.read.options(header='true',sep=";").csv("s3a://bls-data/data/Events.csv")

events.createOrReplaceTempView("events")

alarms= events.filter(events['Event'].isin(['1','2']) == False)
alarms.createOrReplaceTempView("alarms")

#sc.sql("CREATE EXTERNAL TABLE IF NOT EXISTS Events (Device_ID String, Worker_ID String, Worker_Name String, Event String, EventTime String, Latitude String, Longitude String) ROW FORMAT DELIMITED FIELDS TERMINATED BY ';' STORED AS TEXTFILE LOCATION 's3://bls-data/hive/Events'")
#sc.sql("CREATE EXTERNAL TABLE IF NOT EXISTS Alarms (Device_ID String, Worker_ID String, Worker_Name String, Event String, EventTime String, Latitude String, Longitude String) ROW FORMAT DELIMITED FIELDS TERMINATED BY ';' STORED AS TEXTFILE LOCATION 's3://bls-data/hive/Alarms'")

sc.sql("INSERT OVERWRITE TABLE default.events SELECT * FROM events")
sc.sql("INSERT OVERWRITE TABLE default.alarms SELECT * FROM alarms")

sc.sql("INSERT OVERWRITE TABLE TEMPTEvents SELECT * FROM events")
sc.sql("INSERT OVERWRITE TABLE TEMPTAlarms SELECT * FROM alarms")