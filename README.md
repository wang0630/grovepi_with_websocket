## Grovepi + Websocket + Google Chart

### Demo
![Demo GIF](demo.gif)

### Run
`python3 assign2-b.py`

### Sensors architecture
Two threads were used, and each of the threads is responsible for one of the sensors.
1. The ultrasonic sensor is connected to pin 5, and will send data to the server via Websocket for every .3 second.
2. The temperature sensor is connected to the pin 6, and will send data to the server via Websocket for every 2 seconds.

### Websocket architecture
Files for Websocket are under `/app/distance` and `/app/temp`.
1. `on_get_resources`  event is used to receive data passing from sensors, and data will be broadcast to the browser(with `broadcast=True`) using `send resources to web` event.

### Front-end architecture
Google charts is paired with Websocket to provide real-time display.
1. Two `gauges` are used to display data from `send resources to web` event.
2. A `lineChart` is used to display the last 10 records of temperature readings.
