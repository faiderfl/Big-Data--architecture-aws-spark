from api.models import Blsevents , get_blsevents , BlseventsDataInput
from api.models import Blsalarms , get_blsalarms , BlsalarmsDataInput
from django.http import JsonResponse
from django.http import HttpResponse
from datetime import datetime
from pytz import timezone

from utils import Utils
from logger import logger
import json



timeZone = timezone("America/Bogota")

def getLink(status):
    return "https://httpstatuses.com/" + str(status)

class config:
    conf = Utils.loadConfig("config.json")
    log = logger(pathlog= conf["rutaLog"],
                 logName= conf["logName"])


def availableMethods(request):
    return HttpResponse( "Métodos Disponibles: " + "rest/get_blsEvents , rest/set_blsEvents , rest/del_blsEvents , rest/get_blsAlarms , rest/set_blsAlarms , rest/del_blsAlarms" , content_type='application/json; charset=utf-8')


def getCrud():
    modificacioncrudint = int(datetime.now(timeZone).strftime("%Y%m%d%H%M%S"))
    return modificacioncrudint

def getTimeStamp():
    return datetime.now(timeZone).isoformat()

def getMeta(request , size):

    secret = request.META.get('HTTP_X_IBM_CLIENT_SECRET' , None)
    meta = {
              "_messageId": request.META.get('HTTP_MESSAGE_ID' , None)
            , "_requestDateTime": getTimeStamp()
            , "_clientId": request.META.get('HTTP_X_IBM_CLIENT_ID' , None)
            , "_responseSize": size
            #, "_version": "3.0"
            #, "echo": request.GET.get('echo' , "")
            }

    return { k : v for k,v in meta.items() if v is not None }


def getResponse(request , response):
    response["Content-Type"] = "application/vnd.bancolombia.v4+json; charset=utf-8"
    response["API-Version"] = "4.0"
    response["RateLimit-Limit"] = 1000
    response["Message-id"] = request.META.get('HTTP_MESSAGE_ID' , None)
    response["X-Content-Type-Options"] = "nosniff"
    response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response["X-Frame-Options"] = "DENY"
    response["Cache-Control"] = "private, no-cache, no-store, max-age=0, no-transform"
    response["Pragma"] = "no-cache"
    response["Expires"] = 0
    response["Content-Security-Policy"] = "default-src 'self' *.bancolombia.com"

    return response



def getError(e , status):
    cod = "SP" if status == 400 else "SA"
    ret = [
        {
            "code" : cod + str(status) + "BLSAPP",
            "detail": str(e)

        }
    ]
    return ret

def getErrorResponse(status , e , request):
    ret = {
            "meta" : getMeta(request , None) ,
            "status" : status ,
            "title" : "BAD REQUEST" if status == 400 else "INTERNAL SERVER ERROR" ,            
            "errors" : getError(e , status)             
        }

    return ret



def jsonify( pynamObjectList ):
    result = []
    for obj in pynamObjectList:
        try:
            current = {}
            for name , attr in obj.attribute_values.items():
                current[name] = attr
                
            result.append(current)
        except Exception as e:
            msg = "Error en la generación del objeto json de respuesta: " + str(e) + ", Objeto: " + str(obj)
            config.log.Error(msg)
            raise Exception(msg)

    return result


def get_payload(request):
    config.log.Info("request: " + str(request))
    if request.method == 'POST':
        try:
            config.log.Info("body: " + str(request.body))
            body = json.loads( request.body )

            if not body.get("data",None):
                raise Exception("El body del request debe tener el elemento 'data'")

            if type(body["data"]) != list:
                raise Exception("El campo 'data' debe ser de tipo lista")

            return body
        except Exception as e:
            msg = "Error en carga de payload: {0}".format(e)
            config.log.Error( msg )
            raise Exception(msg)
    else:
        config.log.Error("Error en carga de payload: Request debe ser tipo POST")
        raise Exception("Error en carga de payload: Request debe ser tipo POST")  



def rest_get_blsEvents(request):
    try:

        payload = get_payload(request)
        data = payload.get("data" , [])
        res = []
        ret = {}
        for obj in data:
            device_id , eventtime = get_keys_blsEvents(obj)
            result = get_blsevents( device_id , eventtime )
            res = res + jsonify(result)

        ret["meta"] = getMeta( request , len(res))
        ret["data"] = res
        config.log.Info("Response: {0}".format(ret))
        return getResponse(request , JsonResponse( ret , content_type='application/json; charset=utf-8')  )
    
    except Exception as e:
        status = 400
        ret = getErrorResponse(status , e , request)
        return getResponse(request , JsonResponse( ret , content_type='application/json; charset=utf-8' , status = status))



def rest_del_blsEvents(request):
    try:

        payload = get_payload(request)
        data = payload.get("data" , [])
        res = []
        ret = {}
        modcrud = getCrud()
        for obj in data:

            device_id , eventtime = get_keys_blsEvents(obj)
            result = get_blsevents( device_id , eventtime )

            for item in result:
                item.activo = 0
                item.modificacion_crud = modcrud
                item.save()
                res.append("{}".format( (item.device_id , item.eventtime) ))

        ret["meta"] = getMeta(request , len(res))
        ret["data"] = res        
        config.log.Info("Response: {0}".format(ret))        
        return getResponse(request , JsonResponse( ret , content_type='application/json; charset=utf-8'))

    except Exception as e:
        status = 400
        ret = getErrorResponse(status , e , request)
        return getResponse(request , JsonResponse( ret , content_type='application/json; charset=utf-8' , status = status))


