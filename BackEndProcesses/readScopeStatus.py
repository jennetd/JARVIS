from AllModules import *
import ParseFunctions as pf
import TCP_com as tp

numEvents = 100000 
sampleRate = 40 #GSa/s
horizontalWindow = 40 #ns
### if sample rate or horizontal window is changed, TimingDAQ must be recompiled to account for new npoints.
trigCh = "AUX" 
trig = 0.15 #V

vScale1 = 0.04 #V
vScale2 = 0.04 #V
vScale3 = 0.04 #V
vScale4 = 0.05 #V

timeoffset = -100 #ns

############### Remember to source the otsdaq environment
############### Assuming the directory structure in the KeySightScope repository is the same as on this computer

AutoPilotStatusFile = '%sAcquisition/ScopeStatus.txt' % ScopeControlDir
AgilentScopeCommand = 'python %sAcquisition/acquisition.py --numEvents %d --sampleRate %d --horizontalWindow %d --trigCh %s --trig %f --vScale1 %f --vScale2 %f --vScale3 %f --vScale4 %f --timeoffset %i --trigSlope POS' % (ScopeControlDir, numEvents, sampleRate, horizontalWindow, trigCh, trig, vScale1, vScale2, vScale3, vScale4, timeoffset) 
print AgilentScopeCommand
while True:

	inFile = open(AutoPilotStatusFile,"r")
	status = inFile.readline(1)
	time.sleep(1)
	if (status == str(1)):
	   	############### checking the status for the next runs #################  
	    with open(AutoPilotStatusFile,'w') as file:
	        file.write(str(0))
	    print "\n ####################### Running the scope acquisition ##################################\n"
	    
	    #### Reading run number ####
	    #RunNumber = tp.GetRunNumber()

	    #### Starting the acquisition script ####
	    os.system(AgilentScopeCommand)

	    #### Updating the conversion field for "Not started" #####
	    #key = GetKey()
	    #FieldID = pf.GetFieldID(QueryFieldsDict[0], RunNumber, False, key)
	    #pf.UpdateAttributeStatus(FieldID[0], "ConversionKeySightScope", "Not Started", False, key)
	    
	    print "\n ####################### Done with the scope acquisition ##################################\n"
