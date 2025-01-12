import multiprocessing
import subprocess

def run(script):
	subprocess.run(['python3',script])

if __name__=="__main__":

	NoiseSensorScript = 'NoiseLevelSensorMQTT.py'
	TouchSensorScript = 'TouchSensorMQTT.py'
	HTSensorScript = 'HTSensorMQTT.py'
	HeartrateScript = 'HeartRate.py'

	p_1 = multiprocessing.Process(target=run, args=(NoiseSensorScript,))
	p_2 = multiprocessing.Process(target=run, args=(TouchSensorScript,))
	p_3 = multiprocessing.Process(target=run, args=(HTSensorScript,))
	p_4 = multiprocessing.Process(target=run, args=(HeartrateScript,))
	
	p_1.start()
	p_2.start()
	p_3.start()
	p_4.start()

	p_1.join()
	p_2.join()
	p_3.join()
	p_4.join()
