import smbus
import time
import paho.mqtt.client as mqtt

# Initialisation of l'I2C
bus = smbus.SMBus(1)  # Uses I2C-1
address = 0x57        # Adress of the sensor Max30100

# Configuration of the sensor Max30100
def initialize_sensor():
    bus.write_byte_data(address, 0x06, 0x03)  # Mode SpO2
    time.sleep(0.5)
    bus.write_byte_data(address, 0x09, 0x1F)  # Activates LEDs
    time.sleep(0.5)
    bus.write_byte_data(address, 0x08, 0x00)  # Congig FIFO
    print("Initialized sensor.")

# Read data
def read_sensor():
    data = bus.read_i2c_block_data(address, 0x00, 4)  # Read 4 octets
    ir_data = (data[0] << 8) | data[1]                # IR data
    red_data = (data[2] << 8) | data[3]               # Red data
    return ir_data, red_data

# MQTT configuration
broker_address = "broker.hivemq.com"
mqtt_topic = "familink/sensors/heart"
client = mqtt.Client("HeartRatePublisher")
client.tls_set()
client.connect(broker_address, 1883, 60)

# Main program
try:
    initialize_sensor()
    while True:
        ir, red = read_sensor()
        data = {"IR": ir, "Red": red}
        print(f"IR: {ir}, Red: {red}")
        client.publish(mqtt_topic, str(data))
        print(f"Données publiées : {data}")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nProgramme terminé.")
