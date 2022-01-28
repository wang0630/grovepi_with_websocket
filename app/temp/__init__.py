# **************************************************************************
# TCSS 573: Internet of Things (IoT)
# The namespace of /temp websocket
# **************************************************************************
# Author: Tsung Jui Wang(twang31@uw.edu)
# **************************************************************************

from flask import current_app as app
from flask_socketio import Namespace, emit


class TempNsc(Namespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_get_temp(self, temp):
        app.logger.info(f"The temp is {temp}")
        # Send temp data to the web
        # broadcast=True is necessary since we are sending data to other clients except the sender
        # Other clients here are our web browsers
        emit("send temp to web", temp, broadcast=True)
