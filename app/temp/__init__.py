from flask import current_app as app
from flask_socketio import Namespace, emit


class TempNsc(Namespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_get_temp(self, temp):
        app.logger.info(f"The temp is {temp}")
        emit("send temp to web", temp, broadcast=True)
