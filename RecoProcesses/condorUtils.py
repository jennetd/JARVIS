import os
import AllModules as am


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

	session = am.subprocess.Popen(cmd,stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT)
	line = session.stdout.readline()
	if "size=" not in line: return False;
	if int(line.split("size=")[1].strip()) > sizecut:
		return True
	else: return False

def prepareJDL(PID,digitizer_key,run,CMD):

	if PID==2: 
		procname = "TimingDAQ"
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
	f.write("cd /cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_9_0_2/src/\n")
	f.write("eval `scramv1 runtime -sh`\n")
	f.write("cd -\n")

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
	f.write("rm %s\n"%os.path.basename(config))
	# f.write("rm *\n") seems dangerous

	f.write("echo '##### HOST DETAILS #####\n'")
	f.write("echo 'I ran on'\n")
	f.write("hostname\n")
	f.write("date\n")
