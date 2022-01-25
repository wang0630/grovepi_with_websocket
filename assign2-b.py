# **************************************************************************
# TCSS 573: Internet of Things (IoT)
# **************************************************************************
# Author: Tsung Jui Wang(twang31@uw.edu)
# **************************************************************************
import math
import socketio
from time import *
from grovepi import *
import threading
from app import create_app

# Init the socket io client
sio = socketio.Client(reconnection=True, reconnection_attempts=100, reconnection_delay=2)
# Define namespace
namespace = "/distance"


@sio.event(namespace=namespace)
def connect():
    print("I'm connected!")


@sio.event(namespace=namespace)
def connect_error(data):
    print("The connection failed!")


@sio.event(namespace=namespace)
def disconnect():
    print("I'm disconnected!")


class UltraSonicReader:
    def __init__(self):
        self.port = 5
        self.buzzer_port = 6
        self.distance = None
        self.should_keep_sensing = True

    def run(self):
        try:
            sleep(10)
            # Connect to server with namespace distance
            sio.connect('http://localhost:5000', namespaces=[namespace])

            analogWrite(self.buzzer_port, 0)
            while self.should_keep_sensing:
                sleep(.1)
                dist = ultrasonicRead(self.port)

                if (not math.isnan(dist)) and (dist >= 0):
                    # Emit the get_distance event to the server
                    sio.emit(
                        'get_distance',
                        dist,
                        namespace='/distance'
                    )
                    print(f'Distance: {dist}')
                    if 10 < dist <= 30:
                        analogWrite(self.buzzer_port, 10)
                    elif dist <= 30:
                        analogWrite(self.buzzer_port, 100)
                    else:
                        analogWrite(self.buzzer_port, 0)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    u = UltraSonicReader()
    thread = threading.Thread(target=u.run, daemon=True)
    thread.start()
    socket_io, app = create_app()
    # Explicitly state host = 0.0.0.0 to prevent network error
    socket_io.run(app, debug=True, host='0.0.0.0', port=5000)
