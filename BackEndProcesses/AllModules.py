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
BaseTrackDirLocal = '/home/daq/fnal_tb_18_11/Tracks/'
HyperscriptPath = '/home/otsdaq/CMSTiming/HyperScriptFastTrigger_NewGeo_18_12_11.sh'
RulinuxSSH = 'otsdaq@rulinux04.dhcp.fnal.gov'
LocalSSH = 'daq@timingdaq02.dhcp.fnal.gov'
ResultTrackFileNameBeforeRunNumber = 'Run' ###########'Run%d_CMSTiming_converted.root' 
ResultTrackFileNameAfterRunNumber = '_CMSTiming_converted.root'

################ Scope Control from AutoPilot Paths ################
ScopeStateFileName = '/home/daq/fnal_tb_18_11/LocalData/RECO/ETL_Agilent_MSO-X-92004A/Acquisition/RunLog.txt'
ScopeCommFileName = '/home/daq/fnal_tb_18_11/LocalData/RECO/ETL_Agilent_MSO-X-92004A/Acquisition/ScopeStatus.txt'


################## Paths on timingdaq02 #####################
BaseTestbeamDir = '/home/daq/fnal_tb_19_04/'
EnvSetupPath = '/home/daq/otsdaq/setup_ots.sh'

########## TimingDAQ Paths ############
TimingDAQDir = '/home/daq/CMS-MTD/TimingDAQ/'
ConfigFileBasePath = '%sconfig/FNAL_TestBeam_1811/' % TimingDAQDir


############# OTSDAQ Information ################
ip_address = "192.168.133.46"
use_socket = 17000
runFileName ="/data-08/TestBeam/Users/RunNumber/OtherRuns0NextRunNumber.txt"
localRunFileName = "otsdaq_runNumber.txt"


############### Conversion Commands for different digitizer ###########
TwoStageRecoDigitizers = {

                         'TekScope'     :  {

                                            'ConversionCMD'          : 'python %sTekScope/Tektronix_DPO7254Control/Reconstruction/conversion.py %sTekScopeMount/run_scope' % (BaseTestbeamDir,BaseTestbeamDir), 
                                            'RawConversionLocalPath' : '%sTekScope/TekScopeMount/' % (BaseTestbeamDir),
                                            'RawTimingDAQLocalPath'  : '%sTekScope/RecoData/ConversionRECO/'  % (BaseTestbeamDir),
                                            'RecoTimingDAQLocalPath' : '%sTekScope/RecoData/TimingDAQRECO/' % (BaseTestbeamDir),
                                            'RawTimingDAQFileNameFormat' : 'run_scope' ##### run_scope<run>.root
                                            }
                         'KeySightScope'     :  {

                                            'ConversionCMD'          : 'python %sKeySightScope/...... %sKeySightScopeMount/run_scope' % (BaseTestbeamDir,BaseTestbeamDir), 
                                            'RawConversionLocalPath' : '%sKeySightScope/KeySightScopeMount/' % (BaseTestbeamDir),
                                            'RawTimingDAQLocalPath'  : '%sKeySightScope/RecoData/ConversionRECO/'  % (BaseTestbeamDir),
                                            'RecoTimingDAQLocalPath' : '%sKeySightScope/RecoData/TimingDAQRECO/' % (BaseTestbeamDir),
                                            'RawTimingDAQFileNameFormat' : 'run_scope' ##### run_scope<run>.root
                                            }
                         'Sampic'     :  {

                                            'ConversionCMD'          : 'python %sSampic/Tektronix_DPO7254Control/Reconstruction/conversion.py %sSampicMount/run_scope' % (BaseTestbeamDir,BaseTestbeamDir), 
                                            'RawConversionLocalPath' : '%sSampic/SampicMount/' % (BaseTestbeamDir),
                                            'RawTimingDAQLocalPath'  : '%sSampic/RecoData/ConversionRECO/'  % (BaseTestbeamDir),
                                            'RecoTimingDAQLocalPath' : '%sSampic/RecoData/TimingDAQRECO/' % (BaseTestbeamDir),
                                            'RawTimingDAQFileNameFormat' : 'run_scope' ##### run_scope<run>.root

                                            }

                        }

OneStageRecoDigitizers = {

                         'VME'     :  {
                                            'RawTimingDAQLocalPath'  : '%sVME/RecoData/ConversionRECO/'  % (BaseTestbeamDir),
                                            'RecoTimingDAQLocalPath' : '%sVME/RecoData/TimingDAQRECO/' % (BaseTestbeamDir),
                                            'RawTimingDAQFileNameFormat' : 'run_scope' ##### run_scope<run>.root
                                            }
                         'DT5742'     :  {
                                            'RawTimingDAQLocalPath'  : '%sKeySightScope/RecoData/ConversionRECO/'  % (BaseTestbeamDir),
                                            'RecoTimingDAQLocalPath' : '%sKeySightScope/RecoData/TimingDAQRECO/' % (BaseTestbeamDir),
                                            'RawTimingDAQFileNameFormat' : 'run_scope' ##### run_scope<run>.root
                                            }
                        }


DigitizerDict = {
                    0 : 'VME'
                    1 : 'DT5742'
                    2 : 'TekScope'
                    3 : 'KeySightScope'
                    4 : 'Sampic'
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