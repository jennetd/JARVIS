import sys
sys.path.append('../BackEndProcesses/')
import TCP_com as tp
import shutil
import os

stripThreshold_min = 10
pixelThreshold_min = 50

stripThreshold_max = 250
pixelThreshold_max = 250

nsteps = 4

stripThreshold_step = int((stripThreshold_max - stripThreshold_min)/nsteps)
pixelThreshold_step = int((pixelThreshold_max - pixelThreshold_min)/nsteps)

stripThreshold_vals = [stripThreshold_min + i*stripThreshold_step for i in range(0,nsteps)]
pixelThreshold_vals = [pixelThreshold_min + i*pixelThreshold_step for i in range(0,nsteps)]

AutoPilotStatus=1
runsPerConf = 1
iteration = 0

path_to_xml="/home/otsdaq/Ph2_ACF_Irene/settings/PS_Module_v2p1_test.xml"
my_xml = "./PS_Module_v2p1.xml"

while AutoPilotStatus:
	
        # make xml for this iteration
        
        shutil.copy("PS_Module_v2p1_dummy.xml",my_xml)
        os.system("sed -i 's/STRIPTHRESHOLD/\""+str(stripThreshold_vals[iteration])+"\"/g' " + my_xml)
        os.system("sed -i 's/PIXELTHRESHOLD/\""+str(pixelThreshold_vals[iteration])+"\"/g' " + my_xml)

        shutil.copy(my_xml,path_to_xml)

        print("stripThreshold", stripThreshold_vals[iteration])
        print("pixelThreshold", pixelThreshold_vals[iteration])

        os.system("python AutoPilot2.py -nruns %i"%(runsPerConf))

        RunNumber = tp.GetRunNumber()
        print("Saving XML for run ", RunNumber-1)
        shutil.copy(my_xml,"PS_Module_v2p1_"+str(RunNumber-1)+".xml")

	#################################################
	#Check for Stop signal in AutoPilot.status file
	#################################################
        tmpStatusFile = open("AutoPilot.status","r") 
        tmpString = (tmpStatusFile.read().split())[0]
        if tmpString == "STOP" or tmpString == "stop":
                print("Detected stop signal.\nStopping AutoPilot...\n\n")
                AutoPilotStatus = 0
        tmpStatusFile.close()

        iteration += 1

        if iteration >= nsteps:
                AutoPilotStatus = 0
