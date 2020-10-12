import graphene
from graphene_django.types import DjangoObjectType

from api.models import Blsevents , get_blsevents , BlseventsDataInput
from api.models import Blsalarms , get_blsalarms , BlsalarmsDataInput


from graphene_pynamodb import PynamoConnectionField, PynamoObjectType
from itertools import islice
from api.errors import CustomFatalError
import operator as op
from datetime import datetime
from pytz import timezone

def getCrud():
    tzx = timezone("America/Bogota")
    modificacioncrudint = int(datetime.now(tzx).strftime("%Y%m%d%H%M%S"))
    return modificacioncrudint


class BlseventsType(PynamoObjectType):
    class Meta:
        model = Blsevents
     
class BlseventsType_all(graphene.ObjectType):
    total_count = graphene.Int(required=True)
    blsevents = graphene.List(BlseventsType)



class BlsalarmsType(PynamoObjectType):
    class Meta:
        model = Blsalarms
     
class BlsalarmsType_all(graphene.ObjectType):
    total_count = graphene.Int(required=True)
    blsalarms = graphene.List(BlsalarmsType)

        

class Query(graphene.ObjectType):

    blsEvents_all = graphene.Field(BlseventsType_all, device_id=graphene.String() , eventtime=graphene.String())
    blsEvents = graphene.List(BlseventsType, device_id=graphene.String() , eventtime=graphene.String())

    blsAlarms_all = graphene.Field(BlsalarmsType_all, device_id=graphene.String() , eventtime=graphene.String())
    blsAlarms = graphene.List(BlsalarmsType, device_id=graphene.String() , eventtime=graphene.String())


    
    status = graphene.String()
   
    def resolve_status(self, info, **kwargs):
       return "Ok"

    def resolve_blsEvents_all(self, info , device_id , eventtime = None , **kwargs):
        
        complete = BlseventsType_all()

        if device_id is not None:
            result = get_blsevents( device_id , eventtime )
        else:
            result = None

        complete.total_count = len(result)
        complete.blsevents = result

        return complete

    def resolve_blsEvents(self, info, device_id , eventtime = None , **kwargs):
        
        if device_id is not None:
            result = get_blsevents( device_id , eventtime )
        else:
            result= None

        return result

    def resolve_blsAlarms_all(self, info , device_id , eventtime = None , **kwargs):
        
        complete = BlsalarmsType_all()

        if device_id is not None:
            result = get_blsalarms( device_id , eventtime )
        else:
            result = None

        complete.total_count = len(result)
        complete.blsalarms = result

        return complete

    def resolve_blsAlarms(self, info, device_id , eventtime = None , **kwargs):
        
        if device_id is not None:
            result = get_blsalarms( device_id , eventtime )
        else:
            result= None

        return result





class create_Blsevents(graphene.Mutation):
    class Arguments:
        blsEvents_data = BlseventsDataInput()

    blsEvents = graphene.Field(BlseventsType)

    def mutate(self, info, blsEvents_data=None):
        blsEvents = Blsevents(

			device_id=blsEvents_data.device_id,
			worker_id=blsEvents_data.worker_id,
			worker_name=blsEvents_data.worker_name,
			event=blsEvents_data.event,
			eventtime=blsEvents_data.eventtime,
			latitude=blsEvents_data.latitude,
			longitude=blsEvents_data.longitude,
			updated=blsEvents_data.updated,
			activo=blsEvents_data.activo,
			modificacion_crud=getCrud()
            
        )
        blsEvents.save()
        return create_Blsevents(blsEvents=blsEvents)

class delete_Blsevents(graphene.Mutation):
    class Arguments:
        blsEvents_data = BlseventsDataInput()

    status = graphene.Boolean()

    def mutate(self, info, blsEvents_data=None):
        result = get_blsevents( device_id = blsEvents_data.device_id , eventtime = blsEvents_data.eventtime )
        status = False
        for r in result:
            r.activo = 0
            r.modificacion_crud = getCrud()
            r.save()
            status = True

        return delete_Blsevents(status=status)


class create_Blsalarms(graphene.Mutation):
    class Arguments:
        blsAlarms_data = BlsalarmsDataInput()

    blsAlarms = graphene.Field(BlsalarmsType)

    def mutate(self, info, blsAlarms_data=None):
        blsAlarms = Blsalarms(

			device_id=blsAlarms_data.device_id,
			worker_id=blsAlarms_data.worker_id,
			worker_name=blsAlarms_data.worker_name,
			event=blsAlarms_data.event,
			eventtime=blsAlarms_data.eventtime,
			latitude=blsAlarms_data.latitude,
			longitude=blsAlarms_data.longitude,
			updated=blsAlarms_data.updated,
			activo=blsAlarms_data.activo,
			modificacion_crud=getCrud()
            
        )
        blsAlarms.save()
        return create_Blsalarms(blsAlarms=blsAlarms)

class delete_Blsalarms(graphene.Mutation):
    class Arguments:
        blsAlarms_data = BlsalarmsDataInput()

    status = graphene.Boolean()

    def mutate(self, info, blsAlarms_data=None):
        result = get_blsalarms( device_id = blsAlarms_data.device_id , eventtime = blsAlarms_data.eventtime )
        status = False
        for r in result:
            r.activo = 0
            r.modificacion_crud = getCrud()
            r.save()
            status = True

        return delete_Blsalarms(status=status)




class Mutation(graphene.ObjectType):
	createBlsevents = create_Blsevents.Field()
	deleteBlsevents = delete_Blsevents.Field()
	createBlsalarms = create_Blsalarms.Field()
	deleteBlsalarms = delete_Blsalarms.Field()



schema = graphene.Schema(query=Query, mutation=Mutation, types=[ BlseventsType , BlseventsType_all , BlsalarmsType , BlsalarmsType_all ])
