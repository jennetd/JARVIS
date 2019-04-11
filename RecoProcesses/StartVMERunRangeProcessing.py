from ProcessExec import *
import ProcessRuns as pr

ExecutionOrder = 1 #This is Ascending Run number order, Refer to the dictionary in all modules
PID = 2 #3 means Timngdaq, Refer to the dictionary in all modules
StartRunNumber = 1706
StopRunNumber = 1706

############ Doesn't matter for tracking ###########
SaveWaveForms = True
ConfigVersion = "v1"
DigitizerKey = 0 #key=0 for VME, Refer Allmodules

#You need to make a file called "key" that sits inside the RecoProcesses directory and contains the key password for the database.
keyFile = open("key", "r")
key = str(keyFile.read().strip())

print "\n##############################"
print "## Starting Data processing ##"
print "##############################\n"

for run in range (StartRunNumber, StopRunNumber + 1):	
        ProcessExec(ExecutionOrder,PID, SaveWaveForms, ConfigVersion,run,DigitizerKey,key)

print "\n##############################"
print "## Completed Data processing ##"
print "##############################\n"
