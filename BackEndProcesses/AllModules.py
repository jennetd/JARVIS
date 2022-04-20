import requests
import ast
from datetime import datetime
from datetime import timedelta
import time
import numpy as np
import getpass
import os
import subprocess as sp
import socket
import sys
import glob
import subprocess
from subprocess import Popen, PIPE
import pipes
from pipes import quote
import argparse

#############################################################
#Define User and Host
#############################################################
user, isLPC = 'daq', False
try:
    user = os.environ['USER']
    isLPC = 'cmslpc' in os.environ['HOSTNAME'] 
except:
    print "Failed to find environment"
if isLPC:
    print "Found user: {} Running on LPC: {}".format(user, isLPC)

################### Run Table Information #################
MyKey = '' #Read MyKey from key file in RecoProcesses
RunTableName = 'tbll6K78TBGoYB35V'
SensorTableName = 'tbljWMYw2M2mfPXFs'
ConfigTableName = 'tblyMhEwAFj8QMqLH'
KeySightScopeConfigTableName = 'tblNzWILNh3wUPkBj'
LecroyScopeConfigTableName = 'tbl6HZPEwx0LLlbEq'
CAENConfigTableName = 'tblCFsUFHRjv8YOxk'

BaseID = 'appWaxhQY77bbVCsV'
CurlBaseCommandWithoutTable = 'https://api.airtable.com/v0/%s' % (BaseID)
CurlBaseCommand = 'https://api.airtable.com/v0/%s/%s' % (BaseID, RunTableName)
CurlBaseCommandSensor = 'https://api.airtable.com/v0/%s/%s' % (BaseID, SensorTableName)
CurlBaseCommandConfig = 'https://api.airtable.com/v0/%s/%s' % (BaseID, ConfigTableName)
CurlBaseCommandKeySight = 'https://api.airtable.com/v0/%s/%s' % (BaseID, KeySightScopeConfigTableName)
CurlBaseCommandLecroy = 'https://api.airtable.com/v0/%s/%s' % (BaseID, LecroyScopeConfigTableName)
CurlBaseCommandCAEN = 'https://api.airtable.com/v0/%s/%s' % (BaseID, CAENConfigTableName)
CurlBaseCommandRunTable = 'https://api.airtable.com/v0/%s/%s' % (BaseID, RunTableName)
QueryFilePath ="../QueryLog.txt" # Don't care about this

#############################################################
################## Hard Code these paths ####################
#############################################################

############# Tracking Paths ##############
# HyperscriptPath = '/home/otsdaq/CMSTiming/HyperScriptFastTrigger_NewGeo_2020_02_05.sh'

# HyperscriptPath = '/home/otsdaq/CMSTiming/HyperScriptETL2021.sh'
HyperscriptPath = '/home/otsdaq/CMSTiming/HyperScript2022.sh'
# HyperscriptPath = '/home/otsdaq/CMSTiming/HyperScriptETL2020_TI.sh'
 
#HyperscriptPath = '/home/otsdaq/CMSTiming/HyperScriptFastTriggerETL2020.sh'

RulinuxSSH = 'otsdaq@teddy01.dhcp.fnal.gov'#'otsdaq@rulinux04.dhcp.fnal.gov'
BaseTrackDirRulinux = '/data/TestBeam/2020_02_February_cmstiming/'
ResultTrackFileNameBeforeRunNumber = 'Run' ###########'Run%d_CMSTiming_converted.root'
ResultTrackFileNameAfterRunNumber = '_CMSTiming_converted.root' 
ResultTrackFileNameAfterRunNumberSlow = '_CMSTiming_SlowTriggerStream_converted.root'
ResultTrackFileNameAfterRunNumberFast = '_CMSTiming_FastTriggerStream_converted.root'

############## For timingdaq02 ############
BaseTestbeamDir = '/home/daq/SensorBeam2022/' 
if isLPC:
    if 'rheller' in user:
        BaseTestbeamDir = '/uscms/home/rheller/nobackup/SensorBeam2022/'
    elif 'cmadrid' in user:
        BaseTestbeamDir = '/uscms/home/cmadrid/nobackup/ana/SensorBeam2022/'
    else:
        raise ValueError("\"{}\" please define your code path above for the lpc in JARVIS/BackEndProcesses/AllModules.py".format(user))

