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

parser = argparse.ArgumentParser(description='Information for running the AutoPilot program. /n /n General Instructions: If using OTSDAQ make sure the start and stop seconds in the beginning of the program are hard coded correctly. /n Make sure to add sensor and configuration after each controlled access and pass it as an argument to this script. /n/n /n TekScope Specific Instructions: /n Make sure you hard code the dpo_fastframe path. /n If using the OTSDAQ with TekScope make sure the Use_otsdaq boolean is True in dpo_fastframe script. /n Make Sure you pass all four Scope trigger and channel settings. /n /n Other Digitizer Specific Instructions: /n If not running the TekScope make sure that the run file name in TCP_com is correct.')
parser.add_argument('-rtm', '--RunTableMode', type=int, default = 1, help='Give 1 if you are using the run table', required=False)
parser.add_argument('-ac', '--AlreadyConfigured', type=int, default = 0, help='Give 1 if the OTSDAQ is already configured', required=False)
parser.add_argument('-de', '--Debug', type=int, default = 0, required=False)
parser.add_argument('-io', '--IsOTSDAQ', type=int, default=0, help = 'Give 1 if using OTSDAQ',required=False)
parser.add_argument('-it', '--IsTelescope', type=int,default=0, help = 'Give 1 if using the telescope',required=False)
parser.add_argument('-di', '--Digitizer', type=str,default= 'TekScope', help = 'Give VME or DT5742 or TekScope', required =False)
parser.add_argument('-se', '--Sensor', type=int, help = 'Make sure to add the sensor record in the run table. Give sensor S/N from the run table',required=False)
parser.add_argument('-conf', '--Configuration', type=int, help = 'Make sure to add the configuration in the run table. Give COnfiguration S/N from the run table',required=False)
parser.add_argument('-sac', '--StopAndContinue', type=int, default = 0, help = 'This bool should be 1 if the OTSDAQ is already in the running state and you want to stop and it and continue running it.',required=False)

############################## Digitizers ##################################
parser.add_argument('-iv', '--IsVME', type=int, default = 0, help = 'Give 1 if using VME, 0 otherwise.', required =False)
parser.add_argument('-is', '--IsSampic', type=int, default = 0, help = 'Give 1 if using Sampic, 0 otherwise.', required =False)
parser.add_argument('-its', '--IsTekScope', type=int, default = 0, help = 'Give 1 if using TekScope, 0 otherwise.', required =False)
parser.add_argument('-iks', '--IsKeySightScope', type=int, default = 0, help = 'Give 1 if using KeySightScope, 0 otherwise.', required =False)
parser.add_argument('-idt', '--IsDT5742', type=int, default = 0, help = 'Give 1 if using DT5742, 0 otherwise.', required =False)

######################### Only care about this if using TekScope #########################
parser.add_argument('-tl', '--TriggerLevel', type=float,default= -0.01, help = 'Trigger level in volts', required =False)
parser.add_argument('-tc', '--TriggerChannel', type=str, default= 'CH4', help = 'Channel to trigger on',required=False)
parser.add_argument('-ne', '--NumEvents', type=int,default=50000, help = 'Number of events',required=False)
parser.add_argument('-tne', '--TotalNumEvents', type=int,default=50000, help = 'Total number of events',required=False)

args = parser.parse_args()
RunTableMode = args.RunTableMode
AlreadyConfigured = args.AlreadyConfigured
Debug = args.Debug
IsOTS = args.IsOTSDAQ
IsTelescope = args.IsTelescope
Digitizer = args.Digitizer
Sensor = args.Sensor
Configuration = args.Configuration
StopAndContinue = args.StopAndContinue
TriggerLevel = args.TriggerLevel
TriggerChannel = args.TriggerChannel
NumEvents = args.NumEvents
TotalNumEvents = args.TotalNumEvents
IsSampic = args.IsSampic
IsVME = args.IsVME
IsTekScope = args.IsTekScope
IsKeySightScope = args.IsKeySightScope
IsDT5742 = args.IsDT5742


########################### Only when Run table is used ############################
DigitizerList = []
StartTekCMD = "python %s --trig=%f --trigCh=%s --numFrames=%i --totalNumber=%i" % (DPOFastFramePath, TriggerLevel, TriggerChannel, NumEvents, TotalNumEvents)
StartKeySightCMD = "python %s --trig=%f --trigCh=%s --numFrames=%i --totalNumber=%i" % (DPOFastFramePath, TriggerLevel, TriggerChannel, NumEvents, TotalNumEvents)
StartSampicCMD = "python %s --trig=%f --trigCh=%s --numFrames=%i --totalNumber=%i" % (DPOFastFramePath, TriggerLevel, TriggerChannel, NumEvents, TotalNumEvents)

