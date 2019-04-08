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

    if RunList:
        
        for run in RunList: 

            TrackingCMDList.append('source %s %d' % (am.HyperscriptPath, run)) #####Modify Hyperscript to scp the result file on the local machine
            ResultFileLocationList.append(am.BaseTrackDirLocal + am.ResultTrackFileNameBeforeRunNumber + str(run) + am.ResultTrackFileNameAfterRunNumber)

    return TrackingCMDList, ResultFileLocationList, RunList, FieldIDList


def ConversionCMDs(RunNumber, Digitizer, MyKey, Debug):
    MyKey = MyKey
    RunNumber = RunNumber
    Digitizer = Digitizer

    RunList, FieldIDList = pr.ConversionRuns(RunNumber, Digitizer, MyKey, False)
    ConversionCMDList = []
    ResultFileLocationList = []

    if RunList:
        
        for run in RunList: 

            ConversionCMDList.append(am.TwoStageRecoDigitizers[Digitizer]['ConversionCMD'] + str(run))
            ResultFileLocationList.append(am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath'] + am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat'] + str(run) + '.root')

    return ConversionCMDList, ResultFileLocationList, RunList, FieldIDList


def TimingDAQCMDs(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, Debug):
    DoTracking = DoTracking 
    MyKey = MyKey
    Digitizer = Digitizer
    RunNumber = RunNumber
    RunList, FieldIDList = pr.TimingDAQRuns(RunNumber, DoTracking, Digitizer, MyKey, False)
    DatToRootCMDList = []
    ResultFileLocationList = []

    if RunList:
        
        for run in RunList: 

            RecoLocalPath = None
            RawLocalPath = None
            Index = RunList.index(run)

            if Digitizer == am.DigitizerDict[0] or Digitizer == am.DigitizerDict[1]:
                RecoBaseLocalPath = am.OneStageRecoDigitizers[Digitizer]['RecoTimingDAQLocalPath']
                RawBaseLocalPath = am.OneStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath']
                ConfigFilePath = am.OneStageRecoDigitizers[Digitizer]['ConfigFileBasePath'] + '_%s.config' % Version
                DatToROOTExec = am.OneStageRecoDigitizers[Digitizer]['DatToROOTExec']
            else:
                RecoBaseLocalPath = am.TwoStageRecoDigitizers[Digitizer]['RecoTimingDAQLocalPath']
                RawBaseLocalPath = am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath']
                ConfigFilePath = am.TwoStageRecoDigitizers[Digitizer]['ConfigFileBasePath'] + '_%s.config' % Version
                DatToROOTExec = am.TwoStageRecoDigitizers[Digitizer]['DatToROOTExec']

            if not DoTracking: 
                RecoBaseLocalPath = RecoBaseLocalPath + 'RecoWithoutTracks/'
            else:
                RecoBaseLocalPath = RecoBaseLocalPath + 'RecoWithTracks/'

            RecoBaseLocalPath = RecoBaseLocalPath + Version

            if not am.os.path.exists(RecoBaseLocalPath): am.os.system('mkdir -p %s' % RecoBaseLocalPath)

            if Digitizer == am.DigitizerDict[0] or Digitizer == am.DigitizerDict[1]:
                ListRawRunNumber = [(x.split("_Run")[1].split(".dat")[0].split("_")[0]) for x in am.glob.glob(RawBaseLocalPath + '*_Run*')]
                ListRawFilePath = [x for x in am.glob.glob(RawBaseLocalPath + '*_Run*')] 
                RawLocalPath = ListRawFilePath[ListRawRunNumber.index(run)]
                RecoLocalPath = RecoBaseLocalPath + RawLocalPath.split(".dat")[0].split("%s/" % Version)[1] + '.root'                                            
            else:
                RawLocalPath =  RawBaseLocalPath + am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat'] + str(run) + '.root'                                      
                RecoLocalPath = RecoBaseLocalPath + am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat']+ str(run) + '_converted.root' 

            ResultFileLocationList.append(RecoLocalPath)
            
            DatToRootCMD = './' + DatToROOTExec + ' --config_file=' + ConfigFilePath + ' --input_file=' + RawLocalPath + ' --output_file=' + RecoLocalPath
            if SaveWaveformBool: DatToRootCMD = DatToRootCMD + ' --save_meas'
            
            if DoTracking: 
                TrackFilePathLocal = am.BaseTrackDirLocal + 'Run%i_CMSTiming_converted.root' % run
                DatToRootCMD = DatToRootCMD + ' --pixel_input_file=' + TrackFilePathLocal   

            DatToRootCMDList.append(DatToRootCMD)

        return DatToRootCMDList, ResultFileLocationList, RunList, FieldIDList