eosBaseDir = 'root://cmseos.fnal.gov//store/group/cmstestbeam/SensorBeam2022/'
BaseTrackDirLocal = '%sTracks/v10/' % BaseTestbeamDir
LocalSSH = 'daq@timingdaq01.dhcp.fnal.gov'
EnvSetupPath = '/home/daq/setup.sh' ############### Remember to change ProcessExec accordingly
EnvSetupPath2 = '/home/daq/otsdaq/setup_ots.sh' ############### Remember to change ProcessExec accordingly
TimingDAQDir = '%sTimingDAQ/'%BaseTestbeamDir
#TimingDAQDir = '/home/daq/LecroyControl/HitCounter/' ### HACK FOR LONG ACQ
CondorDir = '%sCondor/'%BaseTestbeamDir
TOFHIRRecoDir = '/uscms/home/rheller/nobackup/sw_daq_tofhir_v1/build/'
TOFHIRConfigDir = '/uscms/home/rheller/nobackup/2019_04_April_CMSTiming/TOFHIR/ConfigArchive/'
TOFHIRRecoDir2 = '/uscms/home/rheller/nobackup/sw_daq_tofhir_v1/DAQReco/'
LocalConfigPath = '%sConfigInfo/'%BaseTestbeamDir


############## For PCCITFNAL01 ############
#BaseTestbeamDir = '/data2/2019_04_April_CMSTiming/'
#BaseTrackDirLocal = '%sTracks/' % BaseTestbeamDir
#TimingDAQDir = '/home/sxie/TimingDAQ/'
##### Check ProcessExec for uncommenting the environment setup thingy

################ Scope Control from AutoPilot Paths ################
ScopeControlDir = '%s/ScopeHandler/KeySight/' % BaseTestbeamDir
ScopeStateFileName = '%sAcquisition/RunLog.txt' % ScopeControlDir
ScopeCommFileName = '%sAcquisition/ScopeStatus.txt' % ScopeControlDir

################ Lecroy Scope Control from AutoPilot Paths ################
LecroyScopeControlDir = '%sScopeHandler/Lecroy/' % BaseTestbeamDir
LecroyScopeStateFileName = '%sAcquisition/RunLog.txt' % LecroyScopeControlDir
LecroyScopeCommFileName = '%sAcquisition/ScopeStatus.txt' % LecroyScopeControlDir


ConfigFileBasePath = '%sconfig/' % TimingDAQDir
TOFHIRConfigFileBasePath = '/home/daq/2019_04_April_CMSTiming/TOFHIR/ConfigArchive/'

###Low pass filter frequencies####
FrequencyList=[500,750,1000]

############# OTSDAQ Information ################
#ip_address = "192.168.133.48" #ftbf-daq-06
# ip_address = "192.168.133.10" #athenanu 
ip_address = "131.225.179.70" #athenanu internet
use_socket = 17000
runFileName ="/data-08/TestBeam/Users/RunNumber/OtherRuns0NextRunNumber.txt"
#runFileName ="/data/TestBeam/Users/RunNumber/OtherRuns0NextRunNumber.txt"
localRunFileName = "../AutoPilot/otsdaq_runNumber.txt"
TClockFilePath = "../AutoPilot/TClock"

########## Key File Path starting from Recoprocesses in Javis
keyFilePath = "../RecoProcesses/key"

cred="\033[91m"
cend="\033[0m"

