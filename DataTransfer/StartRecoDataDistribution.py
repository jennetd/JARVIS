#!/usr/bin/python

import os
import datetime
import time

print "\n########################################"
print "## Starting RECO Data Distribution      ##"
print "##########################################\n"

#You need to change this the kerberos principal being used
user = "sxie"

#Change to the location disk location
LocalDataLocation = "/data2/"

#change to name of the testbeam campaign directory
CampaignDirectoryName = "2019_04_April_CMSTiming"


continueLoop = True
while continueLoop : 

    print "\n########################################"
    print "## Starting a new data transfer cycle   ##"
    print "Time: ", str(datetime.datetime.now())
    print "##########################################\n"


    #Copy VME Raw Data from ftbf-daq-08
    print "\n\n"
    print "\n##########################################"
    print   "Transferring VME Raw Data from ftbf-daq-08"
    print   "##########################################\n"
    command = "rsync -uv --progress otsdaq@ftbf-daq-08.fnal.gov:/data/TestBeam/"+CampaignDirectoryName+"/CMSTiming/* " + LocalDataLocation+CampaignDirectoryName+"/VME/RawData/"
    print command
    os.system(command)
    time.sleep(0.5)

    
    #Copy VME RECO Data to CMSLPC EOS
    print "\n\n"
    print "\n##########################################"
    print   "Transferring VME RECO Data to CMSLPC EOS"
    print   "##########################################\n"
    command =  "rsync -ruv --progress " + LocalDataLocation+CampaignDirectoryName+"/VME/RecoData/RecoWithTracks/* "+user+"@cmslpc-sl6.fnal.gov:/eos/uscms/store/user/cmstestbeam/"+CampaignDirectoryName+"/VME/RecoData/RecoWithTracks/"
    print command
    os.system(command)
    time.sleep(0.5)

    
     #Copy DT5742 RECO Data to CMSLPC EOS
    print "\n\n"
    print "\n##########################################"
    print   "Transferring DT5742 RECO Data to CMSLPC EOS"
    print   "##########################################\n"
    command =  "rsync -ruv --progress " + LocalDataLocation+CampaignDirectoryName+"/DT5742/RecoData/RecoWithTracks/* "+user+"@cmslpc-sl6.fnal.gov:/eos/uscms/store/user/cmstestbeam/"+CampaignDirectoryName+"/DT5742/RecoData/RecoWithTracks/"
    print command
    os.system(command)
    time.sleep(0.5)

 
    #Copy KeysightScope RECO Data to CMSLPC EOS
    print "\n\n"
    print "\n###################################################"
    print   "Transferring KeysightScope RECO Data to CMSLPC EOS"
    print   "##################################################\n"
    command =  "rsync -ruv --progress " + LocalDataLocation+CampaignDirectoryName+"/KeySightScope/RecoData/TimingDAQRECO/* "+user+"@cmslpc-sl6.fnal.gov:/eos/uscms/store/user/cmstestbeam/"+CampaignDirectoryName+"/KeySightScope/RecoData/TimingDAQRECO/"
    print command
    os.system(command)
    time.sleep(0.5)

 
