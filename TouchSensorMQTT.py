import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import json
import time

# Configuración del GPIO para el Touch Sensor
TOUCH_PIN = 5  # Cambia este número si el sensor está conectado a otro pin GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TOUCH_PIN, GPIO.IN)

# Configuración del broker MQTT
broker = "broker.hivemq.com"  # Dirección IP de tu broker MQTT
port = 1883
topic = "familink/sensors/touch"  # Topic en el que se publicarán los datos

# Configuración del cliente MQTT
client = mqtt.Client()

try:
    # Conectar al broker
    print(f"Conectando al broker MQTT en {broker}:{port}...")
    client.connect(broker, port)
    print("Conexión exitosa.")

    previous_state = None  # Estado anterior del sensor para detectar cambios

    while True:
        # Leer el estado del Touch Sensor
        current_state = GPIO.input(TOUCH_PIN)

        # Determinar si está activo o inactivo
        activity = "active" if current_state == GPIO.HIGH else "inactive"

        # Publicar datos solo si el estado cambia
        if activity != previous_state:
            message = {
                "device_id": "touch_sensor_1",
                "activity": activity,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
            # Publicar el mensaje al broker MQTT
            client.publish(topic, json.dumps(message))
            print(f"Mensaje publicado: {message}")
            previous_state = activity

        time.sleep(1)  # Tiempo entre lecturas (ajustable)

except KeyboardInterrupt:
    print("Interrumpido por el usuario. Cerrando...")
finally:
    GPIO.cleanup()  # Limpiar la configuración del GPIO
    client.disconnect()  # Desconectar del broker MQTT
    print("Limpieza completada.")

