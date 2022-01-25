from flask import current_app as app
from flask_socketio import Namespace, emit

class DistanceNsc(Namespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_get_distance(self, distance):
        app.logger.info(f"The distance is {distance}")
        emit("send distance to web", distance, broadcast=True)
