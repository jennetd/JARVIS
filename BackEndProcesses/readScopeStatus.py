from AllModules import *
import ParseFunctions as pf
import TCP_com as tp

#### Look at these parameters before running the listener
UsingAutoPilot = True
Configuration = 122


numEvents = 100000
sampleRate = 5 #GSa/s
horizontalWindow = 300 #ns
### if sample rate or horizontal window is changed, TimingDAQ must be recompiled to account for new npoints.
trigCh = "AUX" 
trig = 0.15 #V

vScale1 = 0.20  
vScale2 = 1 
vScale3 = 0.05 
vScale4 = 0.1 

timeoffset = -50 #ns

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
		    	Command = "python /home/daq/JARVIS/AutoPilot/RunTableWithoutAutopilot.py %s %d" % (runNumber, Configuration)
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
		    	Command = "python /home/daq/JARVIS/AutoPilot/RunTableWithoutAutopilot.py %s %d" % (runNumber, Configuration)
		    	print Command
		    	os.system(Command)
		    	print "\n Updated the run table"

		elif ScopeState == "ready":
			print 'Change the RunLog.txt file to ready'		
