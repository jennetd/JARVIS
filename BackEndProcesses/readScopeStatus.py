from AllModules import *

numEvents = 50000 
sampleRate = 40 #GSa/s
horizontalWindow = 40 #ns
trigCh = "AUX" 
trig = -0.15 #V

vScale1 = 0.02 #V
vScale2 = 0.02 #V
vScale3 = 0.05 #V
vScale4 = 0.02 #V

timeoffset = -150e-09 #s

############### Remember to source the otsdaq environment
############### Assuming the directory structure in the KeySightScope repository is the same as on this computer

AutoPilotStatusFile = '%sAcquisition/ScopeStatus.txt' % ScopeControlDir
AgilentScopeCommand = 'python %sAcquisition/acquisition.py --numEvents %d --sampleRate %d --horizontalWindow %d --trigCh %s --trig %f --vScale1 %f --vScale1 %f --vScale1 %f --vScale1 %f --timeoffset %f' % (ScopeControlDir, numEvents, sampleRate, horizontalWindow, trigCh, trig, vScale1, vScale2, vScale3, vScale4, timeoffset) 

while True:

	inFile = open(AutoPilotStatusFile,"r")
	status = inFile.readline(1)
	time.sleep(1)
	if (status == str(1)):
	   	############### checking the status for the next runs #################  
	    with open(AutoPilotStatusFile,'w') as file:
	        file.write(str(0))
	    print "\n ####################### Running the scope acquisition ##################################\n"
	    os.system(AgilentScopeCommand)
	    print "\n ####################### Done with the scope acquisition ##################################\n"
