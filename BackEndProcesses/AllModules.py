import requests
import ast
from datetime import datetime
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


################### Run Table Information #################
MyKey = 'keyfsS7rNSv9sNG6I'
RunTableName = 'tblC4GsJFKjvXgG4e'
SensorTableName = 'tblAUIj7OVFteuAEL'
ConfigTableName = 'tblPKdZ7mOWfPr3K0'

BaseID = 'appd8tCrKgKiaAfre'
CurlBaseCommand = 'https://api.airtable.com/v0/%s/%s' % (BaseID, RunTableName)
CurlBaseCommandSensor = 'https://api.airtable.com/v0/%s/%s' % (BaseID, SensorTableName)
CurlBaseCommandConfig = 'https://api.airtable.com/v0/%s/%s' % (BaseID, ConfigTableName)
QueryFilePath ="/home/daq/Jarvis/QueryLog.txt"

#############################################################
################## Hard Code these paths ####################
#############################################################

############# Tracking Paths ##############

BaseTrackDirRulinux = '/data/TestBeam/2018_11_November_CMSTiming/'
#BaseTrackDirLocal = '/home/daq/fnal_tb_19_04/Tracks/'
BaseTrackDirLocal = '/data2/fnal_tb_19_04/Tracks/'
HyperscriptPath = '/home/otsdaq/CMSTiming/HyperScriptFastTrigger_NewGeo_18_12_11.sh'
RulinuxSSH = 'otsdaq@rulinux04.dhcp.fnal.gov'
#LocalSSH = 'daq@timingdaq02.dhcp.fnal.gov'
ResultTrackFileNameBeforeRunNumber = 'Run' ###########'Run%d_CMSTiming_converted.root' 
ResultTrackFileNameAfterRunNumber = '_CMSTiming_converted.root'

################ Scope Control from AutoPilot Paths ################
#ScopeStateFileName = '/home/daq/fnal_tb_18_11/LocalData/RECO/ETL_Agilent_MSO-X-92004A/Acquisition/RunLog.txt'
#ScopeCommFileName = '/home/daq/fnal_tb_18_11/LocalData/RECO/ETL_Agilent_MSO-X-92004A/Acquisition/ScopeStatus.txt'


################## Paths on timingdaq02 #####################
#BaseTestbeamDir = '/home/daq/fnal_tb_19_04/'
BaseTestbeamDir = '/data2/fnal_tb_19_04/'
EnvSetupPath = '/home/daq/otsdaq/setup_ots.sh'

########## TimingDAQ Paths ############
#TimingDAQDir = '/home/daq/CMS-MTD/TimingDAQ/'
TimingDAQDir = '/home/sxie/TimingDAQ/'
ConfigFileBasePath = '%sconfig/FNAL_TestBeam_1811/' % TimingDAQDir


############# OTSDAQ Information ################
ip_address = "192.168.133.46"
use_socket = 17000
runFileName ="/data-08/TestBeam/Users/RunNumber/OtherRuns0NextRunNumber.txt"
localRunFileName = "otsdaq_runNumber.txt"


############### Conversion Commands for different digitizer ###########
TwoStageRecoDigitizers = {

                         'TekScope'     :  {
                                            'ConfigFileBasePath'     : '',
                                            'DatToROOTExec'          : '', 
                                            'ConversionCMD'          : 'python %sTekScope/Tektronix_DPO7254Control/Reconstruction/conversion.py %sTekScopeMount/run_scope' % (BaseTestbeamDir,BaseTestbeamDir), 
                                            'RawConversionLocalPath' : '%sTekScope/TekScopeMount/' % (BaseTestbeamDir),
                                            'RawTimingDAQLocalPath'  : '%sTekScope/RecoData/ConversionRECO/'  % (BaseTestbeamDir),
                                            'RecoTimingDAQLocalPath' : '%sTekScope/RecoData/TimingDAQRECO/' % (BaseTestbeamDir),
                                            'RawTimingDAQFileNameFormat' : 'run_scope', ##### run_scope<run>.root 
                                            },
                         'KeySightScope'     :  {
                                            'ConfigFileBasePath'     : '',
                                            'DatToROOTExec'          : '',
                                            'ConversionCMD'          : 'python %sKeySightScope/...... %sKeySightScopeMount/run_scope' % (BaseTestbeamDir,BaseTestbeamDir), 
                                            'RawConversionLocalPath' : '%sKeySightScope/KeySightScopeMount/' % (BaseTestbeamDir),
                                            'RawTimingDAQLocalPath'  : '%sKeySightScope/RecoData/ConversionRECO/'  % (BaseTestbeamDir),
                                            'RecoTimingDAQLocalPath' : '%sKeySightScope/RecoData/TimingDAQRECO/' % (BaseTestbeamDir),
                                            'RawTimingDAQFileNameFormat' : 'run_scope', ##### run_scope<run>.root
                                            },
                         'Sampic'     :  {
                                            'ConfigFileBasePath'     : '',
                                            'DatToROOTExec'          : '',
                                            'ConversionCMD'          : 'python %sSampic/Tektronix_DPO7254Control/Reconstruction/conversion.py %sSampicMount/run_scope' % (BaseTestbeamDir,BaseTestbeamDir), 
                                            'RawConversionLocalPath' : '%sSampic/SampicMount/' % (BaseTestbeamDir),
                                            'RawTimingDAQLocalPath'  : '%sSampic/RecoData/ConversionRECO/'  % (BaseTestbeamDir),
                                            'RecoTimingDAQLocalPath' : '%sSampic/RecoData/TimingDAQRECO/' % (BaseTestbeamDir),
                                            'RawTimingDAQFileNameFormat' : 'run_scope', ##### run_scope<run>.root

                                            }

                        }

