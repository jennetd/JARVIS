import ParseFunctions as pf
import ProcessRuns as pr
import AllModules as am


################################################################################################################################################################################################################                                                                         
################################################################################################################################################################################################################                                                                         
##################################These Functions get run lists for various processes from the run table and returns the list of the respective process running commands #######################################
################################################################################################################################################################################################################                                                                         ################################################################################################################################################################################################################                                                                                                           


def TrackingCMDs(RunNumber, MyKey, Debug):
    MyKey = MyKey
    RunNumber = RunNumber
    
    RunList, FieldIDList = pr.TrackingRuns(RunNumber, MyKey, False)
    TrackingCMDList = []
    ResultFileLocationList = []

    if RunList != None:
        
        for run in RunList: 
            TrackingCMDList.append('. %s %d' % (am.HyperscriptPath, run)) #####Modify Hyperscript to scp the result file on the local machine
            ResultFileLocationList.append(am.BaseTrackDirLocal + am.ResultTrackFileNameBeforeRunNumber + str(run) + am.ResultTrackFileNameAfterRunNumberFast)
        return TrackingCMDList, ResultFileLocationList, RunList, FieldIDList
 
    else:
        return None,None,None,None   

def xrdcpRawCMDs(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False):
    RunList, FieldIDList = pr.xrdcpRawRuns(RunNumber, Digitizer, MyKey, False)
    cpCMDList = []
    ResultFileLocationList = []

    # am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath']
    if RunList != None:
        for run in RunList:
        #     cmd = "xrdcp -fs %s %s" %(outputFile,eosPath)
            cpCMDList.append("holder")
            ResultFileLocationList.append("holder")
        return cpCMDList, ResultFileLocationList, RunList, FieldIDList
    else:
        return None,None,None,None 

def ConversionCMDs(RunNumber, Digitizer, MyKey, Debug, condor):
    MyKey = MyKey
    RunNumber = RunNumber
    Digitizer = Digitizer

    RunList, FieldIDList = pr.ConversionRuns(RunNumber, Digitizer, MyKey, False,condor)
    ConversionCMDList = []
    ResultFileLocationList = []

    if RunList != None:
        
        for run in RunList: 

            ConversionCMDList.append(am.TwoStageRecoDigitizers[Digitizer]['ConversionCMD'] + str(run))
            ResultFileLocationList.append(am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath'] + am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat'] + str(run) + '.root')
        return ConversionCMDList, ResultFileLocationList, RunList, FieldIDList

    else:
        return None,None,None,None   



