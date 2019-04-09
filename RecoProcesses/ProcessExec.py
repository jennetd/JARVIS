import sys 
sys.path.append('/home/sxie/JARVIS/BackEndProcesses/')
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

def ProcessExec(OrderOfExecution, PID, SaveWaveformBool = None, Version = None, RunNumber = -1, DigitizerKey = -1 , MyKey = None):
	
	if not DigitizerKey == -1: Digitizer = am.DigitizerDict[DigitizerKey]
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
			if RunNumber != -1: 
				FieldID = FieldIDList[index][0]
			else:
				FieldID = FieldIDList[index]
			ResultFileLocation = ResultFileLocationList[index]
			BadProcessExec = False

			##### Command will be in the log file
			ProcessFile_handle = am.ProcessLog(ProcessName, run, CMD)
			
			print '\n###############################'
			print 'Starting process %s for run %d\n' % (ProcessName, run)

			if PID == 0:
				if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False)
				session = am.subprocess.Popen(["ssh", am.RulinuxSSH, str(CMD)], stderr=am.subprocess.PIPE, stdout=ProcessFile_handle)
			elif PID == 1:
				if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False)
				session = am.subprocess.Popen('source %s; %s' % (am.EnvSetupPath,str(CMD)),stdout=ProcessFile_handle, stderr=am.PIPE, shell=True)
			elif PID == 2 or PID == 3:
				if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False)
				session = am.subprocess.Popen('cd %s; %s;cd -' % (am.TimingDAQDir,str(CMD)),stdout=ProcessFile_handle, stderr=am.subprocess.PIPE, shell=True)                                                                                                                                                                                   			
			stderr = session.communicate() 
			
			ProcessFile_handle.close()  
			if FileSizeBool(ResultFileLocation,SizeCut) or not am.os.path.exists(ResultFileLocation): BadProcessExec = True                                                                                                                                                                                                                                                     
			if BadProcessExec:                                                                                                                                                                                                                               
				if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False)  
				print 'Bad %s execution for run %d. Either the CMD format is wrong or somwthing else was wrong while execution. Please check the ProcessLog to know more.\n' % (ProcessName, run)
			else:
				if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[0], False)
			
			print 'Finished process %s for run %d' % (ProcessName, run)
			print '###############################\n'

