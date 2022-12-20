from ProcessExec import *
import ProcessRuns as pr
import time
ExecutionOrder = 0 #This is descending Run number order, Refer to the dictionary in all modules
PID = 2 #2 means Timingdaq, Refer to the dictionary in all modules
GetRunListEachTime = False #Could be true also for this case.

#Give the range of run numbers to process
StartRunNumber = 60957 #35084#34511   
StopRunNumber = 61302#34679

############ Doesn't matter for tracking ###########
SaveWaveForms = True
ConfigVersion = "v11"
DigitizerKey = 6 #key=3 for KeySightScope, Refer Allmodules

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