def rest_set_blsEvents(request):
    try:

        payload = get_payload(request)
        lista = payload.get("data",[])
        ret = {}
        reslist = []
        modcrud = getCrud()
        for body in lista:
            try:
                newSet = Blsevents()
        
                newSet.device_id = body['device_id']
                newSet.worker_id = body.get('worker_id',None)
                newSet.worker_name = body.get('worker_name',None)
                newSet.event = body.get('event',None)
                newSet.eventtime = body['eventtime']
                newSet.latitude = body.get('latitude',None)
                newSet.longitude = body.get('longitude',None)
                newSet.activo = body.get('activo',1)
                newSet.modificacion_crud = modcrud
        
                newSet.save()
                reslist.append("OK")
            except Exception as e:
                reslist.append("Error: " + str(e))

        ret["meta"] = getMeta(request , len(reslist))
        ret["data"] = reslist
        config.log.Info("Response: {0}".format(ret))  

        return getResponse(request , JsonResponse( ret , content_type='application/json; charset=utf-8') )

    except Exception as e:
        status = 400
        ret = getErrorResponse(status , e , request)
        return getResponse(request , JsonResponse( ret , content_type='application/json; charset=utf-8' , status = status) )




def get_keys_blsEvents( obj ):
    try:
        return obj['device_id'] , obj.get('eventtime', None)
    except Exception as e:
        msg = "Error en el envío de las llaves (HashKey Faltante): " + str(e) + ", Enviado:" + str(obj)
        config.log.Error(msg)
        raise Exception(msg)
    


def rest_get_blsAlarms(request):
    try:

        payload = get_payload(request)
        data = payload.get("data" , [])
        res = []
        ret = {}
        for obj in data:
            device_id , eventtime = get_keys_blsAlarms(obj)
            result = get_blsalarms( device_id , eventtime )
            res = res + jsonify(result)

        ret["meta"] = getMeta( request , len(res))
        ret["data"] = res
        config.log.Info("Response: {0}".format(ret))
        return getResponse(request , JsonResponse( ret , content_type='application/json; charset=utf-8')  )
    
    except Exception as e:
        status = 400
        ret = getErrorResponse(status , e , request)
        return getResponse(request , JsonResponse( ret , content_type='application/json; charset=utf-8' , status = status))



def rest_del_blsAlarms(request):
    try:

        payload = get_payload(request)
        data = payload.get("data" , [])
        res = []
        ret = {}
        modcrud = getCrud()
        for obj in data:

            device_id , eventtime = get_keys_blsAlarms(obj)
            result = get_blsalarms( device_id , eventtime )

            for item in result:
                item.activo = 0
                item.modificacion_crud = modcrud
                item.save()
                res.append("{}".format( (item.device_id , item.eventtime) ))

        ret["meta"] = getMeta(request , len(res))
        ret["data"] = res        
        config.log.Info("Response: {0}".format(ret))        
        return getResponse(request , JsonResponse( ret , content_type='application/json; charset=utf-8'))

    except Exception as e:
        status = 400
        ret = getErrorResponse(status , e , request)
        return getResponse(request , JsonResponse( ret , content_type='application/json; charset=utf-8' , status = status))


def rest_set_blsAlarms(request):
    try:

        payload = get_payload(request)
        lista = payload.get("data",[])
        ret = {}
        reslist = []
        modcrud = getCrud()
        for body in lista:
            try:
                newSet = Blsalarms()
        
                newSet.device_id = body['device_id']
                newSet.worker_id = body.get('worker_id',None)
                newSet.worker_name = body.get('worker_name',None)
                newSet.event = body.get('event',None)
                newSet.eventtime = body['eventtime']
                newSet.latitude = body.get('latitude',None)
                newSet.longitude = body.get('longitude',None)
                newSet.activo = body.get('activo',1)
                newSet.modificacion_crud = modcrud
        
                newSet.save()
                reslist.append("OK")
            except Exception as e:
                reslist.append("Error: " + str(e))

        ret["meta"] = getMeta(request , len(reslist))
        ret["data"] = reslist
        config.log.Info("Response: {0}".format(ret))  

        return getResponse(request , JsonResponse( ret , content_type='application/json; charset=utf-8') )

    except Exception as e:
        status = 400
        ret = getErrorResponse(status , e , request)
        return getResponse(request , JsonResponse( ret , content_type='application/json; charset=utf-8' , status = status) )




def get_keys_blsAlarms( obj ):
    try:
        return obj['device_id'] , obj.get('eventtime', None)
    except Exception as e:
        msg = "Error en el envío de las llaves (HashKey Faltante): " + str(e) + ", Enviado:" + str(obj)
        config.log.Error(msg)
        raise Exception(msg)
    




