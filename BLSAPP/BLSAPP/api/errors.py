# create a custom view and override the format_error static method
from graphene_django.views import GraphQLView, HttpError
#from path/to/cutom/error_class import CustomFatalError
from graphql.error.located_error import GraphQLLocatedError
from graphql.error.syntax_error import GraphQLSyntaxError
from graphql.error.format_error import GraphQLError
from pynamodb.exceptions import QueryError
from utils import Utils
from logger import logger
from django.conf import settings


class config:
    conf = Utils.loadConfig("config.json")
    log = logger(pathlog=conf["rutaLog"],
                 logName=conf["logName"])


class CustomFatalError(Exception):
    def __init__(self, message, cause, code=None, params=None):
       """
           Instantiate the custom error class using your
           custom field(s)
       """
       super().__init__(message)
       self.message = str(message)
       self.cause = cause
       self.code = code
       self.params = params


class CustomGraphQLView(GraphQLView):

    """
        This Custom View will override the static method for
        formatting errors
    """
    config.log.Info("Inicio API")

    @staticmethod
    def format_error(error):
        """
            This method is responsible for customising the 
            error message
            sent back to the user.
        """
        try:
            if isinstance(error, HttpError) or isinstance(error, QueryError) or isinstance(error, GraphQLSyntaxError) or isinstance(error, GraphQLError):
                if hasattr(error, 'message'):
                    config.log.Error(error.message)
                elif hasattr(error, 'msg'): 
                    config.log.Error(error.msg)
                else:
                    config.log.Error(str(error))
                return format_located_error(error)
        except TypeError as error:
            config.log.Error(error.message)
            return GraphQLView.format_error(error)
        else:
            config.log.Error(str(error))
            return GraphQLView.format_error(error)


def format_located_error(error):
    """
        Helper method to help error based on type comparison
    """
    if isinstance(error, HttpError):
     

        config.log.Error('message: ' + error.message +
                         'code: ' + str(error.response.status_code))
        return {
            'error': 'Error de conexión HTTP o no ha enviado una consulta válida',
            'message: ': error.message,
            'code: ': error.response.status_code
        }
    if isinstance(error, GraphQLLocatedError):

        config.log.Error('message: ' + error.message +
                         'code: ' + "1001")
        return {
            'error': 'Ocurrió un error de desarrollador no detectado dentro de la función de resolución / suscripción (por ejemplo, una consulta de base de datos mal escrita)',
            'message': error.message,
            'code': 1001
        }

    if isinstance(error, QueryError):
        config.log.Error('message: ' + error.msg +
                         'code: ' + "1002")
        return {
            'error': 'Error interno en la consulta',
            'message': error.msg,
            'code': 1002
        }

    if isinstance(error, GraphQLSyntaxError):
        config.log.Error('message: ' + error.message +
                         'code: ' + "1003")

        return {
            'error': 'La consulta falla por un error interno de validación (sintaxis, lógica , etc.)',
            'message': error.message,
            'code': 1003
        }
        
    if isinstance(error, CustomFatalError):
                # return custom error if it is an instance
                # of CustomFatalError
                config.log.Error('message: ' + error.message +
                                 'code: ' + "1004")
                return {
                    'error': 'Las variables o el contexto proporcionados por el usuario son incorrectos y la función de resolución / suscripción intencionalmente genera un error (por ejemplo, no se le permite ver al usuario solicitado)',
                    'message': error.message,
                    #'cause': error.original_error.cause,
                    #'code': error.original_error.code
                    'code': 1004
                }
    if isinstance(error, GraphQLError):
        config.log.Error('message: ' + error.message +
                         'code: ' + "1000")
        return {
            'error:': 'La consulta  está mal formada',
            'message': error.message,
            'code': 1000
        }

    config.log.Error(error)
    return GraphQLView.format_error(error)
