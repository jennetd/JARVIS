#!/usr/bin/python

import os
import datetime
import time
import subprocess
import glob
import TransferUtils

#You need to change this the kerberos principal being used
user = "sxie"

#Change to the location disk location
LocalDataLocation = "/data2/"

#change to name of the testbeam campaign directory
CampaignDirectoryName = "2019_04_April_CMSTiming"

continueLoop = True
while continueLoop : 


    #Copy All Data from timingdaq02
    print "\n\n"
    print "\n##########################################"
    print   "Synchronization all data from timingdaq02"
    print   "##########################################\n"

    command = "rsync -artuv --progress daq@timingdaq02:/home/daq/"+CampaignDirectoryName+"/VME/RecoData/RecoWithTracks/v3/* " + LocalDataLocation+CampaignDirectoryName+"/VME/RecoData/RecoWithTracks/v3/"
    #print command
    os.system(command)
 
    command = "rsync -artuv --progress daq@timingdaq02:/home/daq/"+CampaignDirectoryName+"/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v1/* " + LocalDataLocation+CampaignDirectoryName+"/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v1/"
    #print command
    os.system(command)

    command = "rsync -artuv --progress daq@timingdaq02:/home/daq/"+CampaignDirectoryName+"/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v1/* " + LocalDataLocation+CampaignDirectoryName+"/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v1/"
    #print command
    os.system(command)

    command = "rsync -artuv --progress daq@timingdaq02:/home/daq/"+CampaignDirectoryName+"/Tracks/* " + LocalDataLocation+CampaignDirectoryName+"/Tracks/"
    #print command
    os.system(command)

    command = "rsync -artuv --progress daq@timingdaq02:/home/daq/"+CampaignDirectoryName+"/* " + LocalDataLocation+CampaignDirectoryName+"/"
    #print command
    #os.system(command)
    time.sleep(60)
    
    
