import AllModules as am
import ProcessCMDs as pc
import ParseFunctions as pf

def ProcessLog(ProcessName, RunNumber, ProcessOutput):
	ProcessFile_handle = open("/home/daq/fnal_tb_18_11/ProcessLog/%s/run%d.txt" % (ProcessName, RunNumber), "a+")                                                                                                                                                                                                                                 
	ProcessFile_handle.write(ProcessOutput)                                                                                                                                                                                                                                                        
	ProcessFile_handle.close()                                                                                                                                                                                                    

def exists_remote(host, path):                                                                                                                                                                                                                                                                                                
	status = subprocess.call(['ssh', host, 'test -f {0}'.format(pipes.quote(path))])                                                                                                                                                                                                                                          
	if status == 0:                                                                                                                                                                                                                                                                                                           
		return True                                                                                                                                                                                                                                                                                                           
	if status == 1:                                                                                                                                                                                                                                                                                                           
		return False                                                                                                                                                                                                                                                                                                          
	raise Exception('SSH failed') 

def TrackFileRemoteExists(RunNumber):
	TrackFilePathRulinux = am.BaseTrackDirRulinux +'CMSTimingConverted/Run%i_CMSTiming_converted.root' % RunNumber                                                                                                                                                                                                                       
	return exists_remote(am.RulinuxSSH, am.TrackFilePathRulinux), am.TrackFilePathRulinux                                                                                                                                                                                                                                              

def TrackFileLocalExists(RunNumber):
	TrackFilePathLocal = am.BaseTrackDirLocal + 'Run%i_CMSTiming_converted.root' % RunNumber                                                                                                                                                                                                                                             
	return am.os.path.exists(TrackFilePathLocal), TrackFilePathLocal                                                                                                                                                                                                                                                             

def FileSizeBool(FilePath, SizeCut):
	if am.os.path.exists(FilePath):
		return am.os.stat(FilePath).st_size < SizeCut
	else: return True

def ProcessExec(OrderOfExecution, PID, SaveWaveformBool, Version, RunNumber = -1): #PID is 1 for Tracking, 2 for Conversion, 3 for TimingDAQ
	
	SaveWaveformBool = SaveWaveformBool
	Version = Version

	if PID == 1:
		ProcessName = 'Tracking'
		CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TrackingCMDs(RunNumber, False)
		SizeCut = 10000
	elif PID == 2:
		ProcessName = 'Conversion'
		CMDList, ResultFileLocationList, RunList, FieldIDList = pc.ConversionCMDs(False)
		SizeCut = 10000
	elif PID == 3:
		ProcessName = 'TimingDAQ'	
		DoTracking = True
		CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TimingDAQCMDs(SaveWaveformBool, Version, DoTracking, False)
		SizeCut = 20000
	elif PID == 4:
		ProcessName = 'TimingDAQNoTracks'
		DoTracking = False	
		CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TimingDAQCMDs(SaveWaveformBool, Version, DoTracking, False)
		SizeCut = 20000
	elif PID == 10:
		ProcessName = 'VME'
		DoTracking = True	
		CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TimingDAQCMDs(SaveWaveformBool, Version, DoTracking, False)
		SizeCut = 20000
	elif PID == 11:
		ProcessName = 'VMENoTracks'
		DoTracking = False	
		CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TimingDAQCMDs(SaveWaveformBool, Version, DoTracking, False)
		SizeCut = 20000

	RunListInt = map(int,RunList)
	if OrderOfExecution == 1: 
		RunListInt.sort() #Ascending Sorting
	else:
		RunListInt.sort(reverse = True)


	if CMDList:	

		for run in 	RunListInt: 
			index = RunList.index(run)      
			CMD = CMDList[index]  
			ResultFileLocation = ResultFileLocationList[index]
			BadProcessExec = False
			RawStageTwoFilePath = am.RawStageTwoLocalPathScope + 'run_scope' + str(run) + '.root'
			if PID == 1:
				if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldIDList[index]), ProcessName, 'Processing', False)
                                session = am.subprocess.Popen(["ssh", am.RulinuxSSH, str(CMD)], stderr=am.subprocess.PIPE, stdout=am.subprocess.PIPE)
			elif PID == 2:
				if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldIDList[index]), ProcessName, 'Processing', False)
				session = am.subprocess.Popen('source %s; %s' % (am.EnvSetupPath,str(CMD)),stdout=am.subprocess.PIPE, stderr=am.PIPE, shell=True)
			elif PID == 3 or PID == 4:
				if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldIDList[index]), ProcessName, 'Processing', False)
				session = am.subprocess.Popen('cd %s; source %s; %s;cd -' % (am.TimingDAQDir,am.EnvSetupPath,str(CMD)),stdout=am.PIPE, stderr=am.subprocess.PIPE, shell=True)                                                                                                                                                                                   			
			stdout, stderr = session.communicate() 
			ProcessLog(ProcessName, run, stdout)   
			if FileSizeBool(ResultFileLocation,SizeCut) or not am.os.path.exists(ResultFileLocation): BadProcessExec = True                                                                                                                                                                                                                                                     
			if BadProcessExec:                                                                                                                                                                                                                               
				if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldIDList[index]), ProcessName, 'Failed', False)  
			else:
				if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldIDList[index]), ProcessName, 'Complete', False)

