#!/usr/bin/python

import os
import datetime
import time
import subprocess
import glob
import TransferUtils

print "\n##########################################"
print   "## Starting RECO Data Distribution      ##"
print   "##########################################\n"

#You need to change this the kerberos principal being used
user = "sxie"

#Change to the location disk location
LocalDataLocation = "/data2/"

#change to name of the testbeam campaign directory
CampaignDirectoryName = "2019_04_April_CMSTiming"

VMERecoVersion = "v1"
DTRecoVersion = "v1"

continueLoop = True
while continueLoop : 

    print "\n##########################################"
    print   "## Starting a new data transfer cycle   ##"
    print   "Time: ", str(datetime.datetime.now())
    print   "##########################################\n"


    #Copy VME RECO Data from timingdaq02
    print "\n\n"
    print "\n##########################################"
    print   "Synchronization all data timingdaq02"
    print   "##########################################\n"
    command = "rsync -artuv  --progress daq@timingdaq02:/home/daq/"+CampaignDirectoryName+"/* " + LocalDataLocation+CampaignDirectoryName+"/"
    print command
    os.system(command)
    time.sleep(0.5)

    
    #Copy VME RECO Data to CMSLPC EOS
    print "\n\n"
    print "\n##########################################"
    print   "Transferring VME RECO Data to CMSLPC EOS"
    print   "##########################################\n"
    TransferUtils.XrdCopyLocalToRemote("cmseos.fnal.gov", 
                                       "/store/group/cmstestbeam/" + CampaignDirectoryName + "/VME/RecoData/RecoWithTracks/"+ VMERecoVersion + "/",
                                       LocalDataLocation+CampaignDirectoryName+"/VME/RecoData/RecoWithTracks/"+ VMERecoVersion + "/")
    time.sleep(0.5)

    
    #Copy DT5742 RECO Data to CMSLPC EOS
    print "\n\n"
    print "\n##########################################"
    print   "Transferring DT5742 RECO Data to CMSLPC EOS"
    print   "##########################################\n"
    TransferUtils.XrdCopyLocalToRemote("cmseos.fnal.gov", 
                                       "/store/group/cmstestbeam/" + CampaignDirectoryName + "/DT5742/RecoData/RecoWithTracks/"+ DTRecoVersion + "/",
                                       LocalDataLocation+CampaignDirectoryName+"/DT5742/RecoData/RecoWithTracks/"+ DTRecoVersion + "/")
    print command
    os.system(command)
    time.sleep(0.5)

 
    #Copy KeysightScope RECO Data to CMSLPC EOS
    print "\n\n"
    print "\n###################################################"
    print   "Transferring KeysightScope RECO Data to CMSLPC EOS"
    print   "##################################################\n"
    TransferUtils.XrdCopyLocalToRemote("cmseos.fnal.gov", 
                                       "/store/group/cmstestbeam/" + CampaignDirectoryName + "/KeySightScope/RecoData/RecoWithTracks/",
                                       LocalDataLocation+CampaignDirectoryName+"/KeySightScope/RecoData/RecoWithTracks/")
    time.sleep(0.5)

 
