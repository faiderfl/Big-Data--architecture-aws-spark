# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 08:50:22 2017

Módulo que permite hacer loggeo de información en una ruta específica

@author: rlarios
"""

import time
import os
import io

from datetime import datetime
from pytz import timezone

class logger():
    def __init__(self , pathlog = './log/log' , logName = "process.log" , timeZone = timezone("America/Bogota")):
        """Inicializa el logger
        
        Argumentos:
        pathlog -- Ruta donde se escribirá el log
        logName -- Nombre del archivo log (el archivo tendrá un sufijo con la fecha de creación)        
        """
        self.path = pathlog
        self.tz = timeZone
        self.filename = self.path + self.curSimpleDate() + "_" + logName
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            print("Directory ", self.path,  " Created ")
        else:
            print("Directory ", self.path,  " already exists")

        self.flog = io.open(self.filename, 'a' , encoding="utf-8")
        

        self.typeMsg = {
                "I" : "[INFO ] ",
                "E" : "[ERROR] ",
                "D" : "[DEBUG] "                
                }
        
        
    def curDate(self):
        """Devuelve la decha en formato YYYYMMDDHHMMSS."""
        return  datetime.now(self.tz).strftime('%Y%m%d%H%M%S')

    def curSimpleDate(self):
        """Devuelve la decha en formato YYYYMMDD"""
        return datetime.now(self.tz).strftime('%Y%m%d') 

    def curTime(self):
        """Devuelve la decha en formato YYYY-MM-DD HH:MM:SS."""
        return  '[' + datetime.now(self.tz).strftime('%Y-%m-%d %H:%M:%S') + '] '
    
    def Info(self , message):
        """Escribe un mensaje de info en el log"""
        self.__writeLog(message , "I")
        
    def Error(self , message):
        """Escribe un mensaje de error en el log"""
        self.__writeLog(message , "E")
        
    def Debug(self , message):
        """Escribe un mensaje de Debug en el log"""
        self.__writeLog(message , "D")
    
    def __writeLog(self , message , typeM):
        """Función que escribe el mensaje con el tipo especificado"""
        msx = self.curTime() + self.typeMsg[typeM] + message.strip()
        print( msx ) 
        self.flog.writelines( msx + "\n")
        self.flog.flush()
        
    def close(self):
        """ECierra el archivo de log"""
        self.flog.flush()
        self.flog.close()

