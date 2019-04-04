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
RunTableAttributeNames = ['Run number', 'Start time', 'Number of spills', 'Events with track', 'Events after conversion', 'Events after timingDAQ', 'Events', 'Tracking', 'Conversion', 'TimingDAQ']
RunTableAttributeStatus = ['Processing', 'Failed', 'Not started', 'Complete', 'N/A']
MyKey = 'keyfsS7rNSv9sNG6I'
RunTableName = 'tblC4GsJFKjvXgG4e'
SensorTableName = 'tblAUIj7OVFteuAEL'
ConfigTableName = 'tblPKdZ7mOWfPr3K0'

BaseID = 'appd8tCrKgKiaAfre'
CurlBaseCommand = 'https://api.airtable.com/v0/%s/%s' % (BaseID, RunTableName)
CurlBaseCommandSensor = 'https://api.airtable.com/v0/%s/%s' % (BaseID, SensorTableName)
CurlBaseCommandConfig = 'https://api.airtable.com/v0/%s/%s' % (BaseID, ConfigTableName)
QueryFilePath ="/home/daq/Jarvis/QueryLog.txt"

################## Hard Code these paths ####################
DPOFastFramePath = ''
BaseTrackDirRulinux = '/data/TestBeam/2018_11_November_CMSTiming/'
HyperscriptPath = '/home/otsdaq/CMSTiming/HyperScriptFastTrigger_NewGeo_18_12_11.sh'
RulinuxSSH = 'otsdaq@rulinux04.dhcp.fnal.gov'
LocalSSH = 'daq@timingdaq02.dhcp.fnal.gov'

################## Paths on timingdaq02 #####################
ConfigFileBasePath = '/home/daq/TimingDAQ/config/FNAL_TestBeam_1811/'
ScopeStateFileName = '/home/daq/fnal_tb_18_11/LocalData/RECO/ETL_Agilent_MSO-X-92004A/Acquisition/RunLog.txt'
ScopeStatusFileName = '/home/daq/fnal_tb_18_11/LocalData/RECO/ETL_Agilent_MSO-X-92004A/Acquisition/ScopeStatus.txt'
BaseTrackDirLocal = '/home/daq/fnal_tb_18_11/Tracks/'
RawStageTwoLocalPathScope = '/home/daq/fnal_tb_18_11/LocalData/ROOT/'
RawStageOneLocalPathScope = '/home/daq/fnal_tb_18_11/ScopeMount/'
RawBaseLocalPath = '/home/daq/fnal_tb_18_11/'
RecoBaseLocalPath = '/home/daq/fnal_tb_18_11/LocalData/RECO/'
EnvSetupPath = '/home/daq/otsdaq/setup_ots.sh'
TimingDAQDir = '/home/daq/TimingDAQ/'
ConversionCMD = 'python /home/daq/fnal_tb_18_11/Tektronix_DPO7254Control/Reconstruction/conversion.py /home/daq/fnal_tb_18_11/ScopeMount/run_scope'


############# TCP_COM Information ################
ip_address = "192.168.133.46"
use_socket = 17000
runFileName ="/data-08/TestBeam/Users/RunNumber/OtherRuns0NextRunNumber.txt"
localRunFileName = "otsdaq_runNumber.txt"


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
    ScopeState = str(ScopeStateHandle.read())
    return ScopeState

def ScopeStatusAutoPilot():
    ScopeStatusFile = open(ScopeStatusFileName, "w")
    ScopeStatusFile.write(str(1))
    return
