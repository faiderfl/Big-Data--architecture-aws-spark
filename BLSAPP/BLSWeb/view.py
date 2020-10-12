from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons


application = Flask(__name__, template_folder=".")
GoogleMaps(application)

@application.route("/")



def init():
    print("Hello World")
    return render_template('example.html')


if __name__ == "__main__":
    application.run(debug=True)