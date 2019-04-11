from ProcessExec import *
import ProcessRuns as pr

ExecutionOrder = 1 #This is Ascending Run number order, Refer to the dictionary in all modules
PID = 0 #0 means Tracking, Refer to the dictionary in all modules
GetRunListEachTime = False #Could be true also for this case.

#Give the range of run numbers to process
StartRunNumber = 1706
StopRunNumber = 1706

############ Doesn't matter for tracking ###########
SaveWaveForms = True
ConfigVersion = "v1"
DigitizerKey = 0 #key=0 for VME, Refer Allmodules

########### Get Key ###########
keyFilePath = "../RecoProcesses/key"
key = None
NoKeyFile = False
if os.path.exists(keyFilePath): 
	keyFile = open(keyFilePath, "r")
	key = str(keyFile.read().strip())
 	keyFile.close()
else:
	NoKeyFile = True
if key == '' or NoKeyFile:
	raise Exception('\n\n ################################################################################################ \n ######Either the key file is not present in the current directory or there is no key in it!########\n ########################################################################################################### \n\n')

print "\n##############################"
print "## Starting Data processing ##"
print "##############################\n"

for run in range (StartRunNumber, StopRunNumber + 1):	
        ProcessExec(ExecutionOrder,PID, SaveWaveForms, ConfigVersion,run,DigitizerKey,key,GetRunListEachTime)

print "\n##############################"
print "## Completed Data processing ##"
print "##############################\n"
