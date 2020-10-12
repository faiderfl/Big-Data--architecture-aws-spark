# coding: utf-8
from flask import Flask, render_template, request, url_for
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
#from dynaconf import FlaskDynaconf
import requests
import json
from collections import namedtuple

application = Flask(__name__, template_folder="templates", static_url_path="/static")
#FlaskDynaconf(app)  # will read GOOGLEMAPS_KEY from .secrets.toml


# you can set key as config
# app.config['GOOGLEMAPS_KEY'] = ""

# you can also pass key here
GoogleMaps(
    application,
    key=""
)

# NOTE: this example is using a form to get the apikey

class Event(object):
    def __init__(self, deviceId, event,eventtime,latitude,longitude,workerId,workerName ):
        self.deviceId = deviceId
        self.event = event
        self.eventtime=eventtime
        self.latitude= float(latitude)
        self.longitude= float(longitude)
        self.workerId= workerId
        self.workerName=workerName


def getEvents():
    device_id=request.args.get('Device_Id')
    
    listEvents=[]
    if device_id is not None:

        queryEvents = """query{
        blsEvents(deviceId:"""+"\""+device_id+"\""+"""){
            deviceId,
            event,
            eventtime,
                latitude,
            longitude,
                workerId,
                workerName
        }
        }
        """
        #print (queryEvents)
        url = ''
        r = requests.post(url, json={'query': queryEvents})
        #print(r.status_code)
        #print(r.text)
        Events = json.loads(r.text)
        #print (Events['data']['blsEvents'][0])

        
        for e in Events['data']['blsEvents']:
            listEvents.append(Event(deviceId=e['deviceId'], event=e['event'],eventtime=e['eventtime'],latitude=e['latitude'].replace(',','.'),longitude=e['longitude'].replace(',','.'),workerId=e['workerId'],workerName=e['workerName'] ))
    
    return listEvents
    

@application.route("/")
def mapview():
    listEventsAPI=[]
    listEventsAPI = getEvents()
    listMarkers=[]
    for e in listEventsAPI:
        marker={}
        
        if (e.event !="1") & (e.event!="2"):
          
            marker={
            
                "icon":'//maps.google.com/mapfiles/ms/icons/red-dot.png',               
                "infobox": (
                    "There is an <b style='color:red;'>Alert</b>!"
                    "<h2>Information:</h2>"
                    "<ul><li>DeviceId:"+e.deviceId+"</li>"
                    "<li>Event:"+e.event+"</li>"
                    "<li>eventtime:"+e.eventtime+"</li>"
                    "<li>latitude:"+str(e.latitude)+"</li>"
                    "<li>longitude:"+str(+e.longitude)+"</li>"
                    "<li>workerId:"+e.workerId+"</li>"
                    "<li>workerName:"+e.workerName+"</li>"
                    "</ul>"
                    
                ),
                "lat":e.latitude,
                "lng":e.longitude
            }
        else:
            
            marker={
                "icon": '//maps.google.com/mapfiles/ms/icons/green-dot.png',
                "infobox":("Normal Event <b style='color:blue;'></b>!"
                    "<h2>Information:</h2>"
                    "<ul><li>DeviceId:"+e.deviceId+"</li>"
                    "<li>Event:"+e.event+"</li>"
                    "<li>eventtime:"+e.eventtime+"</li>"
                    "<li>latitude:"+str(e.latitude)+"</li>"
                    "<li>longitude:"+str(+e.longitude)+"</li>"
                    "<li>workerId:"+e.workerId+"</li>"
                    "<li>workerName:"+e.workerName+"</li>"
                    "</ul>"),   
                "lat":e.latitude,
                "lng":e.longitude
        }
        listMarkers.append(marker)
    trdmap = Map(
        style="height:600px;width:1500px;",
        identifier="trdmap",
        varname="trdmap",
        markers=listMarkers,
        lat=51.032086,
        lng=-114.043629,        
    
    )     

    return render_template(
        "example.html",
        trdmap=trdmap,  
        GOOGLEMAPS_KEY=request.args.get("apikey"),
        logo = '/static/images/Logo.jpg'
    )


if __name__ == "__main__":
    application.run(debug=True, use_reloader=True)