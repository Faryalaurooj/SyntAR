import os
import time

path = 'Backgroundsdataset/'
for f in os.listdir(path):
	file = f

	cmd = "python main_train.py --input_name " + file
	print ("Harmonization Command : ",cmd)

	if os.system(cmd) != 0:
		print ("Failed command : ", cmd)
	else:
		print ("command completed")	
	print ("----------------------------------------------------")
	#time.sleep(10500)
