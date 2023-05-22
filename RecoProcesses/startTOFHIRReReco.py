from ProcessExec import *
import ProcessRuns as pr
import time
ExecutionOrder = 0 #This is descending Run number order, Refer to the dictionary in all modules
PID = 8 #2 means Timingdaq, Refer to the dictionary in all modules
GetRunListEachTime = True #Could be true also for this case.

#Give the range of run numbers to process
StartRunNumber = 66356
StopRunNumber = 68078

############ Doesn't matter for tracking ###########
SaveWaveForms = True
ConfigVersion = "v1"
DigitizerKey = 5 #key=3 for KeySightScope, Refer Allmodules

########### Get Key ###########
key = am.GetKey()

print "\n##############################"
print "## Starting Data processing ##"
print "##############################\n"
for run in range (StartRunNumber, StopRunNumber + 1):	
	ProcessExec(ExecutionOrder,PID, SaveWaveForms, ConfigVersion,run,DigitizerKey,key,GetRunListEachTime, True)
	time.sleep(0.25)

print "\n##############################"
print "## Completed Data processing ##"
print "##############################\n"