OneStageRecoDigitizers = {

                         'VME'     :  {     'ConfigFileBasePath'     : '%sconfig/FNAL_TestBeam_1811/VME_' % (TimingDAQDir),
                                            'DatToROOTExec'          : 'VMEDat2Root', 
                                            'RawTimingDAQLocalPath'  : '%sVME/RawData/'  % (BaseTestbeamDir),
                                            'RecoTimingDAQLocalPath' : '%sVME/RecoData/' % (BaseTestbeamDir),
                                            },
                         'DT5742'     :  {  'ConfigFileBasePath'     : '%sconfig/FNAL_TestBeam_1811/DT5742_' % (TimingDAQDir),
                                            'DatToROOTExec'          : 'DT5742Dat2Root',
                                            'RawTimingDAQLocalPath'  : '%sDT5742/RawData/'  % (BaseTestbeamDir),
                                            'RecoTimingDAQLocalPath' : '%sDT5742/RecoData/' % (BaseTestbeamDir),
                                            }
                        }


DigitizerDict = {
                    0 : 'VME',
                    1 : 'DT5742',
                    2 : 'TekScope',
                    3 : 'KeySightScope',
                    4 : 'Sampic',
                }

ProcessDict = {
                    0 : {'Tracking' : {'SizeCut' : 10000}},
                    1 : {'Conversion' : {'SizeCut' : 10000}},
                    2 : {'TimingDAQ' : {'SizeCut' : 20000}},
                    3 : {'TimingDAQNoTracks' : {'SizeCut' : 20000}},
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
}

QueryFieldsDict = {
                    0 : 'Run number',
                    1 : 'Digitizer',
                    2 : 'Redo',
                    3 : 'Version',
                    
}

def wait_until(nseconds):
    while True:
        currentSeconds = datetime.now().time().second
        if abs(currentSeconds - nseconds)>0:
            time.sleep(0.1)
        else:
            break
    return
def ScopeState():
    ScopeStateHandle = open(ScopeStateFileName, "r")
    ScopeState = str(ScopeStateHandle.read().strip())
    return ScopeState

def ScopeStatusAutoPilot():
    ScopeCommFile = open(ScopeCommFileName, "w")
    ScopeCommFile.write(str(1))
    return

def WaitForScopeStart():
    while True:
        ScopeStateHandle = open(ScopeCommFileName, "r")
        ScopeState = str(ScopeStateHandle.read().strip())
        if ScopeState=="0": break
        time.sleep(0.5)
    return

def WaitForScopeFinishAcquisition():
    while True:
        ScopeStateHandle = open(ScopeStateFileName, "r")
        ScopeState = str(ScopeStateHandle.read().strip())
        if ScopeState=="writing" or ScopeState=="ready": break
        time.sleep(0.5)
    return

def ProcessLog(ProcessName, RunNumber, ProcessOutput):
    ProcessLogBasePath = "%sProcessLog/%s/" % (BaseTestbeamDir, ProcessName)
    if not os.path.exists(ProcessLogBasePath): os.system('mkdir -p %s' % ProcessLogBasePath)
    ProcessLogFilePath = ProcessLogBasePath + 'run%d.txt' % RunNumber
    ProcessFile_handle = open(ProcessLogFilePath, "a+")                                                                                                                                                                                                                                 
    ProcessFile_handle.write(ProcessOutput)                                                                                                                                                                                                                                                        
    ProcessFile_handle.close()  