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
CERNEOSCampaignDirectoryName = "MTDTB_FNAL_Apr2019"

LocalDir = LocalDataLocation + CampaignDirectoryName
LPCRemoteDir = "/store/group/cmstestbeam/" + CampaignDirectoryName
CERNRemoteDir = "/eos/cms/store/group/dpg_mtd/comm_mtd/TB/" + CERNEOSCampaignDirectoryName

VMERecoVersion = "v3"
DTRecoVersion = "v1"
KeySightScopeRecoVersion = "v1"

continueLoop = True
while continueLoop : 

    print "\n##########################################"
    print   "## Starting a new data transfer cycle   ##"
    print   "Time: ", str(datetime.datetime.now())
    print   "##########################################\n"


    
    #Copy VME RECO Data to CMSLPC EOS
    print "\n\n"
    print "\n###################################################"
    print   "Transferring VME RECO Data to CMSLPC EOS & CERN EOS"
    print   "###################################################\n"
    TransferUtils.XrdCopyLocalToRemote("cmseos.fnal.gov", 
                                       LPCRemoteDir + "/VME/RecoData/RecoWithTracks/"+ VMERecoVersion + "/",
                                       LocalDir+"/VME/RecoData/RecoWithTracks/"+ VMERecoVersion + "/")
    TransferUtils.XrdCopyLocalToRemote("eoscms.cern.ch", 
                                       CERNRemoteDir + "/VME/RecoData/RecoWithTracks/"+ VMERecoVersion + "/",
                                       LocalDir+"/VME/RecoData/RecoWithTracks/"+ VMERecoVersion + "/")
    time.sleep(0.5)

    

    #Copy DT5742 RECO Data to CMSLPC EOS
    print "\n\n"
    print "\n######################################################"
    print   "Transferring DT5742 RECO Data to CMSLPC EOS & CERN EOS"
    print   "######################################################\n"
    TransferUtils.XrdCopyLocalToRemote("cmseos.fnal.gov", 
                                      LPCRemoteDir + "/DT5742/RecoData/RecoWithTracks/"+ DTRecoVersion + "/",
                                      LocalDir+"/DT5742/RecoData/RecoWithTracks/"+ DTRecoVersion + "/")
    TransferUtils.XrdCopyLocalToRemote("eoscms.cern.ch", 
                                      CERNRemoteDir + "/DT5742/RecoData/RecoWithTracks/"+ DTRecoVersion + "/",
                                      LocalDir+"/DT5742/RecoData/RecoWithTracks/"+ DTRecoVersion + "/")
    time.sleep(0.5)

 
    #Copy KeysightScope RECO Data to CMSLPC EOS
    print "\n\n"
    print "\n#############################################################"
    print   "Transferring KeysightScope RECO Data to CMSLPC EOS & CERN EOS"
    print   "#############################################################\n"
    TransferUtils.XrdCopyLocalToRemote("cmseos.fnal.gov", 
                                       LPCRemoteDir + "/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/" + KeySightScopeRecoVersion + "/",
                                       LocalDir+"/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/"+ KeySightScopeRecoVersion + "/")
    TransferUtils.XrdCopyLocalToRemote("eoscms.cern.ch", 
                                       CERNRemoteDir + "/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/"+ KeySightScopeRecoVersion + "/",
                                       LocalDir+"/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/"+ KeySightScopeRecoVersion + "/")
    time.sleep(0.5)

 