############### Conversion Commands for different digitizer ###########
TwoStageRecoDigitizers = {

                         'TekScope'         :  {
                                            'ConfigFileBasePath'     : '%sTekScope_' % (ConfigFileBasePath),
                                            'DatToROOTExec'          : 'NetScopeStandaloneDat2Root', 
                                            'ConversionCMD'          : 'python %sTekScope/Tektronix_DPO7254Control/Reconstruction/conversion.py %sTekScopeMount/run_scope' % (BaseTestbeamDir,BaseTestbeamDir), 
                                            'RawConversionLocalPath' : '%sTekScope/TekScopeMount/' % (BaseTestbeamDir),
                                            'RawTimingDAQLocalPath'  : '%sTekScope/RecoData/ConversionRECO/'  % (BaseTestbeamDir),
                                            'RecoTimingDAQLocalPath' : '%sTekScope/RecoData/TimingDAQRECO/' % (BaseTestbeamDir),
                                            'RawTimingDAQFileNameFormat' : 'run_scope', ##### run_scope<run>.root 
                                            },
                         'KeySightScope'    :  {
                                            'ConfigFileBasePath'     : '%sKeySightScope_' % (ConfigFileBasePath),
                                            'DatToROOTExec'          : 'NetScopeStandaloneDat2Root',
                                            'ConversionCMD'          : 'python %sReconstruction/conversion_bin_fast.py --Run ' % (ScopeControlDir), 
                                            'RawConversionLocalPath' : '/home/daq/ScopeMount/',
                                            'RawTimingDAQLocalPath'  : '%sKeySightScope/RecoData/ConversionRECO/'  % (BaseTestbeamDir),
                                            'RecoTimingDAQLocalPath' : '%sKeySightScope/RecoData/TimingDAQRECO/' % (BaseTestbeamDir),
                                            'RawTimingDAQFileNameFormat' : 'run_scope', ##### run_scope_converted<run>.root
                                            },
                         'Sampic'           :  {
                                            'ConfigFileBasePath'     : '',
                                            'DatToROOTExec'          : '',
                                            'ConversionCMD'          : 'python %sSampic/Tektronix_DPO7254Control/Reconstruction/conversion.py %sSampicMount/run_scope' % (BaseTestbeamDir,BaseTestbeamDir), 
                                            'RawConversionLocalPath' : '%sSampic/SampicMount/' % (BaseTestbeamDir),
                                            'RawTimingDAQLocalPath'  : '%sSampic/RecoData/ConversionRECO/'  % (BaseTestbeamDir),
                                            'RecoTimingDAQLocalPath' : '%sSampic/RecoData/TimingDAQRECO/' % (BaseTestbeamDir),
                                            'RawTimingDAQFileNameFormat' : 'run_scope', ##### run_scope<run>.root
                                            },
                         ## Hack for long acquisition
                         # 'LecroyScope'      :  {
                         #                    'ConfigFileBasePath'     : '%sLecroyScope_' % (ConfigFileBasePath),
                         #                    'DatToROOTExec'          : 'makeHitTree', 
                         #                    'ConversionCMD'          : 'python %s/Reconstruction/conversion_one_event.py --runNumber ' % (LecroyScopeControlDir), 
                         #                    'RawConversionLocalPath' : '/home/daq/LecroyMount/',
                         #                    'RawTimingDAQLocalPath'  : '%sLecroyScope/RecoData/ConversionRECO/'  % (BaseTestbeamDir),
                         #                    'RecoTimingDAQLocalPath' : '%sLecroyScope/RecoData/HitCounterRECO/' % (BaseTestbeamDir),
                         #                    'RawTimingDAQFileNameFormat' : 'converted_run', ##### run_scope<run>.root 
                         #                    'FinalFileNameFormat' : 'hitTree_run', ##### run_scope<run>.root 
                         #                    # 'RawTimingDAQFileNameFormat' : 'run_scope', ##### run_scope<run>.root 
                         #                    },
                        'LecroyScope'      :  {
                                           'ConfigFileBasePath'     : '%sLecroyScope_' % (ConfigFileBasePath),
                                           'DatToROOTExec'          : 'NetScopeStandaloneDat2Root', 
                                           'ConversionCMD'          : 'python %s/Reconstruction/conversion.py --runNumber ' % (LecroyScopeControlDir), 
                                           'RawConversionLocalPath' : '/home/daq/LecroyMount/',
                                           'RawTimingDAQLocalPath'  : '%sLecroyScope/RecoData/ConversionRECO/'  % (BaseTestbeamDir),
                                           'RecoTimingDAQLocalPath' : '%sLecroyScope/RecoData/TimingDAQRECO/' % (BaseTestbeamDir),
                                           'RawTimingDAQFileNameFormat' : 'converted_run', ##### run_scope<run>.root 
                                           'FinalFileNameFormat' : 'run',
                                          
                                           },
  

                        }

