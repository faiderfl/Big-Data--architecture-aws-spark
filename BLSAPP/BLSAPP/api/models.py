import graphene
from datetime import datetime
from django.db import models
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, MapAttribute, ListAttribute, BooleanAttribute, NumberSetAttribute , BinaryAttribute , BinarySetAttribute , JSONAttribute
)
from utils import Utils
from logger import logger
from graphene_pynamodb.relationships import OneToOne, OneToMany
import json
from django.conf import settings
from operator import itemgetter


class config:
    conf = Utils.loadConfig("config.json")
    log = logger(pathlog= conf["rutaLog"],
                 logName= conf["logName"])

class Blsevents(Model):
    class Meta:
        if settings.DEBUG:
            aws_access_key_id = config.conf['aws_access_key_id']
            aws_secret_access_key = config.conf['aws_secret_access_key']

        table_name = config.conf['blsEvents_table'] 
        # Specifies the region
        region = config.conf['region'] 
        # Optional: Specify the hostname only if it needs to be changed from the default AWS setting
        host = config.conf['host'] 
        # Specifies the write capacity
        write_capacity_units = config.conf['write_capacity_units'] 
        # Specifies the read capacity
        read_capacity_units = config.conf['read_capacity_units'] 


    device_id = UnicodeAttribute(hash_key=True,attr_name="Device_ID")
    worker_id = UnicodeAttribute(null=True, attr_name="Worker_ID")
    worker_name = UnicodeAttribute(null=True, attr_name="Worker_Name")
    event = UnicodeAttribute(null=True, attr_name="Event")
    eventtime = UnicodeAttribute(range_key=True,attr_name="EventTime")
    latitude = UnicodeAttribute(null=True, attr_name="Latitude")
    longitude = UnicodeAttribute(null=True, attr_name="Longitude")

def get_blsevents( device_id , eventtime ):

        if config.conf["tracklogs"]:
            config.log.Info("Consulta get_blsevents con parametros: device_id={}".format(device_id))

        if eventtime is not None:
            result = Blsevents.query(hash_key = device_id , range_key_condition = Blsevents.eventtime == eventtime)
        else:
            result = Blsevents.query( hash_key = device_id )
        
        return list(result)


class BlseventsDataInput(graphene.InputObjectType):
    
    device_id = graphene.String()
    worker_id = graphene.String()
    worker_name = graphene.String()
    event = graphene.String()
    eventtime = graphene.String()
    latitude = graphene.String()
    longitude = graphene.String()
    updated = graphene.Int()
    activo = graphene.Int()
    modificacion_crud = graphene.Int()    

class Blsalarms(Model):
    class Meta:
        if settings.DEBUG:
            aws_access_key_id = config.conf['aws_access_key_id']
            aws_secret_access_key = config.conf['aws_secret_access_key']

        table_name = config.conf['blsAlarms_table'] 
        # Specifies the region
        region = config.conf['region'] 
        # Optional: Specify the hostname only if it needs to be changed from the default AWS setting
        host = config.conf['host'] 
        # Specifies the write capacity
        write_capacity_units = config.conf['write_capacity_units'] 
        # Specifies the read capacity
        read_capacity_units = config.conf['read_capacity_units'] 


    device_id = UnicodeAttribute(hash_key=True,attr_name="Device_ID")
    worker_id = UnicodeAttribute(null=True, attr_name="Worker_ID")
    worker_name = UnicodeAttribute(null=True, attr_name="Worker_Name")
    event = UnicodeAttribute(null=True, attr_name="Event")
    eventtime = UnicodeAttribute(range_key=True,attr_name="EventTime")
    latitude = UnicodeAttribute(null=True, attr_name="Latitude")
    longitude = UnicodeAttribute(null=True, attr_name="Longitude")
  
def get_blsalarms( device_id , eventtime ):

        if config.conf["tracklogs"]:
            config.log.Info("Consulta get_blsalarms con parametros: device_id={}".format(device_id))

        if eventtime is not None:
            result = Blsalarms.query(hash_key = device_id , range_key_condition = Blsalarms.eventtime == eventtime)
        else:
            result = Blsalarms.query( hash_key = device_id )
        
        return list(result)


class BlsalarmsDataInput(graphene.InputObjectType):
    
    device_id = graphene.String()
    worker_id = graphene.String()
    worker_name = graphene.String()
    event = graphene.String()
    eventtime = graphene.String()
    latitude = graphene.String()
    longitude = graphene.String()
    updated = graphene.Int()
    activo = graphene.Int()
    modificacion_crud = graphene.Int()



    

