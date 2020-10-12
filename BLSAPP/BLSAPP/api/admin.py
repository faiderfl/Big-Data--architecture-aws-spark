
from django.http import HttpResponse

from pytz import timezone
from datetime import datetime

from utils import Utils
from logger import logger

timeZone = timezone("America/Bogota")

class config:
    conf = Utils.loadConfig("config.json")
    log = logger(pathlog= conf["rutaLog"],
                 logName= conf["logName"])

def getTime():
	return datetime.now(timeZone).strftime("%Y-%m-%d %H:%M:%S")

def getAdmin(request):
	config.log.Info("WARNING: Request for Admin Console")
	return HttpResponse("Consola de Admin no disponible.")


def getEmpty(request):
	msg = "BLSAPP " + getTime()
	config.log.Info("Endpoint request: " + msg)
	return HttpResponse(msg)