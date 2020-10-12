import sys
from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kinesis import KinesisUtils, InitialPositionInStream
import os
import json
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import boto3
#os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages=com.qubole.spark/spark-sql-kinesis_2.11/1.1.3-spark_2.4 pyspark-shell'
#os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars D:\BlacklineSafety\jars\jar_file\spark-sql-kinesis_2.11-1.1.4_spark-2.4.jar pyspark-shell'

table_name = "blsEvents"


def get_dynamodb():


  access_key = ""
  secret_key = ""
  region = "us-east-1"
  return boto3.resource('dynamodb',
                 aws_access_key_id=access_key,
                 aws_secret_access_key=secret_key,
                 region_name=region)

def createTableIfNotExists():
    '''
    Create a DynamoDB table if it does not exist.
    This must be run on the Spark driver, and not inside foreach.
    '''
    dynamodb = get_dynamodb()

    existing_tables = dynamodb.meta.client.list_tables()['TableNames']
    if table_name not in existing_tables:
      print("Creating table %s" % table_name)
      table = dynamodb.create_table(
          TableName=table_name,
          KeySchema=[ { 'AttributeName': 'Device_ID', 'KeyType': 'HASH' } ],
          AttributeDefinitions=[ { 'AttributeName': 'Device_ID', 'AttributeType': 'S' } ],
          ProvisionedThroughput = { 'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5 }
      )

      print("Waiting for table to be ready")
      table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

def sendToDynamoDB_simple(row):
  '''
  Function to send a row to DynamoDB.
  When used with `foreach`, this method is going to be called in the executor
  with the generated output rows.
  '''
  # Create client object in the executor,
  # do not use client objects created in the driver
  dynamodb = get_dynamodb()
  print("Send")
  item= { 'Device_ID': str(row['Device_ID']), 'Event': row['Event'],'EventTime': row['EventTime'],'Latitude': row['Latitude'],'Longitude': row['Longitude'],'Worker_ID': row['Worker_ID'],'Worker_Name': row['Worker_Name'] }
  dynamodb.Table(table_name).put_item(
      Item = item
      )
  print("Item sent:" + json.dumps(item))  

class  SendToDynamoDB_ForeachWriter:
  '''
  Class to send a set of rows to DynamoDB.
  When used with `foreach`, copies of this class is going to be used to writes
  multiple rows in the executor. See the python docs for `DataStreamWriter.foreach`
  for more details.
  '''
  def open(self,partition_id, epoch_id):
    # This is called first when preparing to send multiple rows.
    # Put all the initialization code inside open() so that a fresh
    # copy of this class is initialized in the executor where open()
    # will be called.
    self.dynamodb = get_dynamodb()
    return True

  def process(self, row):
    # This is called for each row after open() has been called.
    # This implementation sends one row at a time.
    # A more efficient implementation can be to send batches of rows at a time.
    self.dynamodb.Table(table_name).put_item(
        Item = { 'Device_ID': str(row['Device_ID']), 'Event': row['Event'],'EventTime': row['EventTime'],'Latitude': row['Latitude'],'Longitude': row['Longitude'],'Worker_ID': row['Worker_ID'],'Worker_Name': row['Worker_Name'] })

  def close(self, err):
    # This is called after all the rows have been processed.
    if err:
      raise err

 
createTableIfNotExists()
sc = SparkContext(appName="PythonStreamingKinesis")

ssc = StreamingContext(sc, 1)
appName='EventStreaming'
streamName='blsEventsStream'
endpointUrl='https://kinesis.us-east-1.amazonaws.com' 
regionName = 'us-east-1'

spark = SparkSession.builder.appName("PythonStreamingKinesis").getOrCreate()
#lines = KinesisUtils.createStream(ssc=ssc, kinesisAppName = appName, streamName=streamName, endpointUrl=endpointUrl, regionName=regionName,initialPositionInStream= InitialPositionInStream.TRIM_HORIZON, checkpointInterval = 2)

kinesis = spark.readStream \
        .format('kinesis') \
        .option('streamName', streamName) \
        .option('endpointUrl', endpointUrl)\
        .option('region', regionName) \
        .option('awsAccessKeyId', '')\
        .option('awsSecretKey', '') \
        .option('startingposition', 'LATEST')\
        .load()\

schema = StructType([
            StructField("Device_ID", StringType()),
            StructField("Event", StringType()),
            StructField("EventTime", StringType()),
            StructField("Latitude", StringType()),
            StructField("Longitude", StringType()),
            StructField("Worker_ID", StringType()),
            StructField("Worker_Name", StringType())
            ])

query= kinesis\
    .selectExpr('CAST(data AS STRING)')\
    .select(from_json('data', schema).alias('data'))\
    .select('data.*')\
    .writeStream\
    .foreach(sendToDynamoDB_simple)\
    .outputMode('update')\
    #.format('console')\
    .start()

query.awaitTermination()

