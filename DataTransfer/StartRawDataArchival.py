#!/usr/bin/python

import os
import datetime
import time

print "\n##############################"
print "## Starting RAW Data Archival ##"
print "################################\n"

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


    #Copy Strip Tracking Data from ftbf-daq-08 and to CMSLPC EOS
    print "\n\n"
    print "\n######################################################"
    print   "Transferring Strip Telescope Raw Data from ftbf-daq-08"
    print   "######################################################\n"
    command = "rsync -uv --progress otsdaq@ftbf-daq-08.fnal.gov:/data/TestBeam/"+CampaignDirectoryName+"/OtsData/* " + LocalDataLocation+CampaignDirectoryName+"/OtsData/"
    print command
    os.system(command)
    print "\n\n"
    print "\n###################################################"
    print   "Transferring Strip Telescope Raw Data to CMSLPC EOS"
    print   "###################################################\n"
    command =  "rsync -uv --progress " + LocalDataLocation+CampaignDirectoryName+"/OtsData/* "+user+"@cmslpc-sl6.fnal.gov:/eos/uscms/store/user/cmstestbeam/"+CampaignDirectoryName+"/OtsData/"
    print command
    os.system(command)
    time.sleep(0.5)

 
    #Copy NimPlus Data from ftbf-daq-08 and to CMSLPC EOS
    print "\n\n"
    print "\n######################################################"
    print   "Transferring NimPlus Data from ftbf-daq-08"
    print   "######################################################\n"
    command = "rsync -uv --progress otsdaq@ftbf-daq-08.fnal.gov:/data/TestBeam/"+CampaignDirectoryName+"/NimPlus/* " + LocalDataLocation+CampaignDirectoryName+"/NimPlus/"
    print command
    os.system(command)
    print "\n\n"
    print "\n###################################################"
    print   "Transferring NimPlus Data to CMSLPC EOS"
    print   "###################################################\n"
    command =  "rsync -uv --progress " + LocalDataLocation+CampaignDirectoryName+"/NimPlus/* "+user+"@cmslpc-sl6.fnal.gov:/eos/uscms/store/user/cmstestbeam/"+CampaignDirectoryName+"/NimPlus/"
    print command
    os.system(command)
    time.sleep(0.5)

 
    #Copy VME RAW Data from ftbf-daq-08 and to CMSLPC EOS
    print "\n\n"
    print "\n######################################################"
    print   "Transferring VME RAW Data from ftbf-daq-08"
    print   "######################################################\n"
    command = "rsync -uv --progress otsdaq@ftbf-daq-08.fnal.gov:/data/TestBeam/"+CampaignDirectoryName+"/CMSTiming/* " + LocalDataLocation+CampaignDirectoryName+"/VME/RawData/"
    print command
    os.system(command)
    print "\n\n"
    print "\n###################################################"
    print   "Transferring VME RAW Data to CMSLPC EOS"
    print   "###################################################\n"
    command =  "rsync -ruv --progress " + LocalDataLocation+CampaignDirectoryName+"/VME/RawData/* "+user+"@cmslpc-sl6.fnal.gov:/eos/uscms/store/user/cmstestbeam/"+CampaignDirectoryName+"/VME/RawData/"
    print command
    os.system(command)
    time.sleep(0.5)

 
    #Copy DT5742 RAW Data to CMSLPC EOS
    print "\n\n"
    print "\n###################################################"
    print   "Transferring DT5742 RAW Data to CMSLPC EOS"
    print   "###################################################\n"
    command =  "rsync -ruv --progress " + LocalDataLocation+CampaignDirectoryName+"/DT5742/RawData/* "+user+"@cmslpc-sl6.fnal.gov:/eos/uscms/store/user/cmstestbeam/"+CampaignDirectoryName+"/DT5742/RawData/"
    print command
    os.system(command)
    time.sleep(0.5)

 
    #Copy Keysight Scope RAW Data to CMSLPC EOS
    