def TimingDAQCMDs(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, Debug, condor):
    DoTracking = DoTracking 
    MyKey = MyKey
    Digitizer = Digitizer
    RunNumber = RunNumber

    RunList, FieldIDList = pr.TimingDAQRuns(RunNumber, DoTracking, Digitizer, MyKey, False, condor)
    DatToRootCMDList = []
    ResultFileLocationList = []
    RunsNotPresent = []

    if RunList != None:

        for run in RunList: 

            RecoLocalPath = None
            RunNotPresent = False
            RawLocalPath = None
            Index = RunList.index(run)

            if Digitizer == am.DigitizerDict[0] or Digitizer == am.DigitizerDict[1]:
                RecoBaseLocalPath = am.OneStageRecoDigitizers[Digitizer]['RecoTimingDAQLocalPath']
                RawBaseLocalPath = am.OneStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath']
                ConfigFilePath = am.OneStageRecoDigitizers[Digitizer]['ConfigFileBasePath'] + '%s.config' % Version
                DatToROOTExec = am.OneStageRecoDigitizers[Digitizer]['DatToROOTExec']
                ResultTrackFileNameAfterRunNumber = am.ResultTrackFileNameAfterRunNumberSlow
            else:
                RecoBaseLocalPath = am.TwoStageRecoDigitizers[Digitizer]['RecoTimingDAQLocalPath']
                RawBaseLocalPath = am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath']
                ConfigFilePath = am.TwoStageRecoDigitizers[Digitizer]['ConfigFileBasePath'] + '%s.config' % Version
                DatToROOTExec = am.TwoStageRecoDigitizers[Digitizer]['DatToROOTExec']
                ResultTrackFileNameAfterRunNumber = am.ResultTrackFileNameAfterRunNumberFast

            if not DoTracking: 
                RecoBaseLocalPath = RecoBaseLocalPath + 'RecoWithoutTracks/'
            else:
                RecoBaseLocalPath = RecoBaseLocalPath + 'RecoWithTracks/'

            RecoBaseLocalPath = RecoBaseLocalPath + Version + '/'

            if not am.os.path.exists(RecoBaseLocalPath): am.os.system('mkdir -p %s' % RecoBaseLocalPath)
            if Digitizer == am.DigitizerDict[0] or Digitizer == am.DigitizerDict[1]:
                ListRawRunNumber = [(x.split("_Run")[1].split(".dat")[0].split("_")[0]) for x in am.glob.glob(RawBaseLocalPath + '*_Run*')]
                ListRawFilePath = [x for x in am.glob.glob(RawBaseLocalPath + '*_Run*')] 
                if str(run) in ListRawRunNumber: 
                    RawLocalPath = ListRawFilePath[ListRawRunNumber.index(str(run))]
                    RecoLocalPath = RecoBaseLocalPath + '/' + RawLocalPath.split(".dat")[0].split("%s" % RawBaseLocalPath)[1] + '.root'                                            
                else:
                    RunNotPresent = True
                    RunsNotPresent.append(run)
            else:
                RawLocalPath =  RawBaseLocalPath + am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat'] + str(run) + '.root'                                      
                RecoLocalPath = RecoBaseLocalPath + '/' + am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat']+ str(run) + '_converted.root' 

            if not RunNotPresent:

                ResultFileLocationList.append(RecoLocalPath)
                DatToRootCMD = './' + DatToROOTExec + ' --config_file=' + ConfigFilePath + ' --input_file=' + RawLocalPath + ' --output_file=' + RecoLocalPath
                if SaveWaveformBool: DatToRootCMD = DatToRootCMD + ' --save_meas'
            
                if DoTracking: 
                    TrackFilePathLocal = am.BaseTrackDirLocal + am.ResultTrackFileNameBeforeRunNumber + str(run) + ResultTrackFileNameAfterRunNumber
                    DatToRootCMD = DatToRootCMD + ' --pixel_input_file=' + TrackFilePathLocal   

                DatToRootCMDList.append(DatToRootCMD)

        #Remove the runs which were not present
        for run in RunsNotPresent:
            print 'Run %d not present in the raw files' % run
            del FieldIDList[RunList.index(run)]
            RunList.remove(run)

        return DatToRootCMDList, ResultFileLocationList, RunList, FieldIDList

    else:
        return None,None,None,None   


def WatchCondorCMDs(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False):
    RunList, FieldIDList,ProcessList = pr.WatchCondorRuns(RunNumber, DoTracking, Digitizer, MyKey, False)
    WatchCMDList = []
    ResultFileLocationList = []
    RecoBaseLocalPath = am.TwoStageRecoDigitizers[Digitizer]['RecoTimingDAQLocalPath']+'RecoWithTracks/'+ Version + '/'
    ConvertedBaseLocalPath = am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath']

    for i,run in enumerate(RunList):
        if(ProcessList[i]==2):
            RecoLocalPath = RecoBaseLocalPath + am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat']+ str(run) + '_converted.root' 
            RecoEOSpath = RecoLocalPath.replace(am.BaseTestbeamDir,am.eosBaseDir)
            WatchCMDList.append("TimingDAQ")
        if(ProcessList[i]==1):
            RecoLocalPath = ConvertedBaseLocalPath + am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat'] + str(run) + '.root'         
            RecoEOSpath = RecoLocalPath.replace(am.BaseTestbeamDir,am.eosBaseDir)
            WatchCMDList.append("Conversion")
       
        ResultFileLocationList.append(RecoEOSpath)
    # print "end of WatchCondorCMDs"
    # print WatchCMDList,RunList,ResultFileLocationList
    return WatchCMDList, ResultFileLocationList, RunList, FieldIDList

