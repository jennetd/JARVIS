import os
import AllModules as am


def xrdcpTracks(run): 
	mountDir = am.BaseTrackDirLocal #am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath']
	destination = am.eosBaseDir+"Tracks"
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

	return success


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

def prepareJDL(PID,digitizer_key,run,CMD):

	if PID==1: 
		procname = "Conversion"

	if PID==2: 
		procname = "TimingDAQ"
	logname = am.CondorDir+"logs/%s_%i_%i.stdout"%(procname,digitizer_key,run) ### must delete log, since WatchCondor looks for this file to see if job is done. This way, retry can be used.
	if os.path.exists(logname): os.remove(logname)
	# 	inputfile = CMD.split("--input_file=\n")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir)
	# 	tracksfile = CMD.split("--pixel_input_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir)
	# 	config = CMD.split("--config_file=")[1].split()[0].replace(am.TimingDAQDir,am.eosBaseDir+"condor/")
	# 	outputfile = CMD.split("--output_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir)

	# 	arguments = " ".join([inputfile,tracksfile,config,outputfile])

	jdlfile = am.CondorDir+"jdl/condor_"+procname+"_"+str(digitizer_key)+"_"+str(PID)+"_"+str(run)+".jdl"
	exec_file = am.CondorDir+"exec/condor_"+procname+"_"+str(digitizer_key)+"_"+str(PID)+"_"+str(run)+".sh"


	f = open(jdlfile,"w+")
	f.write("universe = vanilla\n")
	f.write("Executable = %s\n"%exec_file)
	f.write("should_transfer_files = YES\n")
	f.write("when_to_transfer_output = ON_EXIT\n")
	f.write("Output = logs/%s_%i_%i.stdout\n"%(procname,digitizer_key,run))
	f.write("Error = logs/%s_%i_%i.stderr\n"%(procname,digitizer_key,run))
	f.write("Log = logs/%s_%i_%i.log\n"%(procname,digitizer_key,run))
	# f.write("Arguments = %s\n"%arguments)
	# f.write("Arguments = \n")
	f.write("Queue 1\n")
	f.close()
	return jdlfile

def prepareExecutable(PID,digitizer_key,run,CMD):
	if PID==1: 
		procname = "Conversion"
		inputfiles = []
		for i in range(1,5):
			inputfiles.append(am.eosBaseDir+am.DigitizerDict[digitizer_key]+"/RawData/Wavenewscope_CH%i_%i.bin"%(i,run))
		# outputfile = am.eosBaseDir+digitizer+"RecoData/ConversionRECO/run_scope%i.root"%run

	if PID==2: 
		procname = "TimingDAQ"
		inputfile = CMD.split("--input_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir)
		tracksfile = CMD.split("--pixel_input_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir)
		config = CMD.split("--config_file=")[1].split()[0].replace(am.TimingDAQDir,am.eosBaseDir+"condor/")
		outputfile = CMD.split("--output_file=")[1].split()[0].replace(am.BaseTestbeamDir,am.eosBaseDir)

	exec_file = am.CondorDir+"exec/condor_"+procname+"_"+str(digitizer_key)+"_"+str(PID)+"_"+str(run)+".sh"
	f = open(exec_file,"w+")
	f.write("#!/bin/bash\n")
	f.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
	f.write("cd /cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_20/src/\n")
	f.write("eval `scramv1 runtime -sh`\n")
	f.write("cd -\n")


	if PID==1:
		f.write("xrdcp root://cmseos.fnal.gov//store/group/cmstestbeam/2020_02_CMSTiming/condor/conversion_bin_fast.py .\n")
		f.write("chmod 755 conversion_bin_fast.py\n")
		for inputfile in inputfiles:
			f.write("xrdcp -s %s .\n"%inputfile)
		f.write("ls\n")	
		f.write("python conversion_bin_fast.py --Run %i\n"%run)
		# f.write("xrdcp -fs %s %s\n" % (os.path.basename(outputfile), outputfile)) ## done in script
		f.write("rm *.dat\n")		
		f.write("rm *.root\n")		
		f.write("rm *.py\n")		

	if PID==2:
		f.write("xrdcp root://cmseos.fnal.gov//store/group/cmstestbeam/2020_02_CMSTiming/condor/NetScopeStandaloneDat2Root .\n")
		f.write("chmod 755 NetScopeStandaloneDat2Root\n")

		f.write("xrdcp -s %s .\n" % inputfile)
		f.write("xrdcp -s %s .\n" % tracksfile)
		f.write("xrdcp -s %s .\n" % config)

		f.write("ls\n")
		f.write("./NetScopeStandaloneDat2Root --input_file=%s --pixel_input_file=%s  --config=%s --output_file=out_%s --save_meas --N_evts=100\n" % (os.path.basename(inputfile),os.path.basename(tracksfile),os.path.basename(config),os.path.basename(outputfile)))

		f.write("ls\n")
		f.write("xrdcp -fs out_%s %s\n" % (os.path.basename(outputfile), outputfile))

		f.write("rm *.root\n")
		f.write("rm NetScopeStandaloneDat2Root\n")
		f.write("rm *.config\n")


	f.write("echo '##### HOST DETAILS #####\n'")
	f.write("echo 'I ran on'\n")
	f.write("hostname\n")
	f.write("date\n")
