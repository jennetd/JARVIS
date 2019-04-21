from ProcessExec import *
import ProcessRuns as pr

ExecutionOrder = 0 #This is descending Run number order, Refer to the dictionary in all modules
PID = 2 #2 means Timingdaq, Refer to the dictionary in all modules
GetRunListEachTime = True 

############ Doesn't matter for tracking ###########
SaveWaveForms = True
ConfigVersion1 = "v3"
ConfigVersion2 = "v4"
DigitizerKey = 0 #key=0 for VME, Refer Allmodules

########### Get Key ###########
key = am.GetKey()

print "\n##############################"
print "## Starting Data processing ##"
print "##############################\n"

ProcessExecBTL(ExecutionOrder,PID, SaveWaveForms, ConfigVersion1, ConfigVersion2, -1,DigitizerKey,key,GetRunListEachTime)

print "\n##############################"
print "## Completed Data processing ##"
print "##############################\n"