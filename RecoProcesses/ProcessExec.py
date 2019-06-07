import sys 
sys.path.append('/home/daq/JARVIS/BackEndProcesses/')
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

def GetSessionOutputRealTime(session):
	while True:
		line = session.stdout.readline().rstrip()
		if not line:
			break
		print type(line)
		yield line

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

def ProcessExec(OrderOfExecution, PID, SaveWaveformBool = None, Version = None, RunNumber = -1, DigitizerKey = -1 , MyKey = None, GetRunListEachTime = True):
	
	if not DigitizerKey == -1: Digitizer = am.DigitizerDict[DigitizerKey]
	SaveWaveformBool = SaveWaveformBool
	Version = Version
	RunNumber = RunNumber
	MyKey = MyKey 

	while True:
	
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

		if CMDList != []:	

			if GetRunListEachTime:
				RunListInt = RunListInt[:1] #Just do the first run of the list

			for run in RunListInt: 
			
				index = RunList.index(run)      
				CMD = CMDList[index]  
				if RunNumber != -1: 
					FieldID = FieldIDList[index][0]
				else:
					FieldID = FieldIDList[index]
				ResultFileLocation = ResultFileLocationList[index]
				BadProcessExec = False

				##### Command will be in the log file
				am.DeleteProcessLog(ProcessName, run) ###########Delete previous log file if exists
				am.ProcessLog(ProcessName, run, CMD)
				
				print '\n###############################'
				print 'Starting process %s for run %d\n' % (ProcessName, run)
                                
				if PID == 0:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					session = am.subprocess.Popen(["ssh", am.RulinuxSSH, str(CMD)],stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT)
					while True:
						line = session.stdout.readline()
						am.ProcessLog(ProcessName, run, line)
						if not line and session.poll() != None:
							break
				elif PID == 1:
					am.time.sleep(60)
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					session = am.subprocess.Popen('source %s; %s' % (am.EnvSetupPath,str(CMD)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True)
					while True:
						line = session.stdout.readline()
						am.ProcessLog(ProcessName, run, line)
						if not line and session.poll() != None:
							break
				elif PID == 2 or PID == 3:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					######## For TimingDAQ02 
					session = am.subprocess.Popen('cd %s; source %s; %s;cd -' % (am.TimingDAQDir, am.EnvSetupPath, str(CMD)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True)                                                                                                                                                                                   			
					######## For Caltech CMS Timing computer uncomment this and comment out the above line 
					#session = am.subprocess.Popen('cd %s; %s;cd -' % (am.TimingDAQDir, str(CMD)),stdout=am.subprocess.PIPE, shell=True)                                                                                                                                                                                   			
					while True:
						line = session.stdout.readline()
						am.ProcessLog(ProcessName, run, line)
						if not line and session.poll() != None:
							break
                                
                                if DigitizerKey == 5:
                                        print 'Sleeping for 60 sec'
                                        am.time.sleep(60)
                                        print 'Done sleeping'
                                
				if FileSizeBool(ResultFileLocation,SizeCut) or not am.os.path.exists(ResultFileLocation): BadProcessExec = True                                                                                                                                                                                                                                                     
				if BadProcessExec:                                                                                                                                                                                                                               
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)  
					print 'Bad %s execution for run %d. Either the CMD format is wrong or somwthing else was wrong while execution. Please check the ProcessLog to know more.\n' % (ProcessName, run)
				else:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[0], False, MyKey)
					if PID == 2 and DigitizerKey == 3:
						import GetEntries as ge
						EntriesWithTrack, EntriesWithTrackAndHit, EntriesWithHit, EntriesWithTrackWithoutNplanes = ge.RunEntries(ResultFileLocation)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackScope", int(EntriesWithTrack), False, MyKey)
							am.time.sleep(0.5)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackAndHitScope", int(EntriesWithTrackAndHit), False, MyKey)
							am.time.sleep(0.5)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithHitScope", int(EntriesWithHit), False, MyKey)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackWithoutNplanesScope", int(EntriesWithTrackWithoutNplanes), False, MyKey)

				print 'Finished process %s for run %d' % (ProcessName, run)		
				print '###############################\n'
			
			if RunNumber != -1:
				break
			am.time.sleep(1)	
		
		else:
			print '\n######################'
			print 'No runs to process!!!!'
			print '######################\n'
			am.time.sleep(4)

