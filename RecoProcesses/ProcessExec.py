import AllModules as am
import ProcessCMDs as pc
import ParseFunctions as pf                                                                                                                                                                                                  

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

def ProcessExec(OrderOfExecution, PID, SaveWaveformBool, Version = None, RunNumber = -1, DigitizerKey = -1 , MyKey):
	
	Digitizer = am.DigitizerDict[DigitizerKey]
	SaveWaveformBool = SaveWaveformBool
	Version = Version
	RunNumber = RunNumber
	MyKey = MyKey 
	
	if PID == 0:
		ProcessName = am.ProcessDict[PID].keys()[0]
		CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TrackingCMDs(RunNumber, MyKey, False)
		SizeCut = am.ProcessDict[PID][am.ProcessDict[PID].keys()[0]]['SizeCut']
	elif PID == 1:
		ProcessName = am.ProcessDict[PID].keys()[0] + Digitizer
		CMDList, ResultFileLocationList, RunList, FieldIDList = pc.ConversionCMDs(RunNumber, Digitizer, MyKey, False)
		SizeCut = am.ProcessDict[PID][am.ProcessDict[PID].keys()[0]]['SizeCut']
	elif PID == 2:
		ProcessName = am.ProcessDict[PID].keys()[0] + Digitizer	
		DoTracking = True
		CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TimingDAQCMDs(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False)
		SizeCut = am.ProcessDict[PID][am.ProcessDict[PID].keys()[0]]['SizeCut']
	elif PID == 3:
		ProcessName = am.ProcessDict[PID].keys()[0] + Digitizer
		DoTracking = False	
		CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TimingDAQCMDs(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False)
		SizeCut = am.ProcessDict[PID][am.ProcessDict[PID].keys()[0]]['SizeCut']

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
			if PID == 0:
				if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldIDList[index]), ProcessName, am.StatusDict[1], False)
                session = am.subprocess.Popen(["ssh", am.RulinuxSSH, str(CMD)], stderr=am.subprocess.PIPE, stdout=am.subprocess.PIPE)
			elif PID == 1:
				if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldIDList[index]), ProcessName, am.StatusDict[1], False)
				session = am.subprocess.Popen('source %s; %s' % (am.EnvSetupPath,str(CMD)),stdout=am.subprocess.PIPE, stderr=am.PIPE, shell=True)
			elif PID == 2 or PID == 3:
				if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldIDList[index]), ProcessName, am.StatusDict[1], False)
				session = am.subprocess.Popen('cd %s; source %s; %s;cd -' % (am.TimingDAQDir,am.EnvSetupPath,str(CMD)),stdout=am.PIPE, stderr=am.subprocess.PIPE, shell=True)                                                                                                                                                                                   			
			stdout, stderr = session.communicate() 
			am.ProcessLog(ProcessName, run, stdout)   
			if FileSizeBool(ResultFileLocation,SizeCut) or not am.os.path.exists(ResultFileLocation): BadProcessExec = True                                                                                                                                                                                                                                                     
			if BadProcessExec:                                                                                                                                                                                                                               
				if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldIDList[index]), ProcessName, am.StatusDict[2], False)  
			else:
				if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldIDList[index]), ProcessName, am.StatusDict[0], False)

