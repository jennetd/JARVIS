import os
import AllModules as am
import time
import ProcessExec as pe

def xrdcpTracks(run,Version): 
	mountDir = am.BaseTrackDirLocal #am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath']
	destination = am.eosBaseDir+"Tracks/%s"%Version
	success=True
	cmd = ["xrdcp", "-fs", mountDir+"Run%i_CMSTiming_FastTriggerStream_converted.root" %run,destination]
	print cmd
	session = am.subprocess.Popen(cmd,stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT)
	while True:
		line = session.stdout.readline()
		# am.ProcessLog(ProcessName, run, line)
		if not line and session.poll() != None:
			break



def xrdcpRaw(run,Digitizer):
	## hacked for conversion
	#mountDir = am.TwoStageRecoDigitizers[Digitizer]['RawConversionLocalPath']
	mountDir = am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath']
	destination = am.eosBaseDir+Digitizer+"/RecoData/ConversionRECO"
	success=True
	cmd = ["xrdcp", "-f", mountDir+"run_scope%i.root" %run,destination]
	print cmd
	session = am.subprocess.Popen(cmd,stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT)
	while True:
		line = session.stdout.readline()
		# am.ProcessLog(ProcessName, run, line)
		if not line and session.poll() != None:
			break
	#success = success and CheckExistsEOS(destination+"/run_scope%i.root"%run ,2000)
	print "now copying raw"
	mountDir = "/home/daq/2020_02_cmstiming_ETL/KeySightScope/RawData/"#am.TwoStageRecoDigitizers[Digitizer]['RawConversionLocalPath']
	destination = am.eosBaseDir+Digitizer+"/RawData"
	for i in range(1,5):
		cmd = ["xrdcp", "-f", mountDir+"Wavenewscope_CH%i_%i.bin" %(i,run),destination]
		print cmd
		session2 = am.subprocess.Popen(cmd,stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT)
		while True:
			line = session2.stdout.readline()
			# am.ProcessLog(ProcessName, run, line)
			if not line and session2.poll() != None:
				break
	
	#for i in range(1,5):
		#success = success and CheckExistsEOS(destination+"Wavenewscope_CH%i_%i.bin" %(i,run),2000)

	return True

def xrdcpTOFHIR(run):
    mountDir = "/home/daq/TOFHIRMount/"
    #am.BaseTestbeamDir + "/T"
    print "Looking for files at ",mountDir
    LocalDir = am.BaseTestbeamDir + "TOFHIR"+"/RawData/" 	
    destination = am.eosBaseDir+"TOFHIR"+"/RawData/" 

    time.sleep(5) #This number needs to be tuned to allow TOFHIR enough time to finish writing the file between run stop commands

    rawFileList = []
    rawFileList.append("/run%i.rawf" %(run))
    rawFileList.append("/run%i.modf" %(run))
    rawFileList.append("/run%i.idxf" %(run))
    
    for f in rawFileList:
    	raw_filename = f

        cmd = ["cp",mountDir+"/raw/"+raw_filename,LocalDir]
        print cmd
        session = am.subprocess.Popen(cmd,stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT)
        while True:
            line = session.stdout.readline()
            # am.ProcessLog(ProcessName, run, line)
            if not line and session.poll() != None:
                break


        #To help with future cleanup
        cmd = ["mv",mountDir+"/raw/"+raw_filename,mountDir+"/raw/to_delete/"] #make sure this directory exists on the mount dir
        print cmd
        session3 = am.subprocess.Popen(cmd,stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT)
        while True:
            line = session3.stdout.readline()
            # am.ProcessLog(ProcessName, run, line)
            if not line and session3.poll() != None:
                break


        cmd = ["xrdcp", "-f",LocalDir+raw_filename, destination]
        print cmd
        session2 = am.subprocess.Popen(cmd,stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT)
        while True:
            line = session2.stdout.readline()
            # am.ProcessLog(ProcessName, run, line)
            if not line and session2.poll() != None:
                break
    
    # copy calibration directory associated with the run (needed for reco)
    calibDir = "/config_run%i" %(run)
    cmd = ["cp","-r",mountDir+"/raw/"+calibDir,LocalDir]
    print cmd
    session = am.subprocess.Popen(cmd,stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT)
    while True:
        line = session.stdout.readline()
        if not line and session.poll() != None:
            break

    cmd = ["mv",mountDir+"/raw/"+calibDir,mountDir+"/raw/to_delete/"] #make sure this directory exists on the mount dir
    print cmd
    session2 = am.subprocess.Popen(cmd,stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT)
    while True:
        line = session2.stdout.readline()
        if not line and session2.poll() != None:
            break

    xrdReDirector = "root://cmseos.fnal.gov/"
    relDestination = destination.split(xrdReDirector)[1]
    cmd = ["xrdfs", xrdReDirector, "mkdir", relDestination+calibDir]
    print cmd
    session3 = am.subprocess.Popen(cmd,stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT)
    while True:
        line = session3.stdout.readline()
        if not line and session3.poll() != None:
            break

    cmd = ["xrdcp", "-rf",LocalDir+calibDir,destination]
    print cmd
    session4 = am.subprocess.Popen(cmd,stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT)
    while True:
        line = session4.stdout.readline()
        if not line and session4.poll() != None:
            break
	
    return True


