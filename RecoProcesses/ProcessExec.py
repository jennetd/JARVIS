import sys 
sys.path.append('../BackEndProcesses/')
import AllModules as am
import ProcessCMDs as pc
import ParseFunctions as pf
import condorUtils as cu                                                                                                                                                                                                  

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

def ProcessExec(OrderOfExecution, PID, SaveWaveformBool = None, Version = None, RunNumber = -1, DigitizerKey = -1 , MyKey = None, GetRunListEachTime = True, condor = False, ApplyFilter = False):
	
	if not DigitizerKey == -1: Digitizer = am.DigitizerDict[DigitizerKey]
	SaveWaveformBool = SaveWaveformBool
	Version = Version
	RunNumber = RunNumber
	MyKey = MyKey 

	while True:
	
		if PID == 0:
			ProcessName = am.ProcessDict[PID].keys()[0]
			print ProcessName
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TrackingCMDs(RunNumber, MyKey, False)
			SizeCut = am.ProcessDict[PID][am.ProcessDict[PID].keys()[0]]['SizeCut']
		elif PID == 1:
			ProcessName = am.ProcessDict[PID].keys()[0] + Digitizer
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.ConversionCMDs(RunNumber, Digitizer, MyKey, False, condor)
			SizeCut = am.ProcessDict[PID][am.ProcessDict[PID].keys()[0]]['SizeCut']
		elif PID == 2:
			ProcessName = am.ProcessDict[PID].keys()[0] + Digitizer	
			DoTracking = True
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TimingDAQCMDs(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False, condor)
			SizeCut = am.ProcessDict[PID][am.ProcessDict[PID].keys()[0]]['SizeCut']
		elif PID == 3:
			ProcessName = am.ProcessDict[PID].keys()[0] + Digitizer
			DoTracking = False	
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TimingDAQCMDs(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False)
			SizeCut = am.ProcessDict[PID][am.ProcessDict[PID].keys()[0]]['SizeCut']
			print CMDList
		elif PID == 5:
			ProcessName = am.ProcessDict[PID].keys()[0] + Digitizer	
			DoTracking = True
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.WatchCondorCMDs(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False)
			SizeCut = am.ProcessDict[2][am.ProcessDict[2].keys()[0]]['SizeCut']		
			print ResultFileLocationList, RunList

		elif PID == 6:
			ProcessName = am.ProcessDict[PID].keys()[0] + Digitizer	
			DoTracking = True
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.xrdcpRawCMDs(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False)
			SizeCut = am.ProcessDict[PID][am.ProcessDict[PID].keys()[0]]['SizeCut']		
			#print ResultFileLocationList, RunList

		RunListInt = map(int,RunList)
		if OrderOfExecution == 1: 
			RunListInt.sort() #Ascending Sorting
		else:
			RunListInt.sort(reverse = True)

		if CMDList != []:	

			if GetRunListEachTime:
				RunListInt = RunListInt[:1] #Just do the first run of the list

			for run in RunListInt: 
				# if run > 27363: continue 
				if PID!=0: ProcessName = am.ProcessDict[PID].keys()[0] + Digitizer	
				index = RunList.index(run)      
				CMD = CMDList[index]  
				if RunNumber != -1 and len(FieldIDList[index])>0: 
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
					print "Looking for file at ",ResultFileLocation
					if FileSizeBool(ResultFileLocation,SizeCut) or not am.os.path.exists(ResultFileLocation): BadProcessExec = True                                                                                                                                                                                                                                                     
					if BadProcessExec:                                                                                                                                                                                                                               
						if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)  
						print 'Bad %s execution for run %d. Either the CMD format is wrong or somwthing else was wrong while execution. Please check the ProcessLog to know more.\n' % (ProcessName, run)
					else:
						if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[0], False, MyKey)
				
					cu.xrdcpTracks(run,Version)
				elif PID == 1:
					if not condor:
						if pf.QueryGreenSignal(True):
							pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
							am.time.sleep(15) #may not be necessary to wait too long anymore
						session = am.subprocess.Popen('source %s; %s' % (am.EnvSetupPath,str(CMD)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True)
						# print CMD
						# return
						while True:
							line = session.stdout.readline()
							am.ProcessLog(ProcessName, run, line)
							if not line and session.poll() != None:
								break
						if FileSizeBool(ResultFileLocation,SizeCut) or not am.os.path.exists(ResultFileLocation):
							BadProcessExec = True
							print "Looking for file at ",ResultFileLocation
                                                                                                           
						if BadProcessExec:                                                                                                                                                                                                                               
							if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)  
							print 'Bad %s execution for run %d. Either the CMD format is wrong or somwthing else was wrong while execution. Please check the ProcessLog to know more.\n' % (ProcessName, run)
						else:
							if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[0], False, MyKey)
					else:
						if pf.QueryGreenSignal(True) and not ApplyFilter: pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[8], False, MyKey)
						cu.prepareDirs()

						filterList = [0]
						if ApplyFilter: filterList = am.FrequencyList 
						for freq in filterList:
							jdlname = cu.prepareJDL(PID,DigitizerKey,run,CMD,freq)
							cu.prepareExecutable(PID,DigitizerKey,run,CMD,freq)
							## cd and submit to condor
						#	print CMD
							session = am.subprocess.Popen('cd %s; condor_submit %s; cd -' % (am.CondorDir,jdlname),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True)                                                                                                                                                                                   			

							## wait for submission
							line = session.stdout.readline()
							am.ProcessLog(ProcessName, run, line)
							if not line and session.poll() != None:
								break

				elif PID == 2 or PID == 3:
					######## For TimingDAQ02 
					# print CMD
					if not condor: 
						if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
						print am.TimingDAQDir
						# session = am.subprocess.Popen('cd %s; source %s; %s;cd -' % (am.TimingDAQDir, am.EnvSetupPath, str(CMD)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True)                                                                          
						### Hack for long acq            
						CMD2 = CMD.replace("makeHitTree","addBranches2.py")                                                                                             			
						session = am.subprocess.Popen('cd %s; %s;cd -' % (am.TimingDAQDir, str(CMD)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True)                                                                                                                                                                                   			
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
						
						print ResultFileLocation
						print SizeCut
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

					elif condor:
						if pf.QueryGreenSignal(True) and not ApplyFilter: pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[8], False, MyKey)
						## generate condor jdl and executable
						cu.prepareDirs()
						filterList = [0]
						if ApplyFilter: filterList = am.FrequencyList 
						for freq in filterList: 
							jdlname = cu.prepareJDL(PID,DigitizerKey,run,CMD,freq)
							cu.prepareExecutable(PID,DigitizerKey,run,CMD,freq)
							## cd and submit to condor
							#print CMD
							print run
							session = am.subprocess.Popen('cd %s; condor_submit %s; cd -' % (am.CondorDir,jdlname),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True)                                                                                                                                                                                   			

							# print 'condor_submit %s; cd -' % (jdlname)
							# print am.CondorDir
							## wait for submission
							line = session.stdout.readline()
							am.ProcessLog(ProcessName, run, line)
							if not line and session.poll() != None:
								break
						

				elif PID == 5:
					## checking on condor processes
					## need to check if a job is completed but file not there -> failed.
					this_proc_key = 2
					if "Conversion" in CMD: 
						this_proc_key=1

					ProcessName = am.ProcessDict[this_proc_key].keys()[0] + Digitizer
					
					if cu.CheckExistsLogs(this_proc_key,DigitizerKey,run,CMD):
						if cu.CheckExistsEOS(ResultFileLocation,SizeCut):
							if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[0], False, MyKey)
						# else:
						# 	if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)

							am.time.sleep(1)
							if this_proc_key==2:
								import GetEntries as ge
								EntriesWithTrack, EntriesWithTrackAndHit, EntriesWithHit, EntriesWithTrackWithoutNplanes,hits_ch1,hits_ch2,hits_ch3,hits_ch4,hits_ch5,hits_ch6,hits_ch7,hits_ch8, Events_ge8planes, Events_ge8planes_ge1pix = ge.RunEntries(ResultFileLocation)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackScope", int(EntriesWithTrack), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackAndHitScope", int(EntriesWithTrackAndHit), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithHitScope", int(EntriesWithHit), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackWithoutNplanesScope", int(EntriesWithTrackWithoutNplanes), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "HitsCh1", int(hits_ch1), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "HitsCh2", int(hits_ch2), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "HitsCh3", int(hits_ch3), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "HitsCh4", int(hits_ch4), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "HitsCh5", int(hits_ch5), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "HitsCh6", int(hits_ch6), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "HitsCh7", int(hits_ch7), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "HitsCh8", int(hits_ch8), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "Events_ge8planes", int(Events_ge8planes), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "Events_ge8planes_ge1pix", int(Events_ge8planes_ge1pix), False, MyKey)
									am.time.sleep(0.3)

						else:
							if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)

						## add to list of processes to check on
						## loop over list of runs to check on, grep condor logs to tell when complete, then proceed with checks.
					am.time.sleep(1)
				elif PID == 6:
					## copy raw scope files
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					#am.time.sleep(60) ## allow scope to save at least first channel
					cpstatus = cu.xrdcpRaw2(run,Digitizer)
					am.time.sleep(0.5)
					if cpstatus and pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[0], False, MyKey) 
					elif not cpstatus and pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)
					am.time.sleep(0.5) 
					am.time.sleep(2.0)
				
			if RunNumber != -1:
				break
			
			am.time.sleep(4)	
		
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
						EntriesWithTrack, EntriesWithTrackAndHit, EntriesWithHit, EntriesWithTrackWithoutNplanes,hits_ch1,hits_ch2,hits_ch3,hits_ch4 = ge.RunEntries(ResultFileLocation)
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
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "HitsCh1", int(hits_ch1), False, MyKey)
							am.time.sleep(0.3)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "HitsCh2", int(hits_ch2), False, MyKey)
							am.time.sleep(0.3)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "HitsCh3", int(hits_ch3), False, MyKey)
							am.time.sleep(0.3)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "HitsCh4", int(hits_ch4), False, MyKey)
							am.time.sleep(0.3)

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


