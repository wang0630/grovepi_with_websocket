# **************************************************************************
# TCSS 573: Internet of Things (IoT)
# The namespace of /distance websocket
# **************************************************************************
# Author: Tsung Jui Wang(twang31@uw.edu)
# **************************************************************************

from flask import current_app as app
from flask_socketio import Namespace, emit

class DistanceNsc(Namespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_get_distance(self, distance):
        app.logger.info(f"The distance is {distance}")
        # Send distance data to the web
        # broadcast=True is necessary since we are sending data to other clients except the sender
        # Other clients here are our web browsers
        emit("send distance to web", distance, broadcast=True)
