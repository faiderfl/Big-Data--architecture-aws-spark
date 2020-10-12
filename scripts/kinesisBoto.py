
import random
import time
from datetime import datetime
import boto3 
import string
import json

region = 'us-east-1'
client = boto3.client('kinesis',region_name=region)
stream_name='blsEventsStream'


messages = [
    {'Device_ID': '5', 'Event': '1','EventTime':'20200908 09:36:00', 'Latitude':'51,037086','Longitude':'-114,053629','Worker_ID':'456','Worker_Name':'Paula'},
    {'Device_ID': '6', 'Event': '4','EventTime':'20200908 09:36:00', 'Latitude':'51,037086','Longitude':'-114,053629','Worker_ID':'456','Worker_Name':'Andrea'},
    {'Device_ID': '7', 'Event': '5','EventTime':'20200908 10:36:00', 'Latitude':'51,037086','Longitude':'-114,063629','Worker_ID':'456','Worker_Name':'Bryan'},
    {'Device_ID': '8', 'Event': '5','EventTime':'20200908 10:36:00', 'Latitude':'51,037086','Longitude':'-114,063629','Worker_ID':'456','Worker_Name':'Andres'},
    {'Device_ID': '8', 'Event': '5','EventTime':'20200908 10:36:00', 'Latitude':'51,037086','Longitude':'-114,063629','Worker_ID':'456','Worker_Name':'Andres'},
]
for message in messages:
    client.put_record(
        StreamName=stream_name,
        Data=json.dumps(message),
        PartitionKey='part_key')

print("Ok")