#!/bin/env python
import sys 
sys.path.append('../BackEndProcesses/')
import ParseFunctions as pf
import TCP_com as tp  #in-built 5s delay in all of them
from AllModules import *
import GetTemp as gt

################################### Important #########################################
######## This parameter defines at what time it is safe to start a new run ############
######## It should be about 30 seconds before the arrival time of each spill ##########
######## Since spills come every minute, this is defined as a number of seconds #######
######## after the start of each clock minute (only meaningful modulo 60 seconds) #####
################ Periodically make sure this value makes sense. #######################
#######################################################################################

NumSpillsPerRun = 1
RP = False #### It needs to be true if you want to get files from Raspberry Pi, otherwise it would give default values. 
BTLLogging = False
ETLTemp = True
ETROC=False

ETROC_config_filename = "/home/daq/RaspberryPi/scriptsPC/config.txt"
ETROC_baseline_filename = "/home/daq/RaspberryPi/scriptsPC/baseline.txt"

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


#IsScope is used to check whether the run configuration includes the Keysight or Tektronix scope
if DigitizerDict[2] in DigitizerList or DigitizerDict[3] in DigitizerList:
	IsScope = True
else:
	IsScope = False

############ Initialize progress fields on run table ################
if IsTelescope:
	Tracking = 'Not started'
else:
	Tracking = 'N/A'

if DigitizerDict[0] in DigitizerList:
	if IsTelescope:
		TimingDAQVME = 'Not started'
	else:
		TimingDAQVME = 'N/A'
	TimingDAQNoTracksVME = 'Not started'
	LabviewRecoVME = 'Not started'
	IncludesVME = True
else:
	TimingDAQVME = 'N/A'
	TimingDAQNoTracksVME = 'N/A'
	LabviewRecoVME = 'N/A'
	IncludesVME = False

if DigitizerDict[1] in DigitizerList:
	if IsTelescope:
		TimingDAQDT5742 = 'Not started'
	else:
		TimingDAQDT5742 = 'N/A'
	TimingDAQNoTracksDT5742 = 'Not started'
	LabviewRecoDT5742 = 'Not started'
	IncludesDT5742 = True
else:
	TimingDAQDT5742 = 'N/A'
	TimingDAQNoTracksDT5742 = 'N/A'
	LabviewRecoDT5742 = 'N/A'
	IncludesDT5742 = False

if DigitizerDict[2] in DigitizerList:
	ConversionTekScope = 'Not started'
	TimingDAQTekScope = 'Not started'
	TimingDAQNoTracksTekScope = 'Not started'
	LabviewRecoTekScope = 'Not started'
	IncludesTekScope = True
else:
	ConversionTekScope = 'N/A'
	TimingDAQTekScope = 'N/A'
	TimingDAQNoTracksTekScope = 'N/A'
	LabviewRecoTekScope = 'N/A'
	IncludesTekScope = False

if DigitizerDict[3] in DigitizerList:
	ConversionKeySightScope = 'Not started'
	if IsTelescope:
		TimingDAQKeySightScope = 'Not started'
	else:
		TimingDAQKeySightScope = 'N/A'
	TimingDAQNoTracksKeySightScope = 'Not started'
	LabviewRecoKeySightScope = 'Not started'
	IncludesKeySightScope = True
else:
	ConversionKeySightScope = 'N/A'
	TimingDAQKeySightScope = 'N/A'
	TimingDAQNoTracksKeySightScope = 'N/A'
	LabviewRecoKeySightScope = 'N/A'
	IncludesKeySightScope = False

if DigitizerDict[4] in DigitizerList:
	ConversionSampic = 'Not started'
	TimingDAQSampic = 'Not started'
	TimingDAQNoTracksSampic = 'Not started'
	LabviewRecoSampic = 'Not started'
	IncludesSampic = True
else:
	ConversionSampic = 'N/A'
	TimingDAQSampic = 'N/A'
	TimingDAQNoTracksSampic = 'N/A'
	LabviewRecoSampic = 'N/A'
	IncludesSampic = False

if DigitizerDict[5] in DigitizerList:
	if IsTelescope:
		TimingDAQTOFHIR = 'Not started'
	else:
		TimingDAQTOFHIR = 'N/A'
	TimingDAQNoTracksTOFHIR = 'Not started'
	IncludesTOFHIR = True
else:
	TimingDAQTOFHIR = 'N/A'
	TimingDAQNoTracksTOFHIR = 'N/A'
	IncludesTOFHIR = False

if DigitizerDict[6] in DigitizerList:
	ConversionLecroyScope = 'Not started'
	if IsTelescope:
		TimingDAQLecroyScope = 'Not started'
	else:
		TimingDAQLecroyScope = 'N/A'
	TimingDAQNoTracksLecroyScope = 'Not started'
	LabviewRecoLecroyScope = 'Not started'
	IncludesLecroyScope = True
else:
	ConversionLecroyScope = 'N/A'
	TimingDAQLecroyScope = 'N/A'
	TimingDAQNoTracksLecroyScope = 'N/A'
	LabviewRecoLecroyScope = 'N/A'
	IncludesLecroyScope = False


# Get Sensor ID and Configuration ID list
if pf.QueryGreenSignal(True):
	ConfigID = pf.GetFieldIDOtherTable('Config', 'Configuration number', str(Configuration), False, key)

if not ConfigID: #not SensorID or 
	raise Exception('\n The sensor and configuration you passed as argument are not in the table!!!!!!!!!!!!!!!!!!!! \n')
	##### Exit the program ######

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
if IncludesSampic:
	print "SAMPIC readout Included"
if IncludesVME:
	print "VME readout Included" 
if IncludesTOFHIR:
	print "TOFHIR readout Included" 
if (IncludesDT5742):
	print "DT5742 DRS Desktop Digitizer readout Included"
if (IncludesTekScope):
	print "Tektronix Scope readout Included"
if (IncludesKeySightScope):
	print "Keysight Scope readout Included"
if (IncludesLecroyScope):
	print "Lecroy Scope readout Included"
print ""
print ""
print "*********************************************************************"
print ""
print ""

ETROC_config = "N/A"
ETROC_baseline = "N/A"
# Get Start and stop seconds for the first iteration of the loop
iteration = 0
if RP: tp.RPGlobalComm("GlobalStart")
while (AutoPilotStatus == 1 and iteration < maxRuns):

	if iteration % 5 == 0:
		if IsTelescope: StartSeconds,StopSeconds = GetStartAndStopSeconds(36, 22) #33,22
		else: StartSeconds,StopSeconds = GetStartAndStopSeconds(50, 22)
		print StartSeconds, StopSeconds

	## Refresh this
	DigitizerList = pf.GetDigiFromConfig(Configuration, False, key)

	##sync local run number file with ftbf-daq-08
	tp.GetRunFile()
	time.sleep(5)
	RunNumber = tp.GetRunNumber()
	print "Next Run %i " % (RunNumber)
	print ""
	if ETROC:
		ETROC_baseline_file =  open(ETROC_baseline_filename, "r")
		ETROC_baseline = str(ETROC_baseline_file.read().strip())
		print "ETROC0 baseline: %s"%ETROC_baseline
		ETROC_config_file =  open(ETROC_config_filename, "r")
		ETROC_config = str(ETROC_config_file.read().strip())
		print "ETROC0 configuration: %s"%ETROC_config

	############ Wait for safe time to start run ##########
	wait_until(StartSeconds)

        
	ScopeIncludedThisRun = False
	if IsScope:
		currentScopeState = ScopeState()
		if currentScopeState == 'busy':
			print "[WARNING] : Scope is still acquiring events, but autopilot is ready to start a new run. Likely someone killed a run prematurely. Tracking for scope in previous run is screwed up." 


#### need to check both scopes before continue command
		if currentScopeState == 'ready': 
			print("\n Sending start command to scope.\n")
			if not Debug:
				ScopeStatusAutoPilot(RunNumber)
				ScopeIncludedThisRun = True
				WaitForScopeStart()
			print("Scope has started.")
		else:
			# print("Scope still busy. Excluding scope from the next run\n")
			print("Scope still busy. Wait for next chance.\n")
			continue


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



	tp.UpdateRunNumber(RunNumber+1) ##must be called after scope start.
	tp.SendRunFile()
	print "Is Scope ",IsScope
	print "Keysight/Tek Scope included ",ScopeIncludedThisRun
	print "Lecroy Scope included ",LecroyScopeIncludedThisRun
	################### Starting the run ###################
	StartTime = datetime.now()  
	print "\nRun %i started at %s" % (RunNumber,StartTime)
	print ""
	if RP: tp.RPComm(RunNumber, "start") 

	#Start the run here
	if not Debug and IsTelescope: tp.start_ots(RunNumber,False)
	if DigitizerDict[5] in DigitizerList:
        ###############################################################
        #Archive the Config for the TOFHIR if it's a new configuration
        ###############################################################
		if (not os.path.exists(BaseTestbeamDir+"/TOFHIR/Config/config.ini")):
			print ("TOFHIR Config directory at " + BaseTestbeamDir+"/TOFHIR/Config/ has not been properly mounted. Please mount it.")
			sys.exit(0)
		if (not os.path.exists(BaseTestbeamDir+"/TOFHIR/ConfigArchive/Config_v" + str(Configuration))):
			print ("Current Configuration is v" + str(Configuration) + ". TOFHIR Config directory for this configuration has not been archived. Archiving it now.")
			os.system("cp -rv "+BaseTestbeamDir+"/TOFHIR/Config/ "+BaseTestbeamDir+"/TOFHIR/ConfigArchive/Config_v"+str(Configuration))
		else :
			print ("Current Configuration is v" + str(Configuration) + ". TOFHIR Config directory for this configuration is already archived")

	## Minimum run duration
	time.sleep(60*(NumSpillsPerRun-1))

	### Don't stop run until scope has acquired all events (OK if still writing events disk, though)
	scope_finished=0

	if ((IsScope and ScopeIncludedThisRun) or (IncludesLecroyScope and LecroyScopeIncludedThisRun)):
		time.sleep(15)
				
	if IsScope and ScopeIncludedThisRun:		
		print "Waiting for Keysight/Tek scope to finish"
		WaitForScopeFinishAcquisition()
		scope_finished=time.time()
		print "Keysight/Tek scope finished"
		
	if IncludesLecroyScope and LecroyScopeIncludedThisRun:		
		print "Waiting for Lecroy scope to finish"
		WaitForLecroyScopeFinishAcquisition()
		scope_finished=time.time()
		print "Lecroy scope finished"

		
	print "Waiting for TClock stop time (%0.1f)"%StopSeconds
	wait_until(StopSeconds)
	tclock_finished=time.time()



	if not Debug and IsTelescope: tp.stop_ots(False)

	if RP: tp.RPComm(RunNumber, "stop")
	print ("%0.1f seconds between scope finish and TClock time" % (tclock_finished-scope_finished))
	StopTime = datetime.now()
	print "\nRun %i stopped at %s" % (RunNumber,StopTime)
	print ""
	print "*********************************************************************"
	print ""

	Duration = int((StopTime - StartTime).total_seconds())

	if pf.QueryGreenSignal(True): 
		DigiListThisRun = DigitizerList
		if not ScopeIncludedThisRun:
			if "TekScope" in DigiListThisRun: DigiListThisRun.remove("TekScope")
			if "KeySightScope" in DigiListThisRun: 
				DigiListThisRun.remove("KeySightScope")

			TimingDAQKeySightScope = 'N/A'
			TimingDAQNoTracksKeySightScope = 'N/A'
			LabviewRecoKeySightScope = 'N/A'
			ConversionKeySightScope = 'N/A'
			xrdcpRawKeySightScope = 'N/A'			

		else:			
			xrdcpRawKeySightScope = 'Not started'
			ConversionKeySightScope = 'Not started'
			TimingDAQKeySightScope = 'Not started'
			TimingDAQNoTracksKeySightScope = 'Not started'
			LabviewRecoKeySightScope = 'Not started'
		

		if not LecroyScopeIncludedThisRun:
			if "LecroyScope" in DigiListThisRun: 
				DigiListThisRun.remove("LecroyScope")

			TimingDAQLecroyScope = 'N/A'
			TimingDAQNoTracksLecroyScope = 'N/A'
			LabviewRecoLecroyScope = 'N/A'
			ConversionLecroyScope = 'N/A'
			xrdcpRawLecroyScope = 'N/A'
		else:
			TimingDAQLecroyScope = 'Not started'
			TimingDAQNoTracksLecroyScope = 'Not started'
			LabviewRecoLecroyScope = 'Not started'
			ConversionLecroyScope = 'Not started'
			xrdcpRawLecroyScope = 'Not started'


		######If the scope is included It's gonna update this field to "Not Started" in scope listener script
		# Get Raspberry Pi Value list, Make sure raspberry pi rsync is on, If it is not then the readRPFile function takes care of that.

		BoxTemp, x_stage, y_stage, BoxVoltage, BarCurrent, z_rotation, BoxHum, BoxCurrent, BarVoltage  = ReadRPFile(RunNumber)
		
		if DigitizerDict[5] in DigitizerList:
			OverVoltageBTL, VTHBTL  = BTLLoggingFile()
		else:
			OverVoltageBTL = "N/A"
			VTHBTL = "N/A"

		SpillTime = (StartTime+timedelta(0,27)).strftime("%Y-%m-%d %H:%M:%S")
		if ETLTemp:
			# Get ETL environment data
			ETLTimestamp = (datetime.now() - datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")).total_seconds() #- 3600 ### For daylight saving time 
			print 'Getting ETL environmental data'
			# Temp13ETL, Temp14ETL, Temp15ETL, Temp16ETL, Temp17ETL, Temp18ETL, Temp19ETL, Temp20ETL, LowVoltage1ETL, Current1ETL, LowVoltage2ETL, Current2ETL, LowVoltage3ETL, Current3ETL = gt.ConvertEnv(ETLTimestamp)
			Temp13ETL =0
			Temp14ETL=0
			Temp15ETL=0
			Temp16ETL=0
			Temp17ETL=0
			Temp18ETL=0
			Temp19ETL=0
			Temp20ETL=0
			LowVoltage1ETL=0
			Current1ETL=0
			LowVoltage2ETL=0
			Current2ETL=0
			LowVoltage3ETL=0
			Current3ETL =0
			print 'Updating the run table'
			print Temp13ETL, Temp14ETL, Temp15ETL, Temp16ETL, Temp17ETL, Temp18ETL, Temp19ETL, Temp20ETL, LowVoltage1ETL, Current1ETL, LowVoltage2ETL, Current2ETL, LowVoltage3ETL, Current3ETL
			pf.NewRunRecord4(RunNumber, SpillTime, str(Duration), DigiListThisRun, Tracking, ConversionSampic, ConversionTekScope,ETROC_baseline,ETROC_config, xrdcpRawKeySightScope, xrdcpRawLecroyScope,ConversionKeySightScope,ConversionLecroyScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQLecroyScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope,  TimingDAQNoTracksLecroyScope, TimingDAQNoTracksDT5742, LabviewRecoVME, LabviewRecoDT5742, LabviewRecoKeySightScope, LabviewRecoSampic, LabviewRecoTekScope, BoxTemp, x_stage, y_stage, BoxVoltage, BarCurrent, z_rotation, BoxHum, BoxCurrent, BarVoltage, str(Temp13ETL), str(Temp14ETL), str(Temp15ETL), str(Temp16ETL), str(Temp17ETL), str(Temp18ETL), str(Temp19ETL), str(Temp20ETL), str(LowVoltage1ETL), str(Current1ETL), str(LowVoltage2ETL), str(Current2ETL), str(LowVoltage3ETL), str(Current3ETL), ConfigID, False, key)
			
		else:
			print 'Updating the run table'
			#print RunNumber, StartTime, str(Duration), DigiListThisRun, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQTOFHIR, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, TimingDAQNoTracksTOFHIR, LabviewRecoVME, LabviewRecoDT5742, LabviewRecoKeySightScope, LabviewRecoSampic, LabviewRecoTekScope, BoxTemp, x_stage, y_stage, BoxVoltage, BarCurrent, z_rotation, BoxHum, BoxCurrent, BarVoltage, ConfigID, key
			pf.NewRunRecord2(RunNumber, StartTime, str(Duration), DigiListThisRun, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQTOFHIR, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, TimingDAQNoTracksTOFHIR, LabviewRecoVME, LabviewRecoDT5742, LabviewRecoKeySightScope, LabviewRecoSampic, LabviewRecoTekScope, BoxTemp, x_stage, y_stage, BoxVoltage, BarCurrent, z_rotation, BoxHum, BoxCurrent, BarVoltage, OverVoltageBTL, VTHBTL, ConfigID, True, key)

		#pf.NewRunRecord(RunNumber, StartTime, str(Duration), DigiListThisRun, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, LabviewRecoVME, LabviewRecoDT5742, LabviewRecoKeySightScope, LabviewRecoSampic, LabviewRecoTekScope, ConfigID, False, key)

		#################################################
		#Check for Stop signal in AutoPilot.status file
		#################################################
		tmpStatusFile = open("AutoPilot.status","r") 
		tmpString = (tmpStatusFile.read().split())[0]
		if (tmpString == "STOP" or tmpString == "stop"):
			print "Detected stop signal.\nStopping AutoPilot...\n\n"
			AutoPilotStatus = 0
			if RP: tp.RPGlobalComm("GlobalStop")
		tmpStatusFile.close()
	iteration += 1