if IsTekScope or IsSampic or IsKeySightScope:
    IsScope = True
else:
    IsScope = False

if RunTableMode:

        if IsTelescope:
                Tracking = 'Not started'
        else:
                Tracking = 'N/A'
        if IsVME:
            TimingDAQVME = 'Not started'
            TimingDAQNoTracksVME = 'Not started'
            DigitizerList.append('VME')
        else:
            TimingDAQVME = 'N/A'
            TimingDAQNoTracksVME = 'N/A'

        if IsDT5742:
            TimingDAQDT5742 = 'Not started'
            TimingDAQNoTracksDT5742 = 'Not started'
            DigitizerList.append('DT5742')
        else:
            TimingDAQDT5742 = 'Not started'
            TimingDAQNoTracksDT5742 = 'Not started'

        if IsTekScope:
            ConversionTekScope = 'Not started'
            TimingDAQTekScope = 'Not started'
            TimingDAQNoTracksTekScope = 'Not started'
            DigitizerList.append('TekScope')
        else:
            ConversionTekScope = 'N/A'
            TimingDAQTekScope = 'N/A'
            TimingDAQNoTracksTekScope = 'N/A'

        if IsKeySightScope:
            ConversionKeySightScope = 'Not started'
            TimingDAQKeySightScope = 'Not started'
            TimingDAQNoTracksKeySightScope = 'Not started'
            DigitizerList.append('KeySightScope')
        else:
            ConversionKeySightScope = 'N/A'
            TimingDAQKeySightScope = 'N/A'
            TimingDAQNoTracksKeySightScope = 'N/A'

        if IsSampic:
            ConversionSampic = 'Not started'
            TimingDAQSampic = 'Not started'
            TimingDAQNoTracksSampic = 'Not started'
            DigitizerList.append('Sampic')
        else:
            ConversionSampic = 'N/A'
            TimingDAQSampic = 'N/A'
            TimingDAQNoTracksSampic = 'N/A'

    # Get Sensor ID and Configuration ID list
        if pf.QueryGreenSignal(True):
            SensorID = pf.GetFieldIDOtherTable('Sensor', 'Configuration number', str(Sensor), False)
            ConfigID = pf.GetFieldIDOtherTable('Config', 'Configuration number', str(Configuration), False)

        if not SensorID or not ConfigID:
            raise Exception('\n The sensor and configuration you passed as argument are not in the table!!!!!!!!!!!!!!!!!!!! \n')
            ##### Exit the program ######


#################### CONFIGURING AND INITIALIZING THE OTSDAQ ######################

if not Debug and not AlreadyConfigured and not StopAndContinue and IsOTS:
    print 'INTITIALIZING THE OTS-DAQ'
    tp.init_ots()

if not Debug and not AlreadyConfigured and not StopAndContinue and IsOTS:
    print 'CONFIGURING THE OTS-DAQ'
    tp.config_ots()
    time.sleep(25)



while True:

        if not IsScope and IsOTS and StopAndContinue:

                ############### Wait until stop time ##################
                wait_until(StopSeconds)
                print "Stopping run at %s" % (datetime.now().time())
                if not Debug: tp.stop_ots(False)
                StopAndContinue = False
                time.sleep(20)

        elif not StopAndContinue:

                ############ Wait for safe time to start run ##########
                wait_until(StartSeconds)

                if not Debug and IsScope:

                        if ScopeState() == 'ready': 
                           ScopeStatusAutoPilot()
                        # In case of the scope, running the dpo_fastframe script which will take care of the otsdaq.
                           os.system(StartScopeCMD)
                           time.sleep(1)

                elif not IsScope:

                        ################### Starting the run ###################
                        StartTime = datetime.now()
                        print "Starting run at %s" % (StartTime)

                        RunNumber = tp.start_ots(False)

                        time.sleep(60*(NumSpillsPerRun-1))

                        wait_until(StopSeconds)
                        StopTime = datetime.now()

                        print "Stopping run at %s" % (StopTime)
                        if not Debug: tp.stop_ots(False)

                        if RunTableMode:

                                Duration = (StopTime - StartTime).total_seconds()

                                if pf.QueryGreenSignal(True): pf.NewRunRecord(RunNumber, StartTime, str(Duration), DigitizerList, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, SensorID, ConfigID, False)
