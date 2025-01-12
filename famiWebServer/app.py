from flask import Flask, request, jsonify, render_template, Response
from flask_mqtt import Mqtt
import os
import json
import time

TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

connection_status = "Off"
status_updated = 0

touch_updated = False
last_touch = 0

noise_updated = False
last_noise = 0
last_noise_level = 0
highest_noise_level = 0

heart_updated = False
ir = 0
red = 0

humid_updated = False
temp = 0
hum = 0

# [MQTT]
# MQTT Configuration
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_CLIENT_ID'] = 'familink_webserver'
app.config['MQTT_KEEPALIVE'] = 60

mqtt = Mqtt(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    global connection_status, status_updated
    print("Connected to MQTT Broker!")
    connection_status = "On"
    status_updated = 1
    mqtt.subscribe('familink/sensors/touch')  # Subscribing to a single topic
    mqtt.subscribe('familink/sensors/noise')  # Subscribing to another topic
    mqtt.subscribe('familink/sensors/heart')  # Subscribing to a third topic
    mqtt.subscribe('familink/sensors/humid')  # Subscribing to a fourth topic

# Handling incoming MQTT messages
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    try:
        topic = message.topic
        payload = message.payload.decode()  # Decode the message payload
        print(f"Received message on topic {topic}: {payload}")

        # Parse payload as JSON
        data = json.loads(payload)

        # Store or process the data based on topic
        if topic == 'familink/sensors/touch':
            handle_touch_data(data)
        elif topic == 'familink/sensors/noise':
            handle_noise_data(data)
        elif topic == 'familink/sensors/heart':
            handle_heart_data(data)
        elif topic == 'familink/sensors/humid':
            handle_humid_data(data)
        else:
            print(f"Unhandled topic: {topic}")

    except json.JSONDecodeError:
        print(f"Failed to decode JSON from topic {topic}: {message.payload}")

# Handlers for each topic
def handle_touch_data(data):
    global touch_updated, last_touch
    if 'timestamp' in data:
        touch_updated = True
        last_touch = data['timestamp']
        print(f"Touch event at {data['timestamp']}")

def handle_noise_data(data):
    global noise_updated, last_noise, last_noise_level, highest_noise_level
    if 'noise_level' in data:
        noise_updated = True
        last_noise = data['timestamp']
        last_noise_level = data['noise_level']
        if last_noise_level > highest_noise_level:
            highest_noise_level = last_noise_level
        print(f"Noise level: {data['noise_level']}")

def handle_heart_data(data):
    global heart_updated, ir, red
    if 'ir' in data and 'red' in data:
        heart_updated = True
        ir = data['ir']
        red = data['red']
        print(f"Heart rate data - IR: {data['ir']}, RED: {data['red']}")

def handle_humid_data(data):
    global humid_updated, temp, hum
    if 'timestamp' in data:
        humid_updated = True
        temp = data['temperature']
        hum = data['humidity']
        print(f"Humidity event at {data['timestamp']}")

# [REFRESH]

# Stat Refresh
def refStat():
    global status_updated
    while True:
        if status_updated:  # Check if new data is available
            stat = {
                "connection_status": connection_status,
            }
            yield f"data: {json.dumps(stat)}\n\n"
            status_updated = False  # Reset the flag
        time.sleep(0.5)  # Slight delay to avoid busy looping

# Touch Refresh
def refTouch():
    global touch_updated
    while True:
        if touch_updated:  # Check if new data is available
            touch_data = {
                "last_touch": last_touch,
            }
            yield f"data: {json.dumps(touch_data)}\n\n"
            touch_updated = False  # Reset the flag
        time.sleep(0.5)  # Slight delay to avoid busy looping

# Noise Refresh
def refNoise():
    global noise_updated
    while True:
        if noise_updated:  # Check if new data is available
           noise_data = {
                "last_noise": last_noise,
                "last_noise_level": last_noise_level,
                "highest_noise_level": highest_noise_level
            }
           yield f"data: {json.dumps(noise_data)}\n\n"
           noise_updated = False  # Reset the flag
        time.sleep(0.5)  # Slight delay to avoid busy looping

# Heart Refresh
def refHeart():
    global heart_updated
    while True:
        if heart_updated:  # Check if new data is available
            heart_data = {
                "ir": ir,
                "red": red,
            }
            yield f"data: {json.dumps(heart_data)}\n\n"
            heart_updated = False  # Reset the flag
        time.sleep(0.5)  # Slight delay to avoid busy looping

# Humid Refresh
def refHumid():
    global humid_updated
    while True:
        if humid_updated:  # Check if new data is available
            humid_data = {
                "temperature": temp,
                "humidity": hum,
            }
            yield f"data: {json.dumps(humid_data)}\n\n"
            humid_updated = False  # Reset the flag
        time.sleep(0.5)  # Slight delay to avoid busy looping

# Status Streams
@app.route('/stream-stat', methods=['GET'])
def streamStat():
    return Response(refStat(), content_type='text/event-stream')

# Touch Stream
@app.route('/stream-touch', methods=['GET'])
def streamTouch():
    return Response(refTouch(), content_type='text/event-stream')

# Noise Stream
@app.route('/stream-noise', methods=['GET'])
def streamNoise():
    return Response(refNoise(), content_type='text/event-stream')

# Heart Stream
@app.route('/stream-heart', methods=['GET'])
def streamHeart():
    return Response(refHeart(), content_type='text/event-stream')

# Humid Stream
@app.route('/stream-humid', methods=['GET'])
def streamHumid():
    return Response(refHumid(), content_type='text/event-stream')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
