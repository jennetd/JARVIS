from AllModules import *

################# For this script to run make sure to mount the CAENGECO2020 Document from the logging pc #############
##### Remember to create CAENData, move the existing log as CAENGECO2020_1.log in CAENData ###### 
CAENUnsyncLocalPath = '/home/daq/LabviewData/CAENUnsyncData/CAENData/'
CAENDefaultLogPath = '/home/daq/LabviewData/CAENUnsyncData/CAENGECO2020.log'

while True:
	NumberList = [(x.split("CAENGECO2020_")[1]).split(".log")[0] for x in glob.glob(CAENUnsyncLocalPath + '*CAENGECO2020_*')]
	NumberListInt = map(int,NumberList)
	MaxNumber = max(NumberListInt)
	CMD = "mv %s %sCAENGECO2020_%s.log" % (CAENDefaultLogPath,CAENUnsyncLocalPath,MaxNumber + 1)
	#print CMD
	os.system(CMD)
	print "Saved the CAEN Log. Will save another one in some time!!!!"
	time.sleep(2000) 