def ProcessExecBTLForTOFHIRTracks(OrderOfExecution, PID, SaveWaveformBool = None, Version = None, RunNumber = -1, DigitizerKey = -1 , MyKey = None, GetRunListEachTime = True):
	
	if not DigitizerKey == -1: Digitizer = am.DigitizerDict[DigitizerKey]
	SaveWaveformBool = SaveWaveformBool
	Version = Version
	RunNumber = RunNumber
	MyKey = MyKey 

	while True:
		
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
			CMDList1, CMDList2, ResultFileLocationList, RunList, FieldIDList = pc.TimingDAQCMDsBTLForTOFHIRTracks(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False)
			SizeCut = am.ProcessDict[PID][am.ProcessDict[PID].keys()[0]]['SizeCut']
		elif PID == 3:
			ProcessName = am.ProcessDict[PID].keys()[0] + Digitizer
			DoTracking = False	
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TimingDAQCMDsBTL(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False)
			SizeCut = am.ProcessDict[PID][am.ProcessDict[PID].keys()[0]]['SizeCut']
			#print RunList
		RunListInt = map(int,RunList)
		if OrderOfExecution == 1: 
			RunListInt.sort() #Ascending Sorting
		else:
			RunListInt.sort(reverse = True)

		print RunListInt

		if CMDList1 != []:	

			if GetRunListEachTime:
				RunListInt = RunListInt[:1] #Just do the first run of the list

			for run in RunListInt: 
			
				index = RunList.index(run)      
				CMD1 = CMDList1[index]  
				CMD2 = CMDList2[index] 
				if RunNumber != -1: 
					FieldID = FieldIDList[index][0]
				else:
					FieldID = FieldIDList[index]
				ResultFileLocation = ResultFileLocationList[index]
				BadProcessExec = False

				##### Command will be in the log file
				am.DeleteProcessLog(ProcessName, run) ###########Delete previous log file if exists
				am.ProcessLog(ProcessName, run, CMD1)
				am.ProcessLog(ProcessName, run, CMD2)
				
				print '\n###############################'
				print 'Starting process %s for run %d\n' % (ProcessName, run)
                                
                                if DigitizerKey == 5:
                                        print 'Sleeping for 1 sec'
                                        am.time.sleep(1)
                                        print 'Done sleeping'
                                
				if PID == 0:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					session = am.subprocess.Popen(["ssh", am.RulinuxSSH, str(CMD)],stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT)
					while True:
						line = session.stdout.readline()
						am.ProcessLog(ProcessName, run, line)
						if not line and session.poll() != None:
							break
				elif PID == 1:
					am.time.sleep(60)
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					session = am.subprocess.Popen('source %s; %s' % (am.EnvSetupPath,str(CMD)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True)
					while True:
						line = session.stdout.readline()
						am.ProcessLog(ProcessName, run, line)
						if not line and session.poll() != None:
							break
				elif PID == 2 or PID == 3:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					######## For TimingDAQ02 
					if Digitizer == am.DigitizerDict[5]:
						EnvirSetup1 = am.TOFHIRRecoDir
						EnvirSetup2 = am.TOFHIRRecoDir2
						session1 = am.subprocess.Popen('cd %s; %s;cd -' % (EnvirSetup1, str(CMD1)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True)
						while True:
							line = session1.stdout.readline()
							am.ProcessLog(ProcessName, run, line)
							if not line and session1.poll() != None:
								break
						session2 = am.subprocess.Popen('cd %s; %s;cd -' % (EnvirSetup2, str(CMD2)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True)
						while True:
							line = session2.stdout.readline()
							am.ProcessLog(ProcessName, run, line)
							if not line and session2.poll() != None:
								break				
				if FileSizeBool(ResultFileLocation,SizeCut) or not am.os.path.exists(ResultFileLocation): BadProcessExec = True                                                                                                                                                                                                                                                     
				if BadProcessExec:                                                                                                                                                                                                                               
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)  
					print 'Bad %s execution for run %d. Either the CMD format is wrong or somwthing else was wrong while execution. Please check the ProcessLog to know more.\n' % (ProcessName, run)
				else:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[0], False, MyKey)
					if PID == 2 and DigitizerKey == 3:
						import GetEntries as ge
						EntriesWithTrack, EntriesWithTrackAndHit, EntriesWithHit, EntriesWithTrackWithoutNplanes = ge.RunEntries(ResultFileLocation)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackScope", int(EntriesWithTrack), False, MyKey)
							am.time.sleep(0.5)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackAndHitScope", int(EntriesWithTrackAndHit), False, MyKey)
							am.time.sleep(0.5)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithHitScope", int(EntriesWithHit), False, MyKey)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackWithoutNplanesScope", int(EntriesWithTrackWithoutNplanes), False, MyKey)

				print 'Finished process %s for run %d' % (ProcessName, run)		
				print '###############################\n'
			
			if RunNumber != -1:
				break
			am.time.sleep(1)	
		
		else:
			print '\n######################'
			print 'No runs to process!!!!'
			print '######################\n'
			am.time.sleep(4)

