import os
#conf_list = [r for r in range(810, 816+1)] # OV 3.5, ith1 scan
#conf_list = list(range(810,815)) + list(range(817,822))+ list(range(824,829))+ list(range(854,863)) # Select specific OV configs which are non consecutive
#conf_list = list(range(818,822))+ list(range(824,829))+ list(range(854,863)) # Select specific OV configs which are non consecutive
conf_list = list(range(810,815)) + list(range(817,822))+ list(range(854,863)) # 3.5,1.5,0.5,0.8

#conf_list = list(range(818,822))+ list(range(854,863))


#conf_list = list(range(854,863))

#conf_list = list(range(860,862+1)) 

#conf_list = range(860,863)
AutoPilotStatus=1
runsPerConf = 1
#runsPerConf = 1
iteration = 0
while AutoPilotStatus:
	
	os.system("python AutoPilot2.py -it 1 -nruns %i -conf %i"%(runsPerConf, conf_list[iteration]))
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
