import os
#conf_list = [169,183,165,166,167,168]
# conf_list = [171,172,173,174,175,176]
conf_list = [440,441]
AutoPilotStatus=1
runsPerConf = 1
iteration = 0
while AutoPilotStatus:
	
	os.system("python AutoPilot2.py -it 0 -nruns %i -conf %i"%(runsPerConf, conf_list[iteration]))
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
