#!/bin/env python
import sys 
sys.path.append('../BackEndProcesses/')
import ParseFunctions as pf
import TCP_com as tp  #in-built 5s delay in all of them
from AllModules import *
from muxQuery import *
import GetTemp as gt
import json as js

################################### Important #########################################
######## This parameter defines at what time it is safe to start a new run ############
######## It should be about 30 seconds before the arrival time of each spill ##########
######## Since spills come every minute, this is defined as a number of seconds #######
######## after the start of each clock minute (only meaningful modulo 60 seconds) #####
################ Periodically make sure this value makes sense. #######################
#######################################################################################

NumSpillsPerRun = 1
SetMux=True
#################################Parsing arguments######################################

parser = argparse.ArgumentParser(description='Information for running the AutoPilot program. /n /n General Instructions: Start OTSDAQ and Configure by hand. If using OTSDAQ make sure the start and stop seconds in the beginning of the program are hard coded correctly. /n Make sure to add sensor and configuration after each controlled access and pass it as an argument to this script. /n/n /n TekScope Specific Instructions: /n Make sure you hard code the dpo_fastframe path. /n If using the OTSDAQ with TekScope make sure the Use_otsdaq boolean is True in dpo_fastframe script. /n Make Sure you pass all four Scope trigger and channel settings. /n /n Other Digitizer Specific Instructions: /n If not running the TekScope make sure that the run file name in TCP_com is correct.')
parser.add_argument('-de', '--Debug', type=int, default = 0, required=False)
parser.add_argument('-it', '--IsTelescope', type=int,default=0, help = 'Give 1 if using the telescope',required=False)
parser.add_argument('-conf', '--Configuration', type=int, help = 'Make sure to add the configuration in the run table. Give COnfiguration S/N from the run table',required=True)
parser.add_argument('-nruns', '--maxIterations', type=int,default=999999, help = 'Number of runs to take',required=False)

args = parser.parse_args()
Debug = args.Debug
IsTelescope = args.IsTelescope
Configuration = args.Configuration
maxRuns = int(args.maxIterations)

Debug=False
########################### Only when Run table is used ############################
########### Get Key ###########
key = GetKey()
print "Stopping after %i runs." % maxRuns


############ Getting the digitizer list from the configuration table #############
DigitizerList = pf.GetDigiFromConfig(Configuration, False, key)


not_applicable = ['N/A']
not_started = ['Not started']

default_run_info = {}

default_run_info["Tracking"] = not_applicable
#Keysight fields
default_run_info["xrdcpRawKeySightScope"] = not_applicable
default_run_info["ConversionKeySightScope"] = not_applicable
default_run_info["TimingDAQKeySightScope"] = not_applicable
default_run_info["TimingDAQNoTracksKeySightScope"] = not_applicable
#Lecroy fields
default_run_info["xrdcpRawLecroyScope"] = not_applicable
default_run_info["ConversionLecroyScope"] = not_applicable
default_run_info["TimingDAQLecroyScope"] = not_applicable
default_run_info["TimingDAQNoTracksLecroyScope"] = not_applicable

############ Initialize progress fields on run table ################
if IsTelescope: default_run_info["Tracking"] = not_started

IncludesKeySightScope=False
IncludesLecroyScope = False
if 'KeySightScope' in DigitizerList: IncludesKeySightScope = True
if 'LecroyScope' in DigitizerList: IncludesLecroyScope = True


# Check if specified configuration exists
if pf.QueryGreenSignal(True):
	ConfigID = pf.GetFieldIDOtherTable('Config', 'Configuration number', str(Configuration), False, key)

if not ConfigID: 
	raise Exception('\n The sensor and configuration you passed as argument are not in the table!!!!!!!!!!!!!!!!!!!! \n')
	##### Exit the program ######

###Update local copy of configurations
ConfigDict, LecroyDict,KeySightDict, CAENDict,SensorDict = pf.DownloadConfigs(False, key)
lecroyConfID,caenConfID = pf.getConfigsByGConf(ConfigDict,Configuration)
simpleLecroyDict= pf.getSimpleLecroyDict(LecroyDict,SensorDict,lecroyConfID)
simpleCAENDict= pf.getSimpleCAENDict(CAENDict,SensorDict,caenConfID)


# print caenConfID
# print ConfigDict
# print simpleLecroyDict
# print simpleCAENDict

#### Set multiplexer channels for this config
if SetMux: ConfigureMux(Configuration)


# Use Status file to tell autopilot when to stop.
if os.path.exists("AutoPilot.status"):
	os.remove("AutoPilot.status")
statusFile = open("AutoPilot.status","w") 
statusFile.write("START") 
statusFile.close() 
AutoPilotStatus = 1

print "*********************************************************************"
print "Starting AutoPilot"
print "*********************************************************************"
print ""
print "Using Configuration : ", Configuration

if IsTelescope:
	print "Tracking Telescope Included"
if IncludesKeySightScope:
	print "Keysight Scope readout Included"
if IncludesLecroyScope:
	print "Lecroy Scope readout Included"
print ""
print ""
print "*********************************************************************"
print ""
print ""

# Get Start and stop seconds for the first iteration of the loop
iteration = 0
while (AutoPilotStatus == 1 and iteration < maxRuns):

	if iteration % 5 == 0:
		if IsTelescope: StartSeconds,StopSeconds = GetStartAndStopSeconds(36, 22) #33,22
		else: StartSeconds,StopSeconds = GetStartAndStopSeconds(50, 22)
		print StartSeconds, StopSeconds

	## Refresh this in case a digitizer was removed last run.
	DigitizerList = pf.GetDigiFromConfig(Configuration, False, key)

	##sync local run number file with ftbf-daq-06
	tp.GetRunFile()
	time.sleep(5)
	RunNumber = tp.GetRunNumber()
	print "Next Run %i " % (RunNumber)
	print ""

	############ Wait for safe time to start run ##########
	wait_until(StartSeconds)

	KeySightScopeIncludedThisRun = False
	if IncludesKeySightScope:
		currentKeySightScopeState = ScopeState()
		if currentKeySightScopeState == 'busy':
			print "[WARNING] : Scope is still acquiring events, but autopilot is ready to start a new run. Likely someone killed a run prematurely. Tracking for scope in previous run is screwed up." 

		if currentKeySightScopeState == 'ready': 
			print("\n Sending start command to scope.\n")
			if not Debug:
				ScopeStatusAutoPilot(RunNumber)
				KeySightScopeIncludedThisRun = True
				WaitForScopeStart()
			print("Scope has started.")
		else:
			# print("Scope still busy. Excluding scope from the next run\n")
			print("Scope still busy. Wait for next chance.\n")
			continue #### Should instead check both scopes before continue command.....



	LecroyScopeIncludedThisRun = False
	if IncludesLecroyScope:	
		currentLecroyScopeState = LecroyScopeState()
		if currentLecroyScopeState == 'busy':
			print "[WARNING] : Lecroy Scope is still acquiring events, but autopilot is ready to start a new run. Likely someone killed a run prematurely. Tracking for scope in previous run is screwed up." 

		if currentLecroyScopeState == 'ready': 
			print("\n Sending start command to Lecroy scope.\n")
			if not Debug:
				LecroyScopeStatusAutoPilot(RunNumber)
				LecroyScopeIncludedThisRun = True
				WaitForLecroyScopeStart()
			print("Lecroy Scope has started.")
		else:			
			print("Lecroy Scope still busy. Wait for next chance.\n")
			continue


	### Preparing to start run
	tp.UpdateRunNumber(RunNumber+1) ##must be called after scope start.
	tp.SendRunFile()
	print "Keysight Scope included ",KeySightScopeIncludedThisRun
	print "Lecroy Scope included ",LecroyScopeIncludedThisRun
	################### Starting the run ###################
	StartTime = datetime.now()  
	print "\nRun %i started at %s" % (RunNumber,StartTime)
	print ""

	#Start the otsdaq run here (scopes already started)
	if not Debug and IsTelescope: tp.start_ots(RunNumber,False)
	
	#####Initialize run info dictionary to save to AirTable ####
	this_run_info = default_run_info.copy()
	#####

	DigiListThisRun = []
	if KeySightScopeIncludedThisRun:
		DigiListThisRun.append("KeySightScope")
		this_run_info["xrdcpRawKeySightScope"] = not_started
		this_run_info["ConversionKeySightScope"] = not_started
		this_run_info["TimingDAQNoTracksKeySightScope"] = not_started
		if IsTelescope:
			this_run_info["TimingDAQKeySightScope"] = not_started

	if LecroyScopeIncludedThisRun:
		DigiListThisRun.append("LecroyScope")
		this_run_info["xrdcpRawLecroyScope"] = not_started
		this_run_info["ConversionLecroyScope"] = not_started
		this_run_info["TimingDAQNoTracksLecroyScope"] = not_started
		if IsTelescope:
			this_run_info["TimingDAQLecroyScope"] = not_started


	## Minimum run duration
	time.sleep(60*(NumSpillsPerRun-1))

	### Don't stop run until scope has acquired all events (OK if still writing events disk, though)
	scope_finished=0

	if ((IncludesKeySightScope and KeySightScopeIncludedThisRun) or (IncludesLecroyScope and LecroyScopeIncludedThisRun)):
		time.sleep(15)
				
	if IncludesKeySightScope and KeySightScopeIncludedThisRun:		
		print "Waiting for Keysight scope to finish"
		WaitForScopeFinishAcquisition()
		scope_finished=time.time()
		print "Keysight scope finished"
		
	if IncludesLecroyScope and LecroyScopeIncludedThisRun:		
		print "Waiting for Lecroy scope to finish"
		WaitForLecroyScopeFinishAcquisition()
		scope_finished=time.time()
		print "Lecroy scope finished"

		
	print "Waiting for TClock stop time (%0.1f)"%StopSeconds
	wait_until(StopSeconds)
	tclock_finished=time.time()



	if not Debug and IsTelescope: tp.stop_ots(False)

	print ("%0.1f seconds between scope finish and TClock time" % (tclock_finished-scope_finished))
	StopTime = datetime.now()
	print "\nRun %i stopped at %s" % (RunNumber,StopTime)
	print ""
	print "*********************************************************************"
	print ""

	Duration = int((StopTime - StartTime).total_seconds())

	if pf.QueryGreenSignal(True): 		

		SpillTime = (StartTime+timedelta(0,27)).strftime("%Y-%m-%d %H:%M:%S")
		
		ETLTimestamp = (datetime.now() - datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")).total_seconds() #- 3600 ### For daylight saving time 
		print 'Getting ETL environmental data'
		# Temp13ETL, Temp14ETL, Temp15ETL, Temp16ETL, Temp17ETL, Temp18ETL, Temp19ETL, Temp20ETL, LowVoltage1ETL, Current1ETL, LowVoltage2ETL, Current2ETL, LowVoltage3ETL, Current3ETL = gt.ConvertEnv(ETLTimestamp)

		##### These fields are uploaded to AirTable. The field names and types must match exactly the names in the table. 
		this_run_info["Run number"]=RunNumber
		this_run_info["Configuration"]=ConfigID
		this_run_info["Start time"]=str(SpillTime)
		this_run_info["Duration"]=str(Duration)

		gt.GetTemperaturesSimple(this_run_info)
		gt.GetCAENInfoSimple(this_run_info)
		gt.GetACNetYield(this_run_info)

		this_run_info["Digitizer"]=DigiListThisRun

		pf.NewRunRecordSimple(this_run_info,ConfigID, False, key)
		

		##### These fields are NOT added to airtable, but saved for post processing

		this_run_info["Configuration"]=Configuration
		this_run_info.update(simpleLecroyDict)
		this_run_info.update(simpleCAENDict)

		runLogFileName = LocalConfigPath+"/Runs/info_%i.json"%RunNumber

		a_file = open(runLogFileName, "w")
		js.dump(this_run_info, a_file)
		a_file.close()


		#################################################
		#Check for Stop signal in AutoPilot.status file
		#################################################
		tmpStatusFile = open("AutoPilot.status","r") 
		tmpString = (tmpStatusFile.read().split())[0]
		if (tmpString == "STOP" or tmpString == "stop"):
			print "Detected stop signal.\nStopping AutoPilot...\n\n"
			AutoPilotStatus = 0
		tmpStatusFile.close()
	iteration += 1
