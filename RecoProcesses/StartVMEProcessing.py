from ProcessExec import *
import ProcessRuns as pr

print "Start VME data processing"

ExecutionOrder = 1 #This is Ascending Run number order
TimingDAQPID = 2 #2 means VME Processing 
SaveWaveForms = True
ConfigVersion = "v1"
RunNumber = -1 #-1 means do all runs
DigitizerKey = 0 #key=0 for VME

#You need to make a file called "key" that sits inside the RecoProcesses directory and contains the key password for the database.
keyFile = open("key", "r")
key = str(keyFile.read().strip())

ProcessExec(ExecutionOrder,TimingDAQPID, SaveWaveForms, ConfigVersion,RunNumber,DigitizerKey,key)

