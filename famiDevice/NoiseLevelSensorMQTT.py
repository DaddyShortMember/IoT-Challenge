import time
import json
import paho.mqtt.client as mqtt
from grove.adc import ADC

# Configuración del sensor de ruido y MQTT
LOUDNESS_SENSOR_CHANNEL = 4  # Canal del sensor de ruido
NOISE_THRESHOLD = 400  # Umbral de detección de ruido

# Configuración del broker MQTT
broker = "broker.hivemq.com"  # Dirección IP del broker MQTT (ajusta según tu caso)
port = 1883  # Puerto del broker MQTT
topic = "familink/sensors/noise"  # Tópico para los mensajes

# Función para conectar al broker MQTT
def connect_mqtt():
    client = mqtt.Client()
    try:
        print(f"Conectando al broker MQTT en {broker}:{port}...")
        client.connect(broker, port)
        print("Conexión exitosa.")
    except Exception as e:
        print(f"Error al conectar al broker MQTT: {e}")
        client = None
    return client

# Función para monitorizar el nivel de ruido y enviar los datos al broker MQTT
def monitor_noise():
    print("Monitoring noise level...")
    adc = ADC()  # Inicializa el ADC
    client = connect_mqtt()  # Conectar al broker MQTT

    if not client:
        return  # Si no se pudo conectar al broker, no continuar

    try:
        while True:
            sensor_value = adc.read(LOUDNESS_SENSOR_CHANNEL)  # Leer el valor del sensor de ruido
            if sensor_value > NOISE_THRESHOLD:
                # Si el nivel de ruido supera el umbral, enviamos los datos al broker MQTT
                message = {
                    "device_id": "noise_sensor_1",
                    "noise_level": sensor_value,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
                }
                client.publish(topic, json.dumps(message))  # Publicar el mensaje en el tópico
                print(f"Ruido detectado: {sensor_value} - Mensaje publicado al broker.")
                time.sleep(1.0)  # Esperar 1 segundo antes de la siguiente lectura
            else:
                time.sleep(0.1)  # Si el ruido es bajo, esperar 0.1 segundos antes de la siguiente lectura
    except KeyboardInterrupt:
        print("\nExiting program")
    finally:
        client.disconnect()  # Desconectar del broker MQTT
        print("Monitor stopped")

if __name__ == "__main__":
    monitor_noise()