def xrdcpRaw2(run,Digitizer):
	mountDir = am.TwoStageRecoDigitizers[Digitizer]['RawConversionLocalPath']
	print "Looking for files at ",mountDir

	LocalDir = am.BaseTestbeamDir+ Digitizer+"/RawData/" #am.TwoStageRecoDigitizers[Digitizer]['RawConversionLocalPath']
	destination = am.eosBaseDir+Digitizer+"/RawData/" 
	time.sleep(36)
	nchan = 4
	print Digitizer
	if Digitizer == "LecroyScope":
		nchan=8
	for i in range(1,nchan+1):
		if Digitizer == "KeySightScope":
			raw_filename =  mountDir+"Wavenewscope_CH%i_%i.bin" %(i,run)
		elif Digitizer == "LecroyScope":
			raw_filename =  mountDir+"C%i--Trace%i.trc" %(i,run)
		counter=0
		#while not os.path.exists(raw_filename) and not os.path.exists(LocalDir+("C%i--Trace%i.trc" %(i,run))) and counter<15:
		while pe.FileSizeBool(raw_filename, 10**6) and not os.path.exists(LocalDir+("C%i--Trace%i.trc" %(i,run))) and counter<15:
			counter =counter+1
			print "Sleeping 2 sec, counter: {} for file: {}".format(counter, raw_filename)
			time.sleep(2)

		cmd = ["cp",raw_filename,LocalDir]
		print cmd
		session = am.subprocess.Popen(cmd,stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT)
		while True:
			line = session.stdout.readline()
			# am.ProcessLog(ProcessName, run, line)
			if not line and session.poll() != None:
				break
		cmd = ["mv",raw_filename,mountDir+"/to_delete"]
		print cmd
		session3 = am.subprocess.Popen(cmd,stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT)
		while True:
			line = session3.stdout.readline()
			# am.ProcessLog(ProcessName, run, line)
			if not line and session3.poll() != None:
				break
		
		if Digitizer == "KeySightScope": 
			cmd = ["xrdcp", "-f",LocalDir+"Wavenewscope_CH%i_%i.bin" %(i,run),destination]
		elif Digitizer == "LecroyScope":
			cmd = ["xrdcp", "-f",LocalDir+"C%i--Trace%i.trc" %(i,run),destination]
		print cmd
		session2 = am.subprocess.Popen(cmd,stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT)
		while True:
			line = session2.stdout.readline()
			# am.ProcessLog(ProcessName, run, line)
			if not line and session2.poll() != None:
				break
	

	#### Copy configuration info.
	configFileName = am.LocalConfigPath +"/Runs/info_%i.json"%run
	configDestination = am.eosBaseDir + "/ConfigInfo/Runs/"
	cmd = ["xrdcp","-f",configFileName,configDestination]
	print cmd
	session3 = am.subprocess.Popen(cmd,stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT)
	while True:
		line = session3.stdout.readline()
		# am.ProcessLog(ProcessName, run, line)
		if not line and session3.poll() != None:
			break

	# for i in range(1,5):
	# 	success = success and CheckExistsEOS(destination+"Wavenewscope_CH%i_%i.bin" %(i,run),2000)


	return True

#	return success
 


