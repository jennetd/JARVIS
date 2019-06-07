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
LocalDataLocation = "/home/daq/"

#change to name of the testbeam campaign directory
CampaignDirectoryName = "2019_04_April_CMSTiming"
CERNEOSCampaignDirectoryName = "MTDTB_FNAL_Jun2019"

LocalDir = LocalDataLocation + CampaignDirectoryName
LPCRemoteDir = "/eos/uscms/store/group/cmstestbeam/" + CampaignDirectoryName
CERNRemoteDir = "/eos/cms/store/group/dpg_mtd/comm_mtd/TB/" + CERNEOSCampaignDirectoryName

VMERecoVersion = "v3"
DTRecoVersion = "v1"
KeySightScopeRecoVersion = "v1"
TOFHIRRecoVersion = "v1"

continueLoop = True
while continueLoop : 

    print "\n##########################################"
    print   "## Starting a new data transfer cycle   ##"
    print   "Time: ", str(datetime.datetime.now())
    print   "##########################################\n"


    
    # #Copy VME RECO Data to CMSLPC EOS
    # print "\n\n"
    # print "\n###################################################"
    # print   "Transferring VME RECO Data to CMSLPC EOS & CERN EOS"
    # print   "###################################################\n"

    command = "rsync -uv --progress "+LocalDir+"/VME/RecoData/RecoWithTracks/"+ VMERecoVersion + "/* sxie@cmslpc-sl6.fnal.gov:" + LPCRemoteDir + "/VME/RecoData/RecoWithTracks/"+ VMERecoVersion + "/"
    print command
    os.system(command)

    # TransferUtils.XrdCopyLocalToRemote("cmseos.fnal.gov", 
    #                                    LPCRemoteDir + "/VME/RecoData/RecoWithTracks/"+ VMERecoVersion + "/",
    #                                    LocalDir+"/VME/RecoData/RecoWithTracks/"+ VMERecoVersion + "/")
    # TransferUtils.XrdCopyLocalToRemote("eoscms.cern.ch", 
    #                                    CERNRemoteDir + "/VME/RecoData/RecoWithTracks/"+ VMERecoVersion + "/",
    #                                    LocalDir+"/VME/RecoData/RecoWithTracks/"+ VMERecoVersion + "/")
    # time.sleep(0.5)

    

    # #Copy DT5742 RECO Data to CMSLPC EOS
    # print "\n\n"
    # print "\n######################################################"
    # print   "Transferring DT5742 RECO Data to CMSLPC EOS & CERN EOS"
    # print   "######################################################\n"
    # TransferUtils.XrdCopyLocalToRemote("cmseos.fnal.gov", 
    #                                   LPCRemoteDir + "/DT5742/RecoData/RecoWithTracks/"+ DTRecoVersion + "/",
    #                                   LocalDir+"/DT5742/RecoData/RecoWithTracks/"+ DTRecoVersion + "/")
    # TransferUtils.XrdCopyLocalToRemote("eoscms.cern.ch", 
    #                                   CERNRemoteDir + "/DT5742/RecoData/RecoWithTracks/"+ DTRecoVersion + "/",
    #                                   LocalDir+"/DT5742/RecoData/RecoWithTracks/"+ DTRecoVersion + "/")
    # time.sleep(0.5)

 
    # #Copy KeysightScope RECO Data to CMSLPC EOS
    # print "\n\n"
    # print "\n#############################################################"
    # print   "Transferring KeysightScope RECO Data to CMSLPC EOS & CERN EOS"
    # print   "#############################################################\n"
    # TransferUtils.XrdCopyLocalToRemote("cmseos.fnal.gov", 
    #                                    LPCRemoteDir + "/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/" + KeySightScopeRecoVersion + "/",
    #                                    LocalDir+"/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/"+ KeySightScopeRecoVersion + "/")
    # TransferUtils.XrdCopyLocalToRemote("eoscms.cern.ch", 
    #                                    CERNRemoteDir + "/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/"+ KeySightScopeRecoVersion + "/",
    #                                    LocalDir+"/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/"+ KeySightScopeRecoVersion + "/")
    # time.sleep(0.5)

 
    #Copy TOFHIR RECO Data to CMSLPC EOS
    print "\n\n"
    print "\n######################################################"
    print   "Transferring TOFHIR RECO Data to CMSLPC EOS & CERN EOS"
    print   "######################################################\n"
    command = "rsync -uv --progress "+LocalDir+"/TOFHIR/RecoData/"+ TOFHIRRecoVersion + "/RecoWithoutTracks/* sxie@cmslpc-sl6.fnal.gov:" + LPCRemoteDir + "/TOFHIR/RecoData/RecoWithoutTracks/"+ TOFHIRRecoVersion + "/"
    print command
    os.system(command)
    # command = "rsync -uv --progress "+LocalDir+"/TOFHIR/RecoData/RecoWithTracks/"+ TOFHIRRecoVersion + "/* sxie@cmslpc-sl6.fnal.gov:" + LPCRemoteDir + "/TOFHIR/RecoData/RecoWithTracks/"+ TOFHIRRecoVersion + "/"
    # print command
    # os.system(command)
    # TransferUtils.XrdCopyLocalToRemote("cmseos.fnal.gov", 
    #                                   LPCRemoteDir + "/TOFHIR/RecoData/RecoWithoutTracks/"+ TOFHIRRecoVersion + "/",
    #                                   LocalDir+"/TOFHIR/RecoData/RecoWithoutTracks/"+ TOFHIRRecoVersion + "/")
    # TransferUtils.XrdCopyLocalToRemote("cmseos.fnal.gov", 
    #                                   LPCRemoteDir + "/TOFHIR/RecoData/RecoWithTracks/"+ TOFHIRRecoVersion + "/",
    #                                   LocalDir+"/TOFHIR/RecoData/RecoWithTracks/"+ TOFHIRRecoVersion + "/")
    # TransferUtils.XrdCopyLocalToRemote("eoscms.cern.ch", 
    #                                   CERNRemoteDir + "/TOFHIR/RecoData/" + TOFHIRRecoVersion + "/RecoWithoutTracks/",
    #                                   LocalDir+"/TOFHIR/RecoData/RecoWithoutTracks/"+ TOFHIRRecoVersion + "/")
    # TransferUtils.XrdCopyLocalToRemote("eoscms.cern.ch", 
    #                                   CERNRemoteDir + "/TOFHIR/RecoData/RecoWithTracks/"+ TOFHIRRecoVersion + "/",
    #                                   LocalDir+"/TOFHIR/RecoData/RecoWithTracks/"+ TOFHIRRecoVersion + "/")
    # time.sleep(0.5)

    time.sleep(600)
