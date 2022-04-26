from ProcessExec import *
import ProcessRuns as pr

ExecutionOrder = 0 #This is descending Run number order, Refer to the dictionary in all modules
PID = 5 #5 means watching condor, Refer to the dictionary in all modules
GetRunListEachTime = False 

############ Doesn't matter for tracking ###########
SaveWaveForms = True
ConfigVersion = "v11"
DigitizerKey = 6 #key=3 for KeySightScope, Refer Allmodules

########### Get Key ###########
key = am.GetKey()

print "\n##############################"
print "## Starting Data processing ##"
print "##############################\n"

ProcessExec(ExecutionOrder,PID, SaveWaveForms, ConfigVersion,-1,DigitizerKey,key,GetRunListEachTime, True)

print "\n##############################"
print "## Completed Data processing ##"
print "##############################\n"