def prepareDirs():
	if not os.path.exists(am.CondorDir):
		os.makedirs(am.CondorDir)
	if not os.path.exists(am.CondorDir+"jdl"):
		os.makedirs(am.CondorDir+"jdl")
	if not os.path.exists(am.CondorDir+"logs"):
		os.makedirs(am.CondorDir+"logs")
	if not os.path.exists(am.CondorDir+"exec"):
		os.makedirs(am.CondorDir+"exec")	

def CheckExistsEOS(ResultFileLocation,sizecut):
	if "store" not in ResultFileLocation:
		print "Error, this path is not in EOS:",ResultFileLocation

	if "cmseos.fnal.gov/" in ResultFileLocation:
		cmd = ["eos", "root://cmseos.fnal.gov", "find", "--size",ResultFileLocation.split("cmseos.fnal.gov/")[1]]
	else:
		cmd = ["eos", "root://cmseos.fnal.gov", "find", "--size",ResultFileLocation]	

	print cmd
	session = am.subprocess.Popen(cmd,stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT)
	line = session.stdout.readline()
	if "size=" not in line: return False;
	if int(line.split("size=")[1].strip()) > sizecut:
		return True
	else: return False

def CheckExistsLogs(PID,digitizer_key,run,CMD):
	if PID==1: 
		procname = "Conversion"
	if PID==2: 
		procname = "TimingDAQ"
	
	logname =  am.CondorDir+"logs/%s_%i_%i.stdout"%(procname,digitizer_key,run) 
	if os.path.exists(logname): return True
	else: return False

def prepareJDL(PID,digitizer_key,run,CMD,frequency=0):

	config = ''
	if PID==1: 
		procname = "Conversion"

	if PID==2: 
		procname = "TimingDAQ"
		config = CMD.split("--config_file=")[1].split()[0]

	logname = am.CondorDir+"logs/%s_%i_%i.stdout"%(procname,digitizer_key,run) 
	if frequency!=0: logname = am.CondorDir+"logs/%s_%i_%i_%i.stdout"%(procname,digitizer_key,run,frequency)
	if os.path.exists(logname): os.remove(logname) ### must delete log, since WatchCondor looks for this file to see if job is done. This way, retry can be used.
	
	# 	inputfile = CMD.split("--input_file=\n")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir)
	# 	tracksfile = CMD.split("--pixel_input_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir)
	# 	outputfile = CMD.split("--output_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir)
    #   config = CMD.split("--config_file=")[1].split()[0].replace(am.TimingDAQDir,am.eosBaseDir+"condor/")
	# 	arguments = " ".join([inputfile,tracksfile,config,outputfile])

	jdlfile = am.CondorDir+"jdl/condor_"+procname+"_"+str(digitizer_key)+"_"+str(PID)+"_"+str(run)+".jdl"
	exec_file = am.CondorDir+"exec/condor_"+procname+"_"+str(digitizer_key)+"_"+str(PID)+"_"+str(run)+".sh"
	if frequency!=0:
		jdlfile = am.CondorDir+"jdl/condor_"+procname+"_"+str(digitizer_key)+"_"+str(PID)+"_"+str(run)+"_"+str(frequency)+".jdl"
		exec_file = am.CondorDir+"exec/condor_"+procname+"_"+str(digitizer_key)+"_"+str(PID)+"_"+str(run)+"_"+str(frequency)+".sh"

	f = open(jdlfile,"w+")
	f.write("universe = vanilla\n")
	f.write("Executable = %s\n"%exec_file)
        f.write("Transfer_Input_Files = %sConversion/conversion.py, %sNetScopeStandaloneDat2Root, %s, %s/add_branches_TimingDAQ.py, %sConversion/conversion_bin_fast.py\n"%(am.LecroyScopeControlDir, am.TimingDAQDir, config, am.LecroyScopeControlDir, am.ScopeControlDir))
	f.write("should_transfer_files = YES\n")
	f.write("when_to_transfer_output = ON_EXIT\n")
	if frequency==0:
		f.write("Output = logs/%s_%i_%i.stdout\n"%(procname,digitizer_key,run))
		f.write("Error = logs/%s_%i_%i.stderr\n"%(procname,digitizer_key,run))
		f.write("Log = logs/%s_%i_%i.log\n"%(procname,digitizer_key,run))
	else:
		f.write("Output = logs/%s_%i_%i_%i.stdout\n"%(procname,digitizer_key,run,frequency))
		f.write("Error = logs/%s_%i_%i_%i.stderr\n"%(procname,digitizer_key,run,frequency))
		f.write("Log = logs/%s_%i_%i_%i.log\n"%(procname,digitizer_key,run,frequency))
	# f.write("Arguments = %s\n"%arguments)
	# f.write("Arguments = \n")
	f.write("Queue 1\n")
	f.close()
	return jdlfile