def ProcessExecBTL(OrderOfExecution, PID, SaveWaveformBool = None, Version = None, RunNumber = -1, DigitizerKey = -1 , MyKey = None, GetRunListEachTime = True):
	
	if not DigitizerKey == -1: Digitizer = am.DigitizerDict[DigitizerKey]
	SaveWaveformBool = SaveWaveformBool
	Version = Version
	RunNumber = RunNumber
	MyKey = MyKey 

	while True:
	
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
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TimingDAQCMDsBTL(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False)
			SizeCut = am.ProcessDict[PID][am.ProcessDict[PID].keys()[0]]['SizeCut']
		elif PID == 3:
			ProcessName = am.ProcessDict[PID].keys()[0] + Digitizer
			DoTracking = False	
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TimingDAQCMDsBTL(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False)
			SizeCut = am.ProcessDict[PID][am.ProcessDict[PID].keys()[0]]['SizeCut']
			#print RunList
		RunListInt = map(int,RunList)
		if OrderOfExecution == 1: 
			RunListInt.sort() #Ascending Sorting
		else:
			RunListInt.sort(reverse = True)

		print RunListInt

		if CMDList != []:	

			if GetRunListEachTime:
				RunListInt = RunListInt[:1] #Just do the first run of the list

			for run in RunListInt: 
			
				index = RunList.index(run)      
				CMD = CMDList[index]  
				if RunNumber != -1: 
					FieldID = FieldIDList[index][0]
				else:
					FieldID = FieldIDList[index]
				ResultFileLocation = ResultFileLocationList[index]
				BadProcessExec = False

				##### Command will be in the log file
				am.DeleteProcessLog(ProcessName, run) ###########Delete previous log file if exists
				am.ProcessLog(ProcessName, run, CMD)
				
				print '\n###############################'
				print 'Starting process %s for run %d\n' % (ProcessName, run)
                                
                                if DigitizerKey == 5:
                                        print 'Sleeping for 60 sec'
                                        am.time.sleep(60)
                                        print 'Done sleeping'
                                
				if PID == 0:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					session = am.subprocess.Popen(["ssh", am.RulinuxSSH, str(CMD)],stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT)
					while True:
						line = session.stdout.readline()
						am.ProcessLog(ProcessName, run, line)
						if not line and session.poll() != None:
							break
				elif PID == 1:
					am.time.sleep(60)
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					session = am.subprocess.Popen('source %s; %s' % (am.EnvSetupPath,str(CMD)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True)
					while True:
						line = session.stdout.readline()
						am.ProcessLog(ProcessName, run, line)
						if not line and session.poll() != None:
							break
				elif PID == 2 or PID == 3:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					######## For TimingDAQ02 
					if Digitizer == am.DigitizerDict[5]:
						if PID == 3:
							EnvirSetup = am.TOFHIRRecoDir
						elif PID == 2:
							EnvirSetup = am.TOFHIRRecoDir2
						session = am.subprocess.Popen('cd %s; %s;cd -' % (EnvirSetup, str(CMD)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True)
					else:
						session = am.subprocess.Popen('cd %s; source %s; %s;cd -' % (am.TimingDAQDir, am.EnvSetupPath, str(CMD)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True)                                                                                                                                                                                   			
					######## For Caltech CMS Timing computer uncomment this and comment out the above line 
					#session = am.subprocess.Popen('cd %s; %s;cd -' % (am.TimingDAQDir, str(CMD)),stdout=am.subprocess.PIPE, shell=True)                                                                                                                                                                                   			
					while True:
						line = session.stdout.readline()
						am.ProcessLog(ProcessName, run, line)
						if not line and session.poll() != None:
							break
				
				if FileSizeBool(ResultFileLocation,SizeCut) or not am.os.path.exists(ResultFileLocation): BadProcessExec = True                                                                                                                                                                                                                                                     
				if BadProcessExec:                                                                                                                                                                                                                               
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)  
					print 'Bad %s execution for run %d. Either the CMD format is wrong or somwthing else was wrong while execution. Please check the ProcessLog to know more.\n' % (ProcessName, run)
				else:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[0], False, MyKey)
					if PID == 2 and DigitizerKey == 3:
						import GetEntries as ge
						EntriesWithTrack, EntriesWithTrackAndHit, EntriesWithHit, EntriesWithTrackWithoutNplanes = ge.RunEntries(ResultFileLocation)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackScope", int(EntriesWithTrack), False, MyKey)
							am.time.sleep(0.5)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackAndHitScope", int(EntriesWithTrackAndHit), False, MyKey)
							am.time.sleep(0.5)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithHitScope", int(EntriesWithHit), False, MyKey)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackWithoutNplanesScope", int(EntriesWithTrackWithoutNplanes), False, MyKey)

				print 'Finished process %s for run %d' % (ProcessName, run)		
				print '###############################\n'
			
			if RunNumber != -1:
				break
			am.time.sleep(1)	
		
		else:
			print '\n######################'
			print 'No runs to process!!!!'
			print '######################\n'
			am.time.sleep(4)



