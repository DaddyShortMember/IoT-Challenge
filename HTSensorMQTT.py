import time
import seeed_dht
import paho.mqtt.client as mqtt
import json

# Configuración del sensor DHT
sensor = seeed_dht.DHT("11", 12)  # DHT11 en el pin GPIO 12
# Si usas DHT22, usa la siguiente línea:
# sensor = seeed_dht.DHT("22", 12)

# Configuración del broker MQTT
broker = "broker.hivemq.com"  # Dirección IP de tu broker MQTT
port = 1883
topic = "familink/sensors/humid"  # El topic donde publicarás los datos

# Configuración del cliente MQTT
client = mqtt.Client()

# Función para conectar al broker
def connect_mqtt():
    try:
        print(f"Conectando al broker MQTT en {broker}:{port}...")
        client.connect(broker, port)
        print("Conexión exitosa al broker.")
    except Exception as e:
        print(f"Error al conectar al broker: {e}")
        exit(1)

# Función para enviar los datos de humedad y temperatura
def send_data_to_mqtt(humidity, temperature):
    message = {
        "device_id": "humidity_sensor_1",
        "humidity": humidity,
        "temperature": temperature,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    try:
        client.publish(topic, json.dumps(message))
        print(f"Mensaje publicado: {message}")
    except Exception as e:
        print(f"Error al publicar mensaje: {e}")

# Función principal para monitorear el sensor y enviar los datos
def main():
    connect_mqtt()  # Conectamos al broker MQTT

    while True:
        humi, temp = sensor.read()

        if humi is not None:  # Verificamos si la lectura es válida
            print(f"DHT{sensor.dht_type}, humedad {humi:.1f}%, temperatura {temp:.1f}°C")
            send_data_to_mqtt(humi, temp)  # Enviar los datos al broker MQTT
        else:
            print(f"DHT{sensor.dht_type}, error en la lectura")

        time.sleep(5)  # Esperamos 5 segundos antes de la siguiente lectura

if __name__ == '__main__':
    main()

