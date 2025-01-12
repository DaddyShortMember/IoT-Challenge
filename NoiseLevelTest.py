import time
from grove.adc import ADC

class GroveNoiseSensor:

	def __init__(self, channel):
		self.channel = channel
		self.adc = ADC()

	def readNoiseLevel(self):
		value = self.adc.read(self.channel)
		return value

def main():
	sensor = GroveNoiseSensor(0)
	print("Reading noise sensor value, press ctrl + C to stop")
	try:
		while True:
			noise_value = sensor.readNoiseLevel()
			print(f"noise level: {noise_value}")
			time.sleep(0.5)
	except KeyboardInterrupt:
		print("test stopped")
		
if __name__ == "__main__":
	main() 