OneStageRecoDigitizers = {

                         'VME'     :  {     'ConfigFileBasePath'     : '%sVME_' % (ConfigFileBasePath),
                                            'DatToROOTExec'          : 'VMEDat2Root', 
                                            'RawTimingDAQLocalPath'  : '%sVME/RawData/'  % (BaseTestbeamDir),
                                            'RecoTimingDAQLocalPath' : '%sVME/RecoData/' % (BaseTestbeamDir),
                                            },

                         'DT5742'     :  {  'ConfigFileBasePath'     : '%sDT5742_' % (ConfigFileBasePath),
                                            'DatToROOTExec'          : 'DT5742Dat2Root',
                                            'RawTimingDAQLocalPath'  : '%sDT5742/RawData/'  % (BaseTestbeamDir),
                                            'RecoTimingDAQLocalPath' : '%sDT5742/RecoData/' % (BaseTestbeamDir),
                                            },

                         'TOFHIR'     :  {  'ConfigFileBasePath'     : '%sConfig_v' % (TOFHIRConfigFileBasePath), ### Set this
                                            'DatToROOTExec'          : 'convert_raw_to_trigger', ### Set this
                                            'DatToROOTExec1'         : 'convert_raw_to_singles',
                                            'DatToROOTExec2'         : 'ConvertTOFPETSinglesToEvents', #With Tracks
                                            'RawTimingDAQLocalPath'  : '%sTOFHIR/RawData/'  % (BaseTestbeamDir),
                                            'RecoTimingDAQLocalPath' : '%sTOFHIR/RecoData/v1/' % (BaseTestbeamDir),
                                            'TimingDAQLocalPath' : '%sTOFHIR/RecoData/v1/' % (BaseTestbeamDir), # Path for both raw and reco of tofhir timingdaqwithtracks
                                            'RawTimingDAQFileNameFormat' : 'run', #reco --> run<RunNumber>.root 
                                            }    
                        }


DigitizerDict = {
                    0 : 'VME',
                    1 : 'DT5742',
                    2 : 'TekScope',
                    3 : 'KeySightScope',
                    4 : 'Sampic',
                    5 : 'TOFHIR',
                    6 : 'LecroyScope'
                }

ProcessDict = {
                    0 : {'Tracking' : {'SizeCut' : 7000}},
                    1 : {'Conversion' : {'SizeCut' : 20}},
                    2 : {'TimingDAQ' : {'SizeCut' : 20000}},
                    3 : {'TimingDAQNoTracks' : {'SizeCut' : 20}},
                    4 : {'LabviewReco' : {'SizeCut' : 20000}},
                    5 : {'WatchCondor' : {'SizeCut' : 20000}},
                    6 : {'xrdcpRaw' : {'SizeCut' : 20000}}
                }
StatusDict = {
                    0 : 'Complete',
                    1 : 'Processing',
                    2 : 'Failed',
                    3 : 'Not started',
                    4 : 'Verified',
                    5 : 'Retry',
                    6 : 'Redo',
                    7 : 'N/A',
                    8 : 'Condor'
}

QueryFieldsDict = {
                    0 : 'Run number',
                    1 : 'Digitizer',
                    2 : 'Redo',
                    3 : 'Version',
                    
}

def wait_until(nseconds):
    niterations=0
    while niterations < 400: ##max out after a bit more than a minute
        niterations=niterations+1
        currentSeconds = datetime.now().time().second
        if abs(currentSeconds - nseconds)>0:
            time.sleep(0.2)
        else:
            break
    return

def ScopeState():
    ScopeStateHandle = open(ScopeStateFileName, "r")
    ScopeState = str(ScopeStateHandle.read().strip())
    ScopeStateHandle.close()
    return ScopeState

def ScopeStatusAutoPilot(runNumber):
    ScopeCommFile = open(ScopeCommFileName, "w")
    ScopeCommFile.write(str(runNumber))
    ScopeCommFile.close()
    return

def WaitForScopeStart():
    while True:
        ScopeStateHandle = open(ScopeCommFileName, "r")
        ScopeState = str(ScopeStateHandle.read().strip())
        if ScopeState=="0": break
        time.sleep(0.5)
        ScopeStateHandle.close()
    return
 
def WaitForScopeFinishAcquisition():
    while True:
        ScopeStateHandle = open(ScopeStateFileName, "r")
        ScopeState = str(ScopeStateHandle.read().strip())
        if ScopeState=="writing" or ScopeState=="ready": break
        #if ScopeState=="ready": break
        ScopeStateHandle.close()
        time.sleep(0.5)
    return


def LecroyScopeState():
    LecroyScopeStateHandle = open(LecroyScopeStateFileName, "r")
    LecroyScopeState = str(LecroyScopeStateHandle.read().strip())
    LecroyScopeStateHandle.close()
    return LecroyScopeState

def LecroyScopeStatusAutoPilot(runNumber):
    LecroyScopeCommFile = open(LecroyScopeCommFileName, "w")
    LecroyScopeCommFile.write(str(runNumber))
    LecroyScopeCommFile.close()
    return

