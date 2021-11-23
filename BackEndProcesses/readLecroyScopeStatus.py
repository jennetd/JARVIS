from AllModules import *
import ParseFunctions as pf
import TCP_com as tp

#### Look at these parameters before running the listener
UsingAutoPilot = True
Configuration = 122   ##not used except in BTL mode


#numEvents = 13000
numEvents = 500
sampleRate = 10 #GSa/s
horizontalWindow = 50 #ns
### if sample rate or horizontal window is changed, TimingDAQ must be recompiled to account for new npoints.
#trigCh = "EX" 
trigCh = "C4" 
trig =  -0.015 # V

vScale1 = 0.05  
vScale2 = 0.05
vScale3 = 0.05 
vScale4 = 0.02
vScale5 = 0.05  
vScale6 = 0.05
vScale7 = 0.05 
vScale8 = 0.05

timeoffset = 0 #-207 #ns

############### Remember to source the otsdaq environment
############### Assuming the directory structure in the KeySightScope repository is the same as on this computer

AutoPilotStatusFile = '%s/Acquisition/ScopeStatus.txt' % LecroyScopeControlDir
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
	            ScopeCommand = 'python %s/Acquisition/acquisition.py --runNum %s --numEvents %d --sampleRate %d --horizontalWindow %d --trigCh %s --trig %f --vScale1 %f --vScale2 %f --vScale3 %f --vScale4 %f --timeoffset %i --trigSlope POS' % (LecroyScopeControlDir,runNumber, numEvents, sampleRate, horizontalWindow, trigCh, trig, vScale1, vScale2, vScale3, vScale4, timeoffset) 
	            print ScopeCommand
		    #### Starting the acquisition script ####
		    os.system(ScopeCommand)

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
	            ScopeCommand = 'python %s/Acquisition/acquisition.py --runNum %s --numEvents %d --sampleRate %d --horizontalWindow %d --trigCh %s --trig %f --vScale1 %f --vScale2 %f --vScale3 %f --vScale4 %f --vScale5 %f --vScale6 %f --vScale7 %f --vScale8 %f --timeoffset %i --trigSlope POS' % (LecroyScopeControlDir,runNumber, numEvents, sampleRate, horizontalWindow, trigCh, trig, vScale1, vScale2, vScale3, vScale4,vScale5, vScale6, vScale7, vScale8, timeoffset) 
	            print ScopeCommand
		    #### Starting the acquisition script ####
		    os.system(ScopeCommand)

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