def prepareJDLTOFHIR(PID,digitizer_key,run,CMD,frequency=0):

	doScope = True
	if PID==8: 
		doScope = False

	procname = "BTLReco"
	if (not doScope):
		procname = "BTLRecoNoScope"	

	logname = am.CondorDir+"logs/%s_%i_%i.stdout"%(procname,digitizer_key,run) 
	if os.path.exists(logname): os.remove(logname) ### must delete log, since WatchCondor looks for this file to see if job is done. This way, retry can be used.
	
	jdlfile = am.CondorDir+"jdl/condor_"+procname+"_"+str(digitizer_key)+"_"+str(PID)+"_"+str(run)+".jdl"
	exec_file = am.CondorDir+"exec/condor_"+procname+"_"+str(digitizer_key)+"_"+str(PID)+"_"+str(run)+".sh"
	
	f = open(jdlfile,"w+")
	f.write("universe = vanilla\n")
	f.write("Executable = %s\n"%exec_file)
	f.write("Transfer_Input_Files = %sBTLReco/BTLRecoScript.sh, " % (am.BaseTestbeamDir) ) #SX: need to figure out the full list of executables for the BTL Reco and need to transfer it via condor
	f.write("should_transfer_files = YES\n")
	f.write("when_to_transfer_output = ON_EXIT\n")
	f.write("Output = logs/%s_%i_%i.stdout\n"%(procname,digitizer_key,run))
	f.write("Error = logs/%s_%i_%i.stderr\n"%(procname,digitizer_key,run))
	f.write("Log = logs/%s_%i_%i.log\n"%(procname,digitizer_key,run))	
	f.write("Queue 1\n")
	f.close()
	return jdlfile