def WaitForLecroyScopeStart():
    while True:
        LecroyScopeStateHandle = open(LecroyScopeCommFileName, "r")
        LecroyScopeState = str(LecroyScopeStateHandle.read().strip())
        if LecroyScopeState=="0": break
        time.sleep(0.5)
        LecroyScopeStateHandle.close()
    return
 
def WaitForLecroyScopeFinishAcquisition():
    while True:
        LecroyScopeStateHandle = open(LecroyScopeStateFileName, "r")
        LecroyScopeState = str(LecroyScopeStateHandle.read().strip())
        if LecroyScopeState=="writing" or LecroyScopeState=="ready": break
        #if LecroyScopeState=="ready": break
        LecroyScopeStateHandle.close()
        time.sleep(0.5)
    return


def ReadRPFile(RunNumber):                                                             
    FilePath = "%s/RP/Run%d_conditions.txt" % (BaseTestbeamDir, RunNumber)
    ValueList = []  
    if os.path.exists(FilePath):                                                                                                                                                    
        with open(FilePath) as fp:  
            line = fp.readline()
            while line:
                Value = line.strip().split(": ")[1]
                ValueList.append(Value)
                line = fp.readline()
            return ValueList[0], ValueList[1],  ValueList[2],ValueList[3],ValueList[4],ValueList[5],ValueList[6],ValueList[7],ValueList[8]
            fp.close()
    else:
            return "N/A","N/A", "N/A","N/A","N/A","N/A","N/A","N/A","N/A"

def BTLLoggingFile():                                                             
    FilePath = "/home/daq/2019_04_April_CMSTiming/TOFHIR/DAQSettings/UserInputSettings.txt" 
    ValueList = []  
    if os.path.exists(FilePath):                                                                                                                                                    
        with open(FilePath) as fp:  
            line = fp.readline()
            while line:
                Value = line.strip().split("= ")[1]
                ValueList.append(Value)
                line = fp.readline()
            return ValueList[0], ValueList[1]
            fp.close()
    else:
            return "N/A","N/A"


def ProcessLog(ProcessName, RunNumber, ProcessOutput):
    ProcessLogBasePath = "%sProcessLog/%s/" % (BaseTestbeamDir, ProcessName)
    if not os.path.exists(ProcessLogBasePath): os.system('mkdir -p %s' % ProcessLogBasePath)
    ProcessLogFilePath = ProcessLogBasePath + 'run%d.txt' % RunNumber
    ProcessFile_handle = open(ProcessLogFilePath, "a+")                                                                                                                                                                                                                                 
    ProcessFile_handle.write(ProcessOutput)
    ProcessFile_handle.close()

def DeleteProcessLog(ProcessName, RunNumber):
    ProcessLogBasePath = "%sProcessLog/%s/" % (BaseTestbeamDir, ProcessName)
    if os.path.exists(ProcessLogBasePath):     
        ProcessLogFilePath = ProcessLogBasePath + 'run%d.txt' % RunNumber
        if os.path.exists(ProcessLogFilePath):      
            os.system('rm %s' % ProcessLogFilePath)
    return

def GetKey():
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
        return 
    else:
        return key

def GetTClockTime():    
    if os.path.exists(TClockFilePath): 
        os.system(':> %s' % TClockFilePath) #Emptying the TClock File 
    else:
        os.system('mkdir -p %s' % TClockFilePath)
    os.system('curl https://www-ad.fnal.gov/notifyservlet/www?action=raw | grep -Eoi "SC time</a> \=(.+)/" | cut -c"15-18" > %s' % TClockFilePath)
    LocalMachineTime = datetime.now().time().second
    return LocalMachineTime

def GetStartAndStopSeconds(TClockStartSeconds, TClockStopSeconds):
    LocalMachineTime = GetTClockTime()
    print " Local machine time is ", LocalMachineTime
    TClockFile = open(TClockFilePath, "r")
    TClockTime = float(TClockFile.read().strip())
    TClockFile.close()  
    print " TClock time is ", TClockTime
    deltaTwrtTClock = LocalMachineTime - TClockTime
    print " Local machine time is ", LocalMachineTime
    LocalMachineStartSeconds = (TClockStartSeconds + deltaTwrtTClock) % 60
    LocalMachineStopSeconds = (TClockStopSeconds + deltaTwrtTClock) % 60
    print cred+"Beam should arrive at %0.1f seconds after minute." % ((deltaTwrtTClock+4)%60)+cend
    return int(LocalMachineStartSeconds), int(LocalMachineStopSeconds)

