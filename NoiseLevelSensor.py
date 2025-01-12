import time
from grove.adc import ADC

LOUDNESS_SENSOR_CHANNEL=4
NOISE_THRESHOLD=400

def monitor_noise():
	print("Monitoring noise level...")
	try:
		adc=ADC()
		while True:
			sensor_value = adc.read(LOUDNESS_SENSOR_CHANNEL)
			if(sensor_value>NOISE_THRESHOLD):
				print(f"sonido detectado: {sensor_value}")
				time.sleep(1.0)
			else:
				time.sleep(0.1)
	except KeyboardInterrupt:
		print("\nExiting program")
	finally:
		print("Monitor stopped")

if __name__=="__main__":
	monitor_noise()
