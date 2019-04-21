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

def ConversionCMDs(RunNumber, Digitizer, MyKey, Debug):
    MyKey = MyKey
    RunNumber = RunNumber
    Digitizer = Digitizer

    RunList, FieldIDList = pr.ConversionRuns(RunNumber, Digitizer, MyKey, False)
    ConversionCMDList = []
    ResultFileLocationList = []

    if RunList != None:
        
        for run in RunList: 

            ConversionCMDList.append(am.TwoStageRecoDigitizers[Digitizer]['ConversionCMD'] + str(run))
            ResultFileLocationList.append(am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath'] + am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat'] + str(run) + '.root')
        return ConversionCMDList, ResultFileLocationList, RunList, FieldIDList

    else:
        return None,None,None,None   



def TimingDAQCMDs(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, Debug):
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


def TimingDAQCMDsBTL(RunNumber, SaveWaveformBool, Version1, Version2, DoTracking, Digitizer, MyKey, Debug):
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

