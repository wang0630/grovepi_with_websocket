# **************************************************************************
# TCSS 573: Internet of Things (IoT)
# The main class to create the Flask app
# **************************************************************************
# Author: Tsung Jui Wang(twang31@uw.edu)
# **************************************************************************


from flask import Flask, render_template
from flask_socketio import SocketIO
from grovepi import *


def create_app():
    # Create the app
    app = Flask(__name__)

    # Register the route to serve html file
    # Make sure html files are in /templates and css files are in /static
    @app.route("/")
    def getPage():
        try:
            return render_template('assign2-b.html')
        except Exception as e:
            print('An error has occured')

    # We use app inside distance module, so we need to delay the import to prevent cycle
    from .distance import DistanceNsc
    from .temp import TempNsc

    # Create socket_io wrapper
    socket_io = SocketIO(app)
    # Bind the distance namespace
    socket_io.on_namespace(DistanceNsc('/distance'))
    # Bind the temp namespace
    socket_io.on_namespace(TempNsc('/temp'))
    return socket_io, app
