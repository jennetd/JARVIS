from ProcessExec import *
import ProcessRuns as pr
import time
ExecutionOrder = 0 #This is descending Run number order, Refer to the dictionary in all modules
PID = 1 #1 means conversion, Refer to the dictionary in all modules
GetRunListEachTime = False #Could be true also for this case.

#Give the range of run numbers to process
StartRunNumber = 28233   
StopRunNumber = 28234

############ Doesn't matter for tracking ###########
SaveWaveForms = True
ConfigVersion = "v9" ## doesn't matter
DigitizerKey = 3 #key=3 for KeySightScope, Refer Allmodules


ApplyFilter=True

########### Get Key ###########
key = am.GetKey()

print "\n##############################"
print "## Starting Data processing ##"
print "##############################\n"
for run in range (StartRunNumber, StopRunNumber + 1):	
	ProcessExec(ExecutionOrder,PID, SaveWaveForms, ConfigVersion,run,DigitizerKey,key,GetRunListEachTime, True, ApplyFilter)
	time.sleep(0.25)

print "\n##############################"
print "## Completed Data processing ##"
print "##############################\n"
