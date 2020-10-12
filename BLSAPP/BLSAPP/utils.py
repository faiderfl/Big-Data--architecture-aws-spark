import json
import traceback
import sys

class Utils:
    def loadConfig( conf_path ):
        if conf_path is None or conf_path == '':
            raise('Archivo de Configuración no puede ser Nulo')
        
        with open( conf_path ) as f_in :
            json_str = f_in.read()
            return json.loads( json_str )



