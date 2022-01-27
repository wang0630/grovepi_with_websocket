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
import traceback

# Init the socket io client
sio = socketio.Client(reconnection=True, reconnection_attempts=100, reconnection_delay=2)
# Define namespace
namespace = "/distance"
temp_namespace = "/temp"

# Lock
gplock = threading.Lock()


@sio.event(namespace=namespace)
def connect():
    print(f"I'm connected from {namespace}!")


@sio.event(namespace=namespace)
def connect_error(data):
    print(f"Connected fail {namespace}!")


@sio.event(namespace=namespace)
def disconnect():
    print(f"Disconnect from {namespace}!")


@sio.event(namespace=temp_namespace)
def connect():
    print(f"I'm connected from {temp_namespace}!")


@sio.event(namespace=temp_namespace)
def connect_error(data):
    print(f"Connected fail {temp_namespace}!")


@sio.event(namespace=temp_namespace)
def disconnect():
    print(f"Disconnect from {temp_namespace}!")


def get_traceback(e):
    lines = traceback.format_exception(type(e), e, e.__traceback__)
    return ''.join(lines)


class UltraSonicReader:
    def __init__(self):
        self.port = 5
        self.buzzer_port = 6
        self.distance = None

    def run(self):
        global gplock
        sleep(10)
        print('****** u thread starts *******')
        try:
            while True:
                # Connect to server with namespace distance
                with gplock:
                    if not sio.connected:
                        print('****** u thread connects *******')
                        sio.connect('http://localhost:5000', namespaces=[namespace, temp_namespace])
                    analogWrite(self.buzzer_port, 0)
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
                sleep(.5)
        except Exception as e:
            print('------Start--------')
            print(get_traceback(e))
            print('------End--------')


class TempReader:
    def __init__(self):
        self.temp_port = 6

    def run(self):
        global gplock
        sleep(10)
        print('****** t thread starts *******')
        while True:
            with gplock:
                if not sio.connected:
                    print('****** t thread connects *******')
                    # Connect to server with namespace distance and temp
                    sio.connect('http://localhost:5000', namespaces=[namespace, temp_namespace])

                [temp, humidity] = dht(6, 0)
                if (not math.isnan(temp)) and (not math.isnan(humidity)) and (humidity >= 0):
                    print(f'Temp: {temp} and humidity: {humidity}')
                    # Emit the get_distance event to the server
                    sio.emit(
                        'get_temp',
                        temp,
                        namespace=temp_namespace
                    )
            # Sleep for 5 seconds and try to acquire the lock again
            sleep(5)


if __name__ == '__main__':
    u = UltraSonicReader()
    t = TempReader()
    u_thread = threading.Thread(target=u.run, daemon=True)
    t_thread = threading.Thread(target=t.run, daemon=True)

    u_thread.start()
    t_thread.start()
    socket_io, app = create_app()
    # Explicitly state host = 0.0.0.0 to prevent network error
    socket_io.run(app, debug=True, host='0.0.0.0', port=5000)