def ProcessExecApril(OrderOfExecution, PID, SaveWaveformBool = None, Version1 = None, Version2 = None, RunNumber = -1, DigitizerKey = -1 , MyKey = None, GetRunListEachTime = True):
	
	if not DigitizerKey == -1: Digitizer = am.DigitizerDict[DigitizerKey]
	SaveWaveformBool = SaveWaveformBool
	Version2 = Version2
	Version1 = Version1
	RunNumber = RunNumber
	MyKey = MyKey 

	while True:
	
		if PID == 2:
			ProcessName = am.ProcessDict[PID].keys()[0] + Digitizer	
			DoTracking = True
			CMDList1, CMDList2, ResultFileLocationList1, ResultFileLocationList2, RunList, FieldIDList = pc.TimingDAQCMDsBTL(RunNumber, SaveWaveformBool, Version1, Version2, DoTracking, Digitizer, MyKey, False)
			SizeCut = am.ProcessDict[PID][am.ProcessDict[PID].keys()[0]]['SizeCut']
		elif PID == 3:
			ProcessName = am.ProcessDict[PID].keys()[0] + Digitizer
			DoTracking = False	
			CMDList1, CMSList2, ResultFileLocationList1, ResultFileLocationList2, RunList, FieldIDList = pc.TimingDAQCMDsBTL(RunNumber, SaveWaveformBool, Version1, Version2, DoTracking, Digitizer, MyKey, False)
			SizeCut = am.ProcessDict[PID][am.ProcessDict[PID].keys()[0]]['SizeCut']

		RunListInt = map(int,RunList)
		if OrderOfExecution == 1: 
			RunListInt.sort() #Ascending Sorting
		else:
			RunListInt.sort(reverse = True)

		if CMDList1 != []:	

			if GetRunListEachTime:
				RunListInt = RunListInt[:1] #Just do the first run of the list

			for run in RunListInt: 
			
				index = RunList.index(run)      
				CMD1 = CMDList1[index]  
				CMD2 = CMDList2[index] 
				if RunNumber != -1: 
					FieldID = FieldIDList[index][0]
				else:
					FieldID = FieldIDList[index]
				ResultFileLocation1 = ResultFileLocationList1[index]
				ResultFileLocation2 = ResultFileLocationList2[index]
				BadProcessExec = False

				##### Command will be in the log file
				am.DeleteProcessLog(ProcessName, run) ###########Delete previous log file if exists
				am.ProcessLog(ProcessName, run, CMD1)
				
				print '\n###############################'
				print 'Starting process %s for run %d\n' % (ProcessName, run)
                                
				if PID == 2 or PID == 3:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					######## For TimingDAQ02 
					session1 = am.subprocess.Popen('cd %s; source %s; %s;cd -' % (am.TimingDAQDir, am.EnvSetupPath, str(CMD1)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True)                                                                                                                                                                                   			
					######## For Caltech CMS Timing computer uncomment this and comment out the above line 
					#session = am.subprocess.Popen('cd %s; %s;cd -' % (am.TimingDAQDir, str(CMD)),stdout=am.subprocess.PIPE, shell=True)                                                                                                                                                                                   			
					while True:
						line = session1.stdout.readline()
						am.ProcessLog(ProcessName, run, line)
						if not line and session1.poll() != None:
							break
					session2 = am.subprocess.Popen('cd %s; source %s; %s;cd -' % (am.TimingDAQDir, am.EnvSetupPath, str(CMD2)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True)                                                                                                                                                                                   			
					######## For Caltech CMS Timing computer uncomment this and comment out the above line 
					#session = am.subprocess.Popen('cd %s; %s;cd -' % (am.TimingDAQDir, str(CMD)),stdout=am.subprocess.PIPE, shell=True)                                                                                                                                                                                   			
					while True:
						line = session2.stdout.readline()
						am.ProcessLog(ProcessName, run, line)
						if not line and session2.poll() != None:
							break
				
				if FileSizeBool(ResultFileLocation1,SizeCut) or FileSizeBool(ResultFileLocation2,SizeCut) or not am.os.path.exists(ResultFileLocation1) or not am.os.path.exists(ResultFileLocation2): BadProcessExec = True                                                                                                                                                                                                                                                     
				if BadProcessExec:                                                                                                                                                                                                                               
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)  
					print 'Bad %s execution for run %d. Either the CMD format is wrong or somwthing else was wrong while execution. Please check the ProcessLog to know more.\n' % (ProcessName, run)
				else:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[0], False, MyKey)
				
				print 'Finished process %s for run %d' % (ProcessName, run)		
				print '###############################\n'
			
			if RunNumber != -1:
				break
			am.time.sleep(1)	
		
		else:
			print '\n######################'
			print 'No runs to process!!!!'
			print '######################\n'
			am.time.sleep(4)


