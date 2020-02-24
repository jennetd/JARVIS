from AllModules import *

################# For this script to run make sure to mount the CAENGECO2020 Document from the logging pc #############
##### Remember to create CAENData, move the existing log as CAENGECO2020_1.log in CAENData ###### 

while True:
	CAENUnsyncLocalPath = '/home/daq/LabviewData/CAENUnsyncData/CAENData/'
	NumberList = [(x.split("CAENGECO2020_")[1]).split(".log")[0] for x in glob.glob(CAENUnsyncLocalPath + '*CAENGECO2020_*')]
	NumberListInt = map(int,NumberList)
	MaxNumber = max(NumberListInt)
	CMD = "mv %sCAENGECO2020.log %sCAENGECO2020_%s.log" % (CAENUnsyncLocalPath,CAENUnsyncLocalPath,MaxNumber + 1)
	os.system(CMD)
        print "Saved the CAEN Log. Will save another one in some time!!!!"
	time.sleep(2000) 
