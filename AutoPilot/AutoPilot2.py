#!/bin/env python
import sys 
sys.path.append('../BackEndProcesses/')
import ParseFunctions as pf
import TCP_com as tp  #in-built 5s delay in all of them
from AllModules import *
#from muxQuery import *
#import GetTemp as gt
import json as js

################################### Important #########################################
######## This parameter defines at what time it is safe to start a new run ############
######## It should be about 30 seconds before the arrival time of each spill ##########
######## Since spills come every minute, this is defined as a number of seconds #######
######## after the start of each clock minute (only meaningful modulo 60 seconds) #####
################ Periodically make sure this value makes sense. #######################
#######################################################################################

NumSpillsPerRun = 1
#################################Parsing arguments######################################

parser = argparse.ArgumentParser(description='Information for running the AutoPilot program. /n /n General Instructions: Start OTSDAQ and Configure by hand. If using OTSDAQ make sure the start and stop seconds in the beginning of the program are hard coded correctly. /n Make sure to add sensor and configuration after each controlled access and pass it as an argument to this script. /n/n /n TekScope Specific Instructions: /n Make sure you hard code the dpo_fastframe path. /n If using the OTSDAQ with TekScope make sure the Use_otsdaq boolean is True in dpo_fastframe script. /n Make Sure you pass all four Scope trigger and channel settings. /n /n Other Digitizer Specific Instructions: /n If not running the TekScope make sure that the run file name in TCP_com is correct.')
parser.add_argument('-nruns', '--maxIterations', type=int,default=999999, help = 'Number of runs to take',required=False)

args = parser.parse_args()
Debug = True # Jennet change this
IsTelescope = True
maxRuns = int(args.maxIterations)

print("Stopping after %i runs." % maxRuns)

not_applicable = ['N/A']
not_started = ['Not started']

# Use Status file to tell autopilot when to stop.
if os.path.exists("AutoPilot.status"):
	os.remove("AutoPilot.status")
statusFile = open("AutoPilot.status","w") 
statusFile.write("START") 
statusFile.close() 
AutoPilotStatus = 1

print("*********************************************************************")
print("Starting AutoPilot")
print("*********************************************************************")
print("")

if IsTelescope:
	print("Tracking Telescope Included")
print("")
print("")
print("*********************************************************************")
print("")
print("")

# Get Start and stop seconds for the first iteration of the loop
iteration = 0
while (AutoPilotStatus == 1 and iteration < maxRuns):

	if iteration % 5 == 0:
		#if IsTelescope: StartSeconds,StopSeconds = GetStartAndStopSeconds(36, 0) #33,22
		if IsTelescope: StartSeconds,StopSeconds = GetStartAndStopSeconds(30, 10) #33,22
		else: StartSeconds,StopSeconds = GetStartAndStopSeconds(50, 22)
		print("start seconds", StartSeconds, "stop seconds", StopSeconds)

	##sync local run number file with ftbf-daq-06
#	tp.GetRunFile() # Jennet add this
	time.sleep(5)
	RunNumber = 999 #tp.GetRunNumber() # Jennet will fix later
	print("Next Run %i " % (RunNumber))
	print("")

	############ Wait for safe time to start run ##########
	wait_until(StartSeconds)

	### Preparing to start run

	RunNumber += 1 #tp.UpdateRunNumber(RunNumber+1) ## Jennet you have to do this too
#	tp.SendRunFile() # will need to enable later Jennet

	################### Starting the run ###################
	StartTime = datetime.now()  
	print("\nRun %i started at %s" % (RunNumber,StartTime))
	print("")

	#Start the otsdaq run here (scopes already started)
	if not Debug and IsTelescope: tp.start_ots(RunNumber,False)
	
	## Minimum run duration
	time.sleep(60*(NumSpillsPerRun-1))

	### Don't stop run until scope has acquired all events (OK if still writing events disk, though)
	tclock_finished=time.time()

	if not Debug and IsTelescope: tp.stop_ots(False)

	StopTime = datetime.now()
	print("\nRun %i stopped at %s" % (RunNumber,StopTime))
	print("")
	print("*********************************************************************")
	time.sleep(10) #print("")

	Duration = int((StopTime - StartTime).total_seconds())

	if pf.QueryGreenSignal(True): 		

		SpillTime = (StartTime+timedelta(0,27)).strftime("%Y-%m-%d %H:%M:%S")
		
		ETLTimestamp = (datetime.now() - datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")).total_seconds() #- 3600 ### For daylight saving time 

		#################################################
		#Check for Stop signal in AutoPilot.status file
		#################################################
		tmpStatusFile = open("AutoPilot.status","r") 
		tmpString = (tmpStatusFile.read().split())[0]
		if (tmpString == "STOP" or tmpString == "stop"):
			print("Detected stop signal.\nStopping AutoPilot...\n\n")
			AutoPilotStatus = 0
		tmpStatusFile.close()
	iteration += 1
