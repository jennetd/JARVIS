from AllModules import *

############### Remember to source the otsdaq environment
AutoPilotStatusFile = '/home/daq/fnal_tb_18_11/LocalData/RECO/ETL_Agilent_MSO-X-92004A/Acquisition/ScopeStatus.txt'
 
while True:

	inFile = open(AutoPilotStatusFile,"r")
	status = inFile.readline(1)
	time.sleep(1)
	if (status == str(1)):
	   	############### checking the status for the next runs #################  
	    with open(AutoPilotStatusFile,'w') as file:
	        file.write(str(0))
	    print "\n ####################### Running the scope acquisition ##################################\n"
	    AgilentScopeCommand = 'python /home/daq/fnal_tb_18_11/LocalData/RECO/ETL_Agilent_MSO-X-92004A/Acquisition/acquisition.py --numEvents 1000 --numPoints 1000 --trigCh 1 --trig -0.05'
	    os.system(AgilentScopeCommand)
	    print "\n ####################### Done with the scope acquisition ##################################\n"