def prepareExecutable(PID,digitizer_key,run,CMD,frequency=0):
	if PID==1: 
		procname = "Conversion"
		inputfiles = []
		if digitizer_key==3:
			for i in range(1,5):
				inputfiles.append(am.eosBaseDir+am.DigitizerDict[digitizer_key]+"/RawData/Wavenewscope_CH%i_%i.bin"%(i,run))
		elif digitizer_key==6:
			for i in range(1,9):
				inputfiles.append(am.eosBaseDir+am.DigitizerDict[digitizer_key]+"/RawData/C%i--Trace%i.trc"%(i,run))
		# outputfile = am.eosBaseDir+digitizer+"RecoData/ConversionRECO/run_scope%i.root"%run

	if PID==2: 
		procname = "TimingDAQ"
		inputfile = CMD.split("--input_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir)
		tracksfile = CMD.split("--pixel_input_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir)
		config = CMD.split("--config_file=")[1].split()[0].replace(am.TimingDAQDir,am.eosBaseDir+"condor/")
		outputfile = CMD.split("--output_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir)
		if frequency != 0:
			inputfile = CMD.split("--input_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir).replace(".root","_%i.root"%frequency).replace("ConversionRECO","FilterConversionRECO")
			outputfile = CMD.split("--output_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir).replace("run_scope","run_scope_dat2root_").replace(".root","_%i.root"%frequency).replace("TimingDAQRECO","FilterTimingDAQRECO").replace("_converted","")

			# if not os.path.exists(os.path.dirname(outputfile)):
			# 	os.system("eosmkdir %s" %os.path.dirname(outputfile))

	exec_file = am.CondorDir+"exec/condor_"+procname+"_"+str(digitizer_key)+"_"+str(PID)+"_"+str(run)+".sh"
	if frequency != 0: exec_file = am.CondorDir+"exec/condor_"+procname+"_"+str(digitizer_key)+"_"+str(PID)+"_"+str(run)+"_"+str(frequency)+".sh"



	f = open(exec_file,"w+")
	f.write("#!/bin/bash\n")

	if PID==1:
		f.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
		f.write("cd /cvmfs/cms.cern.ch/slc7_amd64_gcc530/cms/cmssw/CMSSW_8_0_20/src/\n")
		f.write("eval `scramv1 runtime -sh`\n")
		f.write("cd -\n")		# f.write("source /cvmfs/sft.cern.ch/lcg/views/LCG_89/x86_64-slc6-gcc62-opt/setup.sh\n")
		if frequency == 0: 
			if digitizer_key==3:
				#f.write("xrdcp %scondor/conversion_bin_fast.py .\n"%am.eosBaseDir)
				f.write("chmod 755 conversion_bin_fast.py\n")
                        elif digitizer_key==6:
				#f.write("xrdcp %scondor/conversion.py .\n"%am.eosBaseDir)
				f.write("chmod 755 conversion.py\n")
		else:
			f.write("xrdcp %scondor/conversion_bin_fast_filter.py .\n"%am.eosBaseDir)
			f.write("chmod 755 conversion_bin_fast_filter.py\n")
		for inputfile in inputfiles:
			f.write("xrdcp -s %s .\n"%inputfile)
		f.write("ls\n")	
		if frequency == 0: 
			if digitizer_key==3:
				f.write("python conversion_bin_fast.py --Run %i\n"%run)
			elif digitizer_key==6:
				f.write("python conversion.py --runNumber %i\n"%run)
		else: f.write("python conversion_bin_fast_filter.py --Run %i --Freq %i\n"%(run,frequency))
		# f.write("xrdcp -fs %s %s\n" % (os.path.basename(outputfile), outputfile)) ## done in script
		f.write("rm *.dat\n")		
		f.write("rm *.bin\n")		
		f.write("rm *.trc\n")		
		f.write("rm *.root\n")		
		f.write("rm *.py\n")		

	if PID==2:
		f.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
		f.write("cd /cvmfs/cms.cern.ch/slc7_amd64_gcc530/cms/cmssw/CMSSW_8_0_20/src/\n")
		f.write("eval `scramv1 runtime -sh`\n")
		f.write("cd -\n")
                f.write("chmod 755 NetScopeStandaloneDat2Root\n")
                f.write("chmod 755 add_branches_TimingDAQ.py\n")
		f.write("xrdcp -s %s .\n" % inputfile)
		f.write("xrdcp -s %s .\n" % tracksfile)
                f.write("xrdcp %s/ConfigInfo/Runs/info_%i.json .\n"%(am.eosBaseDir,run))

		f.write("ls\n")
		if digitizer_key==3:
			f.write("./NetScopeStandaloneDat2Root --input_file=%s --pixel_input_file=%s  --config=%s --output_file=out_%s --save_meas\n" % (os.path.basename(inputfile),os.path.basename(tracksfile),os.path.basename(config),os.path.basename(outputfile)))
		if digitizer_key==6:
			f.write("./NetScopeStandaloneDat2Root --input_file=%s --pixel_input_file=%s  --config=%s --output_file=out_%s --save_meas --correctForTimeOffsets=true\n" % (os.path.basename(inputfile),os.path.basename(tracksfile),os.path.basename(config),os.path.basename(outputfile)))

                if digitizer_key==3:
                        f.write("ls\n")
                        f.write("xrdcp -fs out_%s %s\n" % (os.path.basename(outputfile), outputfile))
                if digitizer_key==6:
                        f.write("python add_branches_TimingDAQ.py %i %i %s\n" % (run,9999,"out_"+os.path.basename(outputfile)))
                        f.write("ls\n")
                        f.write("xrdcp -fs out_%s %s\n" % (os.path.basename(outputfile).replace(".root","_info.root"), outputfile.replace(".root","_info.root")))

		# f.write("scp out_%s daq@ti\n" % (os.path.basename(outputfile)))

		f.write("rm *.root\n")
		f.write("rm NetScopeStandaloneDat2Root*\n")
		f.write("rm *.config\n")
                f.write("rm *.json\n")
                f.write("rm *.py\n")

	f.write("echo '##### HOST DETAILS #####\n'")
	f.write("echo 'I ran on'\n")
	f.write("hostname\n")
	f.write("date\n")

def prepareExecutableTOFHIR(PID,digitizer_key,run,CMD,frequency=0):
	
	#Bryan/Chris: Put line to call BTLReco.sh in this code here

	if PID==7: 
		procname = "BTLReco"



		TOFHIRRawFile =  am.eosBaseDir + ("/TOFHIR/RawData/TOFHIR_Singles_Run%i.dat" % run)
		ScopeRecoFile = am.eosBaseDir + ("/KeysightScope/") #SX: need to check if this directory is the correct name
		tracksfile = CMD.split("--pixel_input_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir)
		config = CMD.split("--config_file=")[1].split()[0].replace(am.TimingDAQDir,am.eosBaseDir+"condor/")
		outputfile = CMD.split("--output_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir)
		if frequency != 0:
			inputfile = CMD.split("--input_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir).replace(".root","_%i.root"%frequency).replace("ConversionRECO","FilterConversionRECO")
			outputfile = CMD.split("--output_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir).replace("run_scope","run_scope_dat2root_").replace(".root","_%i.root"%frequency).replace("TimingDAQRECO","FilterTimingDAQRECO").replace("_converted","")

			# if not os.path.exists(os.path.dirname(outputfile)):
			# 	os.system("eosmkdir %s" %os.path.dirname(outputfile))


	if PID==8: 
		procname = "BTLRecoNoScope"
		inputfile = CMD.split("--input_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir)
		tracksfile = CMD.split("--pixel_input_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir)
		config = CMD.split("--config_file=")[1].split()[0].replace(am.TimingDAQDir,am.eosBaseDir+"condor/")
		outputfile = CMD.split("--output_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir)
		if frequency != 0:
			inputfile = CMD.split("--input_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir).replace(".root","_%i.root"%frequency).replace("ConversionRECO","FilterConversionRECO")
			outputfile = CMD.split("--output_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir).replace("run_scope","run_scope_dat2root_").replace(".root","_%i.root"%frequency).replace("TimingDAQRECO","FilterTimingDAQRECO").replace("_converted","")

			# if not os.path.exists(os.path.dirname(outputfile)):
			# 	os.system("eosmkdir %s" %os.path.dirname(outputfile))


	exec_file = am.CondorDir+"exec/condor_"+procname+"_"+str(digitizer_key)+"_"+str(PID)+"_"+str(run)+".sh"
	if frequency != 0: exec_file = am.CondorDir+"exec/condor_"+procname+"_"+str(digitizer_key)+"_"+str(PID)+"_"+str(run)+"_"+str(frequency)+".sh"



	f = open(exec_file,"w+")
	f.write("#!/bin/bash\n")

	
	if PID==2:
		f.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
		f.write("cd /cvmfs/cms.cern.ch/slc7_amd64_gcc530/cms/cmssw/CMSSW_8_0_20/src/\n")
		f.write("eval `scramv1 runtime -sh`\n")
		f.write("cd -\n")
                f.write("chmod 755 NetScopeStandaloneDat2Root\n")
                f.write("chmod 755 add_branches_TimingDAQ.py\n")
		f.write("xrdcp -s %s .\n" % inputfile)
		f.write("xrdcp -s %s .\n" % tracksfile)
                f.write("xrdcp %s/ConfigInfo/Runs/info_%i.json .\n"%(am.eosBaseDir,run))

		f.write("ls\n")
		if digitizer_key==3:
			f.write("./NetScopeStandaloneDat2Root --input_file=%s --pixel_input_file=%s  --config=%s --output_file=out_%s --save_meas\n" % (os.path.basename(inputfile),os.path.basename(tracksfile),os.path.basename(config),os.path.basename(outputfile)))
		if digitizer_key==6:
			f.write("./NetScopeStandaloneDat2Root --input_file=%s --pixel_input_file=%s  --config=%s --output_file=out_%s --save_meas --correctForTimeOffsets=true\n" % (os.path.basename(inputfile),os.path.basename(tracksfile),os.path.basename(config),os.path.basename(outputfile)))

                f.write("python add_branches_TimingDAQ.py %i %i %s\n" % (run,9999,"out_"+os.path.basename(outputfile)))
		f.write("ls\n")
		f.write("xrdcp -fs out_%s %s\n" % (os.path.basename(outputfile).replace(".root","_info.root"), outputfile.replace(".root","_info.root")))
		# f.write("scp out_%s daq@ti\n" % (os.path.basename(outputfile)))

		f.write("rm *.root\n")
		f.write("rm NetScopeStandaloneDat2Root*\n")
		f.write("rm *.config\n")
                f.write("rm *.json\n")
                f.write("rm *.py\n")

	f.write("echo '##### HOST DETAILS #####\n'")
	f.write("echo 'I ran on'\n")
	f.write("hostname\n")
	f.write("date\n")
