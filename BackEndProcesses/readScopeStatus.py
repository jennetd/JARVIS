#!/bin/python
from AllModules import *
import ParseFunctions as pf
import TCP_com as tp

#### Look at these parameters before running the listener
UsingAutoPilot = True
Configuration = 122   ##not used except in BTL mode


numEvents = 10000
sampleRate = 20 #GSa/s 10
horizontalWindow = 40 #ns 20000
### if sample rate or horizontal window is changed, TimingDAQ must be recompiled to account for new npoints.
trigCh = "AUX" 
#trigCh = "4" 
#trig =  -0.020 # V
#trig =  -0.070 # V
trig = 0.500 # V

vScale1 = 0.2
vScale2 = 0.1
vScale3 = 0.1
vScale4 = 0.15

timeoffset = -70 #-207 #-207 #ns
TimeOut= 23 #Max run duration [s]. Use -1 for no timeout. 38 for telescope, 23 for photek mode

############### Remember to source the otsdaq environment
############### Assuming the directory structure in the KeySightScope repository is the same as on this computer

AutoPilotStatusFile = '%sAcquisition/ScopeStatus.txt' % ScopeControlDir
#AgilentScopeCommand = 'python %sAcquisition/acquisition.py --numEvents %d --sampleRate %d --horizontalWindow %d --trigCh %s --trig %f --vScale1 %f --vScale2 %f --vScale3 %f --vScale4 %f --timeoffset %i --trigSlope POS' % (ScopeControlDir, numEvents, sampleRate, horizontalWindow, trigCh, trig, vScale1, vScale2, vScale3, vScale4, timeoffset) 
#print AgilentScopeCommand
while True:

	inFile = open(AutoPilotStatusFile,"r")
	runNumber = inFile.readline().strip()
	time.sleep(1)
	if (runNumber != str(0)):

		ScopeStateHandle = open(ScopeStateFileName, "r")
		ScopeState = str(ScopeStateHandle.read().strip())

		if not UsingAutoPilot and ScopeState == "ready":

		   	############### checking the status for the next runs #################  
		    with open(AutoPilotStatusFile,'w') as file:
		        file.write(str(0))
		    print "\n ####################### Running the scope acquisition ##################################\n"
		    
		    #### Reading run number ####
		    #RunNumber = tp.GetRunNumber()
	            AgilentScopeCommand = 'python %sAcquisition/acquisition.py --runNum %s --numEvents %d --sampleRate %d --horizontalWindow %d --trigCh %s --trig %f --vScale1 %f --vScale2 %f --vScale3 %f --vScale4 %f --timeoffset %i --trigSlope POS' % (ScopeControlDir,runNumber, numEvents, sampleRate, horizontalWindow, trigCh, trig, vScale1, vScale2, vScale3, vScale4, timeoffset) 
	            print AgilentScopeCommand
		    #### Starting the acquisition script ####
		    os.system(AgilentScopeCommand)

		    #### Updating the conversion field for "Not started" #####
		    #key = GetKey()
		    #FieldID = pf.GetFieldID(QueryFieldsDict[0], RunNumber, False, key)
		    #pf.UpdateAttributeStatus(FieldID[0], "ConversionKeySightScope", "Not Started", False, key)
		    
		    print "\n ####################### Done with the scope acquisition ##################################\n"

		    if not UsingAutoPilot:
		    	print "Updating the run table from the scope listener script"
		    	Command = "python ../AutoPilot/RunTableWithoutAutopilot.py %s %d" % (runNumber, Configuration)
		    	print Command
		    	os.system(Command)
		    	print "\n Updated the run table"
		elif UsingAutoPilot:

		   	############### checking the status for the next runs #################  
		    with open(AutoPilotStatusFile,'w') as file:
		        file.write(str(0))
		    print "\n ####################### Running the scope acquisition ##################################\n"
		    
		    #### Reading run number ####
		    #RunNumber = tp.GetRunNumber()
	            # AgilentScopeCommand = 'python %sAcquisition/acquisition.py --timeout %i --runNum %s --numEvents %d --sampleRate %d --horizontalWindow %d --trigCh %s --trig %f --vScale1 %f --vScale2 %f --vScale3 %f --vScale4 %f --timeoffset %i --trigSlope POS' % (ScopeControlDir,TimeOut,runNumber, numEvents, sampleRate, horizontalWindow, trigCh, trig, vScale1, vScale2, vScale3, vScale4, timeoffset) 
	            AgilentScopeCommand = 'python %sAcquisition/acquisition.py --timeout %i --runNum %s --numEvents %d --sampleRate %d --horizontalWindow %d --trigCh %s --trig %f --vScale1 %f --vScale2 %f --vScale3 %f --vScale4 %f --timeoffset %i --trigSlope POS' % (ScopeControlDir,TimeOut,runNumber, numEvents, sampleRate, horizontalWindow, trigCh, trig, vScale1, vScale2, vScale3, vScale4, timeoffset) 
	            print AgilentScopeCommand
		    #### Starting the acquisition script ####
		    os.system(AgilentScopeCommand)

		    #### Updating the conversion field for "Not started" #####
		    #key = GetKey()
		    #FieldID = pf.GetFieldID(QueryFieldsDict[0], RunNumber, False, key)
		    #pf.UpdateAttributeStatus(FieldID[0], "ConversionKeySightScope", "Not Started", False, key)
		    
		    print "\n ####################### Done with the scope acquisition ##################################\n"

		    if not UsingAutoPilot:
		    	print "Updating the run table from the scope listener script"
		    	Command = "python ../AutoPilot/RunTableWithoutAutopilot.py %s %d" % (runNumber, Configuration)
		    	print Command
		    	os.system(Command)
		    	print "\n Updated the run table"

		elif ScopeState == "ready":
			print 'Change the RunLog.txt file to ready'		
