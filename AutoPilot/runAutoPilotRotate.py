import os
conf_list = [165,166,167,168,169,170]
AutoPilotStatus=1
runsPerConf = 2
iteration = 0
while AutoPilotStatus:
	
	os.system("python AutoPilotRotate.py -it 1 -nruns %i -conf %i"%(runsPerConf, conf_list[iteration]))
	iteration = (iteration+1) % len(conf_list)

	#################################################
	#Check for Stop signal in AutoPilot.status file
	#################################################
	tmpStatusFile = open("AutoPilot.status","r") 
	tmpString = (tmpStatusFile.read().split())[0]
	if (tmpString == "STOP" or tmpString == "stop"):
		print "Detected stop signal.\nStopping AutoPilot...\n\n"
		AutoPilotStatus = 0
	tmpStatusFile.close()