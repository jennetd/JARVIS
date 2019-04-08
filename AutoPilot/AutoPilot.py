import sys 
sys.path.append('/home/daq/JarvisDevelopment/BackEndProcesses/')
import ParseFunctions as pf
import TCP_com as tp  #in-built 5s delay in all of them
from AllModules import *

################################### Important #########################################
######## This parameter defines at what time it is safe to start a new run ############
######## It should be about 30 seconds before the arrival time of each spill ##########
######## Since spills come every minute, this is defined as a number of seconds #######
######## after the start of each clock minute (only meaningful modulo 60 seconds) #####
################ Periodically make sure this value makes sense. #######################
#######################################################################################

StartSeconds = 9
StopSeconds = 40
NumSpillsPerRun = 1

#################################Parsing arguments######################################

parser = argparse.ArgumentParser(description='Information for running the AutoPilot program. /n /n General Instructions: Start OTSDAQ and Configure by hand. If using OTSDAQ make sure the start and stop seconds in the beginning of the program are hard coded correctly. /n Make sure to add sensor and configuration after each controlled access and pass it as an argument to this script. /n/n /n TekScope Specific Instructions: /n Make sure you hard code the dpo_fastframe path. /n If using the OTSDAQ with TekScope make sure the Use_otsdaq boolean is True in dpo_fastframe script. /n Make Sure you pass all four Scope trigger and channel settings. /n /n Other Digitizer Specific Instructions: /n If not running the TekScope make sure that the run file name in TCP_com is correct.')
parser.add_argument('-de', '--Debug', type=int, default = 0, required=False)
parser.add_argument('-it', '--IsTelescope', type=int,default=1, help = 'Give 1 if using the telescope',required=False)
parser.add_argument('-conf', '--Configuration', type=int, help = 'Make sure to add the configuration in the run table. Give COnfiguration S/N from the run table',required=False)
parser.add_argument('-se', '--Sensor', type=int, help = 'Make sure to add the sensor record in the run table. Give sensor S/N from the run table',required=False)

args = parser.parse_args()
Debug = args.Debug
IsTelescope = args.IsTelescope
Configuration = args.Configuration
Sensor = args.Sensor

########################### Only when Run table is used ############################

############ Getting the digitizer list from the configuration table #############
DigitizerList = GetDigiFromConfig(Configuration, False)

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
	TimingDAQVME = 'Not started'
	TimingDAQNoTracksVME = 'Not started'
else:
	TimingDAQVME = 'N/A'
	TimingDAQNoTracksVME = 'N/A'

if DigitizerDict[1] in DigitizerList:
	TimingDAQDT5742 = 'Not started'
	TimingDAQNoTracksDT5742 = 'Not started'
else:
	TimingDAQDT5742 = 'Not started'
	TimingDAQNoTracksDT5742 = 'Not started'

if DigitizerDict[2] in DigitizerList:
	ConversionTekScope = 'Not started'
	TimingDAQTekScope = 'Not started'
	TimingDAQNoTracksTekScope = 'Not started'
else:
	ConversionTekScope = 'N/A'
	TimingDAQTekScope = 'N/A'
	TimingDAQNoTracksTekScope = 'N/A'

if DigitizerDict[3] in DigitizerList:
	ConversionKeySightScope = 'Not started'
	TimingDAQKeySightScope = 'Not started'
	TimingDAQNoTracksKeySightScope = 'Not started'
else:
	ConversionKeySightScope = 'N/A'
	TimingDAQKeySightScope = 'N/A'
	TimingDAQNoTracksKeySightScope = 'N/A'

if DigitizerDict[4] in DigitizerList:
	ConversionSampic = 'Not started'
	TimingDAQSampic = 'Not started'
	TimingDAQNoTracksSampic = 'Not started'
else:
	ConversionSampic = 'N/A'
	TimingDAQSampic = 'N/A'
	TimingDAQNoTracksSampic = 'N/A'

# Get Sensor ID and Configuration ID list

if pf.QueryGreenSignal(True):
	SensorID = pf.GetFieldIDOtherTable('Sensor', 'Configuration number', str(Sensor), False)
	ConfigID = pf.GetFieldIDOtherTable('Config', 'Configuration number', str(Configuration), False)

if not ConfigID: #not SensorID or 
	raise Exception('\n The sensor and configuration you passed as argument are not in the table!!!!!!!!!!!!!!!!!!!! \n')
	##### Exit the program ######

# Use Status file to tell autopilot when to stop.
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
print "Sensor Configuration : ", Sensor

if IsTelescope:
        print "Tracking Telescope Included"
if IsSampic:
        print "SAMPIC readout Included"
if IsVME:
        print "VME readout Included" 
if (IsDT5742):
        print "DT5742 DRS Desktop Digitizer readout Included"
if (IsTekScope):
        print "Tektronix Scope readout Included"
if (IsKeySightScope):
        print "Keysight Scope readout Included"
print ""
print ""
print "*********************************************************************"
print ""
print ""



while (AutoPilotStatus == 1):

	##sync local run number file with ftbf-daq-08
	tp.GetRunFile()
	time.sleep(5)
	RunNumber = tp.GetRunNumber()
	print "Starting Run %i " % (RunNumber)
        print ""
	############ Wait for safe time to start run ##########


	ScopeIncludedThisRun = False

	if IsScope:
		currentScopeState = ScopeState() 
		if currentScopeState == 'ready': 
		   print("Sending start command to scope.")
		   if not Debug:
			   ScopeStatusAutoPilot()
			   ScopeIncludedThisRun = True
			   WaitForScopeStart()
		   print("Scope has started.")
                else:
                   print("Scope still busy. Excluding scope from the next run\n")

	wait_until(StartSeconds)
	tp.UpdateRunNumber(RunNumber+1) ##must be called after scope start.
	tp.SendRunFile()

	################### Starting the run ###################
	StartTime = datetime.now()  
	print "\nRun %i started at %s" % (RunNumber,StartTime)
        print ""
	if not Debug: tp.start_ots(False)

	## Minimum run duration
	time.sleep(60*(NumSpillsPerRun-1))

	### Don't stop run until scope has acquired all events (OK if still writing events disk, though)
	if IsScope and ScopeIncludedThisRun:
		WaitForScopeFinishAcquisition()
		
	wait_until(StopSeconds)
	if not Debug: tp.stop_ots(False)

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
			if "KeySightScope" in DigiListThisRun: DigiListThisRun.remove("KeySightScope")

		pf.NewRunRecord(RunNumber, StartTime, str(Duration), DigiListThisRun, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, SensorID, ConfigID, False)
		
        
        #################################################
        #Check for Stop signal in AutoPilot.status file
        #################################################
        tmpStatusFile = open("AutoPilot.status","r") 
        tmpString = (tmpStatusFile.read().split())[0]
        if (tmpString == "STOP" or tmpString == "stop"):
                print "Detected stop signal.\n Stopping AutoPilot...\n\n"
                AutoPilotStatus = 0

