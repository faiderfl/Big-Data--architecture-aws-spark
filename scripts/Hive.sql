CREATE EXTERNAL TABLE IF NOT EXISTS Alarms (
Device_ID String,						
Worker_ID String,
Worker_Name String,
Event String,
EventTime String,
Latitude String,
Longitude String
) 
ROW FORMAT DELIMITED FIELDS TERMINATED BY ';'
STORED AS TEXTFILE
LOCATION 's3://bls-data/hive/Alarms';


CREATE EXTERNAL TABLE IF NOT EXISTS Events (
Device_ID String,						
Worker_ID String,
Worker_Name String,
Event String,
Time String,
Latitude String,
Longitude String
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ';'
STORED AS TEXTFILE
LOCATION 's3://bls-data/hive/Events';

----------------------
DROP TABLE TEMPTEvents PURGE
CREATE  EXTERNAL TABLE TEMPTEvents(
    Device_ID String,
    Worker_ID String,
    Worker_Name String,
    Event String,
    EventTime String,
    Latitude String,
    Longitude String  
        )
STORED BY 'org.apache.hadoop.hive.dynamodb.DynamoDBStorageHandler'
TBLPROPERTIES ("dynamodb.table.name" = "blsEvents", "dynamodb.column.mapping" = "Device_ID:Device_ID,Worker_ID:Worker_ID,Worker_Name:Worker_Name,Event:Event,EventTime:EventTime,Latitude:Latitude,Longitude:Longitude");

DROP TABLE TEMPTAlarms PURGE
CREATE  EXTERNAL TABLE TEMPTAlarms(
    Device_ID String,
    Worker_ID String,
    Worker_Name String,
    Event String,
    EventTime String,
    Latitude String,
    Longitude String  
        )
STORED BY 'org.apache.hadoop.hive.dynamodb.DynamoDBStorageHandler'
TBLPROPERTIES ("dynamodb.table.name" = "blsAlarms", "dynamodb.column.mapping" = "Device_ID:Device_ID,Worker_ID:Worker_ID,Worker_Name:Worker_Name,Event:Event,EventTime:EventTime,Latitude:Latitude,Longitude:Longitude");
