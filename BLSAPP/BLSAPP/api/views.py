from django.shortcuts import render
from django.template import RequestContext
from utils import Utils
from logger import logger
# HTTP Error 400


class config:
    conf = Utils.loadConfig("config.json")
    log = logger(pathlog=conf["rutaLog"],
                 logName=conf["logName"])


def bad_request(request, exception=None, template_name='400.html'):
    response = render(request, '400.html')
    response.status_code = 400
    response.message = "server error"

    config.log.Error("Error: " + 'host: ' + request.environ['REMOTE_ADDR'] + ' message: ' + response.message +
                     ' code: ' + str(response.status_code))
    return response


def server_error(request, exception=None, template_name='500.html'):
    response = render(request, '500.html')
    response.status_code = 500
    response.message= "server error"

    config.log.Error("Error: " + 'host: ' + request.environ['REMOTE_ADDR'] + ' message: ' + response.message +
                     ' code: ' + str(response.status_code))
    return response


def permission_denied(request, exception=None, template_name='403.html'):
    response = render(request, '403.html')
    response.status_code = 403
    response.message = "permission_denied"

    config.log.Error("Error: " + 'host: ' + request.environ['REMOTE_ADDR'] + ' message: ' + response.message +
                     ' code: ' + str(response.status_code))
    return response


def page_not_found(request, exception=None, template_name='404.html'):
    response = render(request, '404.html')
    response.status_code = 404
    response.message = "page_not_found"

    config.log.Error("Error: " + 'host: ' + request.environ['REMOTE_ADDR'] + ' message: ' + response.message +
                     ' code: ' + str(response.status_code))
    return response