def TimingDAQCMDsBTLApril(RunNumber, SaveWaveformBool, Version1, Version2, DoTracking, Digitizer, MyKey, Debug):
    DoTracking = DoTracking 
    MyKey = MyKey
    Digitizer = Digitizer
    RunNumber = RunNumber

    RunList, FieldIDList = pr.TimingDAQRuns(RunNumber, DoTracking, Digitizer, MyKey, False)
    DatToRootCMDList1 = []
    DatToRootCMDList2 = []
    ResultFileLocationList1 = []
    ResultFileLocationList2 = []
    RunsNotPresent = []

    if RunList != None:

        for run in RunList: 

            RecoLocalPath1 = None
            RecoLocalPath2 = None
            RunNotPresent = False
            RawLocalPath = None
            Index = RunList.index(run)

            if Digitizer == am.DigitizerDict[0] or Digitizer == am.DigitizerDict[1]:
                RecoBaseLocalPath = am.OneStageRecoDigitizers[Digitizer]['RecoTimingDAQLocalPath']
                RawBaseLocalPath = am.OneStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath']
                ConfigFilePath1 = am.OneStageRecoDigitizers[Digitizer]['ConfigFileBasePath'] + '%s.config' % Version1
                ConfigFilePath2 = am.OneStageRecoDigitizers[Digitizer]['ConfigFileBasePath'] + '%s.config' % Version2
                DatToROOTExec = am.OneStageRecoDigitizers[Digitizer]['DatToROOTExec']
                ResultTrackFileNameAfterRunNumber = am.ResultTrackFileNameAfterRunNumberSlow

            if not DoTracking: 
                RecoBaseLocalPath = RecoBaseLocalPath + 'RecoWithoutTracks/'
            else:
                RecoBaseLocalPath = RecoBaseLocalPath + 'RecoWithTracks/'

            RecoBaseLocalPath1 = RecoBaseLocalPath + Version1 + '/'
            RecoBaseLocalPath2 = RecoBaseLocalPath + Version2 + '/'

            if not am.os.path.exists(RecoBaseLocalPath1): am.os.system('mkdir -p %s' % RecoBaseLocalPath1)
            if not am.os.path.exists(RecoBaseLocalPath2): am.os.system('mkdir -p %s' % RecoBaseLocalPath2)

            if Digitizer == am.DigitizerDict[0] or Digitizer == am.DigitizerDict[1]:
                ListRawRunNumber = [(x.split("_Run")[1].split(".dat")[0].split("_")[0]) for x in am.glob.glob(RawBaseLocalPath + '*_Run*')]
                ListRawFilePath = [x for x in am.glob.glob(RawBaseLocalPath + '*_Run*')] 
                if str(run) in ListRawRunNumber: 
                    RawLocalPath = ListRawFilePath[ListRawRunNumber.index(str(run))]
                    RecoLocalPath1 = RecoBaseLocalPath1 + '/' + RawLocalPath.split(".dat")[0].split("%s" % RawBaseLocalPath)[1] + '.root'    
                    RecoLocalPath2 = RecoBaseLocalPath2 + '/' + RawLocalPath.split(".dat")[0].split("%s" % RawBaseLocalPath)[1] + '.root'                                        
                else:
                    RunNotPresent = True
                    RunsNotPresent.append(run)

            if not RunNotPresent:

                ResultFileLocationList1.append(RecoLocalPath1)
                ResultFileLocationList2.append(RecoLocalPath2)
                DatToRootCMD1 = './' + DatToROOTExec + ' --config_file=' + ConfigFilePath1 + ' --input_file=' + RawLocalPath + ' --output_file=' + RecoLocalPath1
                DatToRootCMD2 = './' + DatToROOTExec + ' --config_file=' + ConfigFilePath2 + ' --input_file=' + RawLocalPath + ' --output_file=' + RecoLocalPath2
                if SaveWaveformBool: 
                    DatToRootCMD1 = DatToRootCMD1 + ' --save_meas'
                    DatToRootCMD2 = DatToRootCMD2 + ' --save_meas'
            
                if DoTracking: 
                    TrackFilePathLocal = am.BaseTrackDirLocal + am.ResultTrackFileNameBeforeRunNumber + str(run) + ResultTrackFileNameAfterRunNumber
                    DatToRootCMD1 = DatToRootCMD1 + ' --pixel_input_file=' + TrackFilePathLocal
                    DatToRootCMD2 = DatToRootCMD2 + ' --pixel_input_file=' + TrackFilePathLocal   

                DatToRootCMDList1.append(DatToRootCMD1)
                DatToRootCMDList2.append(DatToRootCMD2)

        #Remove the runs which were not present
        for run in RunsNotPresent:
            print 'Run %d not present in the raw files' % run
            del FieldIDList[RunList.index(run)]
            RunList.remove(run)

        return DatToRootCMDList1, DatToRootCMDList2, ResultFileLocationList1, ResultFileLocationList2, RunList, FieldIDList

    else:
        return None,None,None,None,None

def TimingDAQCMDsBTL(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, Debug):
    DoTracking = DoTracking 
    MyKey = MyKey
    Digitizer = Digitizer
    RunNumber = RunNumber

    RunList, FieldIDList = pr.TimingDAQRuns(RunNumber, DoTracking, Digitizer, MyKey, False)
    DatToRootCMDList = []
    ResultFileLocationList = []
    RunsNotPresent = []

    if RunList != None:
        
        for run in RunList: 

            RecoLocalPath = None
            RunNotPresent = False
            RawLocalPath = None
            Index = RunList.index(run)
            GlobalConfig = pf.GetConfigNumberFromConfig(run, False, MyKey)

            if Digitizer == am.DigitizerDict[0] or Digitizer == am.DigitizerDict[1] or Digitizer == am.DigitizerDict[5]:
                if Digitizer == am.DigitizerDict[5] and DoTracking:
                    RecoBaseLocalPath = am.OneStageRecoDigitizers[Digitizer]['RecoTimingDAQLocalPath']
                    RawBaseLocalPath1 = am.OneStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath']
                    RawBaseLocalPath2 = am.OneStageRecoDigitizers[Digitizer]['RecoTimingDAQLocalPath']
                    DatToROOTExec1 = am.OneStageRecoDigitizers[Digitizer]['DatToROOTExec1']
                    DatToROOTExec2 = am.OneStageRecoDigitizers[Digitizer]['DatToROOTExec2']
                    ResultTrackFileNameAfterRunNumber = am.ResultTrackFileNameAfterRunNumberFast
                else:
                    RecoBaseLocalPath = am.OneStageRecoDigitizers[Digitizer]['RecoTimingDAQLocalPath']
                    RawBaseLocalPath = am.OneStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath']
                    DatToROOTExec = am.OneStageRecoDigitizers[Digitizer]['DatToROOTExec']
                    ResultTrackFileNameAfterRunNumber = am.ResultTrackFileNameAfterRunNumberSlow
                if Digitizer == am.DigitizerDict[5]:
                    ConfigFilePath = am.OneStageRecoDigitizers[Digitizer]['ConfigFileBasePath'] +  str(GlobalConfig) + '/config.ini'
                else:
                    ConfigFilePath = am.OneStageRecoDigitizers[Digitizer]['ConfigFileBasePath'] + '%s.config' % Version

            else:
                ConfigFilePath = am.TwoStageRecoDigitizers[Digitizer]['ConfigFileBasePath'] + '%s.config' % Version
                RecoBaseLocalPath = am.TwoStageRecoDigitizers[Digitizer]['RecoTimingDAQLocalPath']
                RawBaseLocalPath = am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath']
                DatToROOTExec = am.TwoStageRecoDigitizers[Digitizer]['DatToROOTExec']
                ResultTrackFileNameAfterRunNumber = am.ResultTrackFileNameAfterRunNumberFast

            if not DoTracking: 
                RecoBaseLocalPath = RecoBaseLocalPath + 'RecoWithoutTracks/'
            else:
                if Digitizer == am.DigitizerDict[5]:
                    RecoBaseLocalPath1 = RecoBaseLocalPath + 'RecoWithTracks/'
                    RecoBaseLocalPath2 = RecoBaseLocalPath + 'RecoWithTracks/'
                    RawBaseLocalPath2 = RawBaseLocalPath + 'RecoWithTracks/'
                else:
                    RecoBaseLocalPath = RecoBaseLocalPath + 'RecoWithTracks/'

            if Digitizer != am.DigitizerDict[5]: RecoBaseLocalPath = RecoBaseLocalPath + Version + '/' #### For everything except TOFHIR

            if not am.os.path.exists(RecoBaseLocalPath): am.os.system('mkdir -p %s' % RecoBaseLocalPath)
            if Digitizer == am.DigitizerDict[0] or Digitizer == am.DigitizerDict[1]:
                ListRawRunNumber = [(x.split("_Run")[1].split(".dat")[0].split("_")[0]) for x in am.glob.glob(RawBaseLocalPath + '*_Run*')]
                ListRawFilePath = [x for x in am.glob.glob(RawBaseLocalPath + '*_Run*')] 
                if str(run) in ListRawRunNumber: 
                    RawLocalPath = ListRawFilePath[ListRawRunNumber.index(str(run))]
                    RecoLocalPath = RecoBaseLocalPath + '/' + RawLocalPath.split(".dat")[0].split("%s" % RawBaseLocalPath)[1] + '.root'                                            
                else:
                    RunNotPresent = True
                    RunsNotPresent.append(run) 

            elif Digitizer == am.DigitizerDict[5] and not DoTracking:
                RawLocalPath = RawBaseLocalPath + am.OneStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat'] + str(run)                                      
                RecoLocalPath = RecoBaseLocalPath + '/' + am.OneStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat']+ str(run) + '.root' 
            elif Digitizer == am.DigitizerDict[5] and DoTracking:
                RawLocalPath1 = RawBaseLocalPath1 + am.OneStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat'] + str(run) 
                RawLocalPath2 = RawBaseLocalPath2 + am.OneStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat'] + str(run) + '_singles.root'                                   
                RecoLocalPath1 = RecoBaseLocalPath1 + '/' + am.OneStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat']+ str(run) + '_singles.root'
                RecoLocalPath2 = RecoBaseLocalPath2 + '/' + am.OneStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat']+ str(run) + '_events.root'  

            else:
                RawLocalPath = RawBaseLocalPath + am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat'] + str(run) + '.root'                                      
                RecoLocalPath = RecoBaseLocalPath + '/' + am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat']+ str(run) + '_converted.root' 

            if not RunNotPresent:

                ResultFileLocationList.append(RecoLocalPath)
                if Digitizer == am.DigitizerDict[5] and not DoTracking:
                    DatToRootCMD = './' + DatToROOTExec + ' --config ' + ConfigFilePath + ' -i ' + RawLocalPath + ' -o ' + RecoLocalPath + ' --writeRoot --channelIDs 0,1,6,8,14,15,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,384'
                elif Digitizer != am.DigitizerDict[5]:
                    DatToRootCMD = './' + DatToROOTExec + ' --config_file=' + ConfigFilePath + ' --input_file=' + RawLocalPath + ' --output_file=' + RecoLocalPath
                if SaveWaveformBool and Digitizer != am.DigitizerDict[5]: DatToRootCMD = DatToRootCMD + ' --save_meas'
            
                if DoTracking: 
                    TrackFilePathLocal = am.BaseTrackDirLocal + am.ResultTrackFileNameBeforeRunNumber + str(run) + ResultTrackFileNameAfterRunNumber
                    if Digitizer == am.DigitizerDict[5]:
                        DatToRootCMD1 = './' + DatToROOTExec1 + ' --config ' + ConfigFilePath + ' -i ' + RawLocalPath1 + ' -o ' + RecoLocalPath1 + ' --writeRoot'
                        DatToRootCMD2 = './' + DatToROOTExec2 + ' ' + RawLocalPath2 + ' ' + TrackFilePathLocal + ' ' + RecoLocalPath2
                    else:
                        DatToRootCMD = DatToRootCMD + ' --pixel_input_file=' + TrackFilePathLocal
                DatToRootCMDList.append(DatToRootCMD)

        #Remove the runs which were not present
        for run in RunsNotPresent:
            print 'Run %d not present in the raw files' % run
            del FieldIDList[RunList.index(run)]
            RunList.remove(run)

        return DatToRootCMDList, ResultFileLocationList, RunList, FieldIDList

    else:
        return None,None,None,None 

def TimingDAQCMDsBTLForTOFHIRTracks(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, Debug):
    DoTracking = DoTracking 
    MyKey = MyKey
    Digitizer = Digitizer
    RunNumber = RunNumber

    RunList, FieldIDList = pr.TimingDAQRuns(RunNumber, DoTracking, Digitizer, MyKey, False)
    RunsNotPresent = []
    DatToRootCMDList1 = []
    DatToRootCMDList2 = []
    ResultFileLocationList = []

    if RunList != None:
        
        for run in RunList: 

            RecoLocalPath = None
            RunNotPresent = False
            RawLocalPath = None
            Index = RunList.index(run)
            GlobalConfig = pf.GetConfigNumberFromConfig(run, False, MyKey)

            if Digitizer == am.DigitizerDict[0] or Digitizer == am.DigitizerDict[1] or Digitizer == am.DigitizerDict[5]:
                if Digitizer == am.DigitizerDict[5] and DoTracking:
                    RecoBaseLocalPath = am.OneStageRecoDigitizers[Digitizer]['RecoTimingDAQLocalPath']
                    RawBaseLocalPath1 = am.OneStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath']
                    RawBaseLocalPath2 = am.OneStageRecoDigitizers[Digitizer]['RecoTimingDAQLocalPath']
                    DatToROOTExec1 = am.OneStageRecoDigitizers[Digitizer]['DatToROOTExec1']
                    DatToROOTExec2 = am.OneStageRecoDigitizers[Digitizer]['DatToROOTExec2']
                    ResultTrackFileNameAfterRunNumber = am.ResultTrackFileNameAfterRunNumberFast
                else:
                    RecoBaseLocalPath = am.OneStageRecoDigitizers[Digitizer]['RecoTimingDAQLocalPath']
                    RawBaseLocalPath = am.OneStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath']
                    DatToROOTExec = am.OneStageRecoDigitizers[Digitizer]['DatToROOTExec']
                    ResultTrackFileNameAfterRunNumber = am.ResultTrackFileNameAfterRunNumberSlow
                if Digitizer == am.DigitizerDict[5]:
                    ConfigFilePath = am.OneStageRecoDigitizers[Digitizer]['ConfigFileBasePath'] +  str(GlobalConfig) + '/config.ini'
                else:
                    ConfigFilePath = am.OneStageRecoDigitizers[Digitizer]['ConfigFileBasePath'] + '%s.config' % Version

            else:
                ConfigFilePath = am.TwoStageRecoDigitizers[Digitizer]['ConfigFileBasePath'] + '%s.config' % Version
                RecoBaseLocalPath = am.TwoStageRecoDigitizers[Digitizer]['RecoTimingDAQLocalPath']
                RawBaseLocalPath = am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath']
                DatToROOTExec = am.TwoStageRecoDigitizers[Digitizer]['DatToROOTExec']
                ResultTrackFileNameAfterRunNumber = am.ResultTrackFileNameAfterRunNumberFast

            if not DoTracking: 
                RecoBaseLocalPath = RecoBaseLocalPath + 'RecoWithoutTracks/'
            else:
                if Digitizer == am.DigitizerDict[5]:
                    RecoBaseLocalPath1 = RecoBaseLocalPath + 'RecoWithTracks/'
                    RecoBaseLocalPath2 = RecoBaseLocalPath + 'RecoWithTracks/'
                    RawBaseLocalPath2 = RawBaseLocalPath2 + 'RecoWithTracks/'
                else:
                    RecoBaseLocalPath = RecoBaseLocalPath + 'RecoWithTracks/'

            if Digitizer != am.DigitizerDict[5]: RecoBaseLocalPath = RecoBaseLocalPath + Version + '/' #### For everything except TOFHIR

            if not am.os.path.exists(RecoBaseLocalPath): am.os.system('mkdir -p %s' % RecoBaseLocalPath)
            if Digitizer == am.DigitizerDict[0] or Digitizer == am.DigitizerDict[1]:
                ListRawRunNumber = [(x.split("_Run")[1].split(".dat")[0].split("_")[0]) for x in am.glob.glob(RawBaseLocalPath + '*_Run*')]
                ListRawFilePath = [x for x in am.glob.glob(RawBaseLocalPath + '*_Run*')] 
                if str(run) in ListRawRunNumber: 
                    RawLocalPath = ListRawFilePath[ListRawRunNumber.index(str(run))]
                    RecoLocalPath = RecoBaseLocalPath + '/' + RawLocalPath.split(".dat")[0].split("%s" % RawBaseLocalPath)[1] + '.root'                                            
                else:
                    RunNotPresent = True
                    RunsNotPresent.append(run) 

            elif Digitizer == am.DigitizerDict[5] and not DoTracking:
                RawLocalPath = RawBaseLocalPath + am.OneStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat'] + str(run)                                      
                RecoLocalPath = RecoBaseLocalPath + '/' + am.OneStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat']+ str(run) + '.root' 
            elif Digitizer == am.DigitizerDict[5] and DoTracking:
                RawLocalPath1 = RawBaseLocalPath1 + am.OneStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat'] + str(run) 
                RawLocalPath2 = RawBaseLocalPath2 + am.OneStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat'] + str(run) + '_singles.root'                                   
                RecoLocalPath1 = RecoBaseLocalPath1 + '/' + am.OneStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat']+ str(run) + '_singles.root'
                RecoLocalPath2 = RecoBaseLocalPath2 + '/' + am.OneStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat']+ str(run) + '_events.root'  

            else:
                RawLocalPath = RawBaseLocalPath + am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat'] + str(run) + '.root'                                      
                RecoLocalPath = RecoBaseLocalPath + '/' + am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat']+ str(run) + '_converted.root' 

            if not RunNotPresent:

                ResultFileLocationList.append(RecoLocalPath2)
                if Digitizer == am.DigitizerDict[5] and not DoTracking:
                    DatToRootCMD = './' + DatToROOTExec + ' --config ' + ConfigFilePath + ' -i ' + RawLocalPath + ' -o ' + RecoLocalPath + ' --writeRoot --channelIDs 0,1,6,8,14,15,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,384'
                elif Digitizer != am.DigitizerDict[5]:
                    DatToRootCMD = './' + DatToROOTExec + ' --config_file=' + ConfigFilePath + ' --input_file=' + RawLocalPath + ' --output_file=' + RecoLocalPath
                if SaveWaveformBool and Digitizer != am.DigitizerDict[5]: DatToRootCMD = DatToRootCMD + ' --save_meas'
            
                if DoTracking: 
                    TrackFilePathLocal = am.BaseTrackDirLocal + am.ResultTrackFileNameBeforeRunNumber + str(run) + ResultTrackFileNameAfterRunNumber
                    if Digitizer == am.DigitizerDict[5]:
                        DatToRootCMD1 = './' + DatToROOTExec1 + ' --config ' + ConfigFilePath + ' -i ' + RawLocalPath1 + ' -o ' + RecoLocalPath1 + ' --writeRoot'
                        DatToRootCMD2 = './' + DatToROOTExec2 + ' ' + RawLocalPath2 + ' ' + TrackFilePathLocal + ' ' + RecoLocalPath2
                    else:
                        DatToRootCMD = DatToRootCMD + ' --pixel_input_file=' + TrackFilePathLocal
                DatToRootCMDList1.append(DatToRootCMD1)
                DatToRootCMDList2.append(DatToRootCMD2)

        #Remove the runs which were not present
        for run in RunsNotPresent:
            print 'Run %d not present in the raw files' % run
            del FieldIDList[RunList.index(run)]
            RunList.remove(run)

        return DatToRootCMDList1, DatToRootCMDList2, ResultFileLocationList, RunList, FieldIDList

    else:
        return None,None,None,None,None


