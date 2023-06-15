import AllModules as am
import json as js
################################################################################################################################################################################################################                                                                         
################################################################################################################################################################################################################                                                                         
#########################################These Functions parse the run table and performs function such as record query,  record update, record Addition etc ###################################################
################################################################################################################################################################################################################                                           
################################################################################################################################################################################################################           
    

################### Unicode Operations to form CURL commands ###################

def QueryAllow():

    QueryFile = open(am.QueryFilePath,"a+") 
    ScanLines = [line.rstrip('\n') for line in open(am.QueryFilePath)]
 
    QueryNumberList = []
    QueryTimeList = [] 
    TimeToWait = -1

    if ScanLines:
       for entry in ScanLines:
            if ScanLines.index(entry) % 2 == 0:
                QueryNumberList.append(int(entry))
            else:
                QueryTimeList.append(entry) #Absolute time 
    else:
        QueryNumberList.append(0)

    LastQueryNumber = QueryNumberList[len(QueryNumberList - 1)]
    if  LastQueryNumber < 5:
        AllowQuery = True
        QueryFile.write(str(LastQueryNumber + 1) + "\n")  
        QueryFile.write(str(datetime.now()) + "\n")
        QueryFile.close() 

    elif LastQueryNumber == 5:
        TimeSinceFirstQuery = (datetime.now() - datetime.strptime(QueryTimeList[0],"%Y-%m-%d %H:%M:%S.%f")).total_seconds()
        if TimeSinceFirstQuery > 60:
            AllowQuery = True
            os.system("rm %s" % am.QueryFilePath)
            QueryFile = open(am.QueryFilePath,"a+") 
            QueryFile.write(str(1) + "\n")  
            QueryFile.write(str(datetime.now()) + "\n")
            QueryFile.close()
        else:
            TimeToWait = 65 - TimeSinceFirstQuery
            AllowQuery = False
    
    return AllowQuery, TimeToWait 

def QueryGreenSignal(Bypass):
    while True:
        if Bypass == True:
            return True
            break
        IsQueryAllowed, TimeToWait = QueryAllow()
        if IsQueryAllowed: 
            return True
            break
        else:
           time.sleep(TimeToWait)

def DoubleQuotes(string):
    return '%%22%s%%22' % string 

def Curly(string):
    return '%%7B%s%%7D' % string
    
def EqualToFunc(string1,string2):
    return '%s%%3D%s' % (string1,string2)

def ANDFunc(AttributeNameList, AttributeStatusList):
    Output = 'AND('
    index = 0
    for AttributeName in AttributeNameList:
        AttributeStatus = AttributeStatusList[index]
        Condition = EqualToFunc(Curly(AttributeName), DoubleQuotes(AttributeStatus))
        if index > 0: Output = Output + ','
        Output = Output + Condition
        index = index + 1
    Output = Output + ')'
    return Output
 
def ORFunc(AttributeNameList, AttributeStatusList):
    Output = 'OR('
    index = 0 
    for AttributeName in AttributeNameList:
        AttributeStatus = AttributeStatusList[index]
        Condition = EqualToFunc(Curly(AttributeName), DoubleQuotes(AttributeStatus))
        if index > 0: Output = Output + ','
        Output = Output + Condition
        index = index + 1
    Output = Output + ')'
    return Output

def DownloadRuntable(Debug,MyKey):
    headers = {'Authorization': 'Bearer %s' % MyKey, }

    RunTableResponse = am.requests.get(am.CurlBaseCommandRunTable, headers=headers)
    RunTableDict = am.ast.literal_eval(RunTableResponse.text)

    runTableFileName = am.LocalConfigPath+"RunTable.txt"
    gfile = open(runTableFileName, "w")
    js.dump(RunTableDict, gfile)
    gfile.close()
    return RunTableDict


def DownloadConfigs(Debug, MyKey):
    headers = {'Authorization': 'Bearer %s' % MyKey, }
    
    ConfigResponse = am.requests.get(am.CurlBaseCommandConfig, headers=headers)
    ConfigDict = am.ast.literal_eval(ConfigResponse.text)

    LecroyResponse = am.requests.get(am.CurlBaseCommandLecroy, headers=headers)
    LecroyDict = am.ast.literal_eval(LecroyResponse.text)

    KeySightResponse = am.requests.get(am.CurlBaseCommandKeySight, headers=headers)
    KeySightDict = am.ast.literal_eval(KeySightResponse.text)

    TOFHIRResponse = am.requests.get(am.CurlBaseCommandTOFHIR, headers=headers)
    TOFHIRDict = am.ast.literal_eval(TOFHIRResponse.text)

    CAENResponse = am.requests.get(am.CurlBaseCommandCAEN, headers=headers)
    CAENDict = am.ast.literal_eval(CAENResponse.text)

    SensorResponse = am.requests.get(am.CurlBaseCommandSensor, headers=headers)
    SensorDict = am.ast.literal_eval(SensorResponse.text)


    globalDictFileName = am.LocalConfigPath+"Configurations.txt"
    gfile = open(globalDictFileName, "w")
    js.dump(ConfigDict, gfile)
    gfile.close()

    LecroyDictFileName = am.LocalConfigPath+"LecroyConfigurations.txt"
    lfile = open(LecroyDictFileName, "w")
    js.dump(LecroyDict, lfile)
    lfile.close()

    KeySightDictFileName = am.LocalConfigPath+"KeySightConfigurations.txt"
    kfile = open(KeySightDictFileName, "w")
    js.dump(KeySightDict, kfile)
    kfile.close()

    TOFHIRDictFileName = am.LocalConfigPath+"TOFHIRConfigurations.txt"
    kfile = open(TOFHIRDictFileName, "w")
    js.dump(TOFHIRDict, kfile)
    kfile.close()

    CAENDictFileName = am.LocalConfigPath+"CAENConfigurations.txt"
    cfile = open(CAENDictFileName, "w")
    js.dump(CAENDict, cfile)
    cfile.close()

    SensorDictFileName = am.LocalConfigPath+"SensorConfigurations.txt"
    sensorfile = open(SensorDictFileName, "w")
    js.dump(SensorDict, sensorfile)
    sensorfile.close()

    return ConfigDict, LecroyDict,KeySightDict, TOFHIRDict,CAENDict,SensorDict

def getSensorById(SensorDict,idnum):
    for item in SensorDict['records']: 
        if item['id']==idnum:
            return item['fields']['Name no commas allowed']

def getConfigsByGConf(ConfigDict,gconf):
    for item in ConfigDict['records']:
        if item['fields']['Configuration number']==gconf:
            lecroyConfID = item['fields']['ConfigurationLecroyScope'][0]
            caenConfID = item['fields']['ConfigurationCAENHV'][0]
            return lecroyConfID,caenConfID

def getConfigsByGConfTOFHIR(ConfigDict,gconf):
    for item in ConfigDict['records']:
        if item['fields']['Configuration number']==gconf:
            tofhirConfID = item['fields']['ConfigurationTOFHIR'][0]
            return tofhirConfID

def getSimpleLecroyDict(LecroyDict,SensorDict,lecroyConfID):
    for item in LecroyDict['records']: 
        if item['id']==lecroyConfID:
            simpleLecroyDict =  item['fields']
            for key in simpleLecroyDict: 
                if "Sensor" in key:
                    simpleLecroyDict[key] = getSensorById(SensorDict,simpleLecroyDict[key][0])
        # print key, test['records'][0]['fields'][key]
            return simpleLecroyDict

def getSimpleCAENDict(CAENDict,SensorDict,caenConfID):
    for item in CAENDict['records']: 
        if item['id']==caenConfID:
            simpleCAENDict =  item['fields']
            for key in simpleCAENDict: 
                if "Sensor" in key:
                    simpleCAENDict[key] = getSensorById(SensorDict,simpleCAENDict[key][0])
        # print key, test['records'][0]['fields'][key]
            return simpleCAENDict


##################### Main Run Table Operaton functions #########################

def ParsingQuery(NumberOfConditions, ConditionAttributeNames, ConditionAttributeStatus, QueryAttributeName, Debug, MyKey):
    Output = [] 
    FieldID = []
    FilterByFormula = ''
    headers = {'Authorization': 'Bearer %s' % MyKey, }
    for i in range (0, NumberOfConditions): 
        if i > 0: FilterByFormula = FilterByFormula + ','
        FilterByFormula = FilterByFormula + EqualToFunc(Curly(ConditionAttributeNames[i]), DoubleQuotes(ConditionAttributeStatus[i])) 
    if NumberOfConditions > 1: FilterByFormula = 'AND(' + FilterByFormula + ')'
    response = am.requests.get(am.CurlBaseCommand  + '?filterByFormula=' + FilterByFormula, headers=headers)
    ResponseDict = am.ast.literal_eval(response.text)
    if Debug: print(FilterByFormula)

    for i in ResponseDict["records"]: Output.append(i['fields'][QueryAttributeName])   
    for i in ResponseDict["records"]: FieldID.append(i['id'])   
    return Output, FieldID

def ParsingQuery2(NumberOfConditions, ConditionAttributeNames, ConditionAttributeStatus, QueryAttributeName, Debug, MyKey):
    Output = [] 
    FieldID = []
    FilterByFormula = ''
    headers = {'Authorization': 'Bearer %s' % MyKey, }
    for i in range (0, NumberOfConditions): 
        if i > 0: FilterByFormula = FilterByFormula + ','
        FilterByFormula = FilterByFormula + EqualToFunc(Curly(ConditionAttributeNames[i]), DoubleQuotes(ConditionAttributeStatus[i])) 
    if NumberOfConditions > 1: FilterByFormula = 'AND(' + FilterByFormula + ')'
    response = am.requests.get(am.CurlBaseCommandConfig  + '?filterByFormula=' + FilterByFormula, headers=headers)
    ResponseDict = am.ast.literal_eval(response.text)
    if Debug: return ResponseDict, FilterByFormula

    for i in ResponseDict["records"]: Output.append(i['fields'][QueryAttributeName])   
    for i in ResponseDict["records"]: FieldID.append(i['id'])   
    return Output[0]

def ParsingQuery3(NumberOfConditions, ConditionAttributeNameList, ConditionAttributeStatusList, QueryAttributeNameList, Debug, MyKey):
    OutputDict = {x: [] for x in range(len(QueryAttributeNameList))}
    FieldID = []
    FilterByFormula = ''
    headers = {'Authorization': 'Bearer %s' % MyKey, }
    for i in range (0, NumberOfConditions): 
        if i > 0: FilterByFormula = FilterByFormula + ','
        FilterByFormula = FilterByFormula + EqualToFunc(Curly(ConditionAttributeNameList[i]), DoubleQuotes(ConditionAttributeStatusList[i])) 
    if NumberOfConditions > 1: FilterByFormula = 'AND(' + FilterByFormula + ')'
    response = am.requests.get(am.CurlBaseCommand  + '?filterByFormula=' + FilterByFormula, headers=headers)
    ResponseDict = am.ast.literal_eval(response.text)
    if Debug: print(FilterByFormula)
    for key,value in OutputDict.items():
        for i in ResponseDict["records"]:
            value.append(i['fields'][QueryAttributeNameList[key]])
    return OutputDict

def GetDigiFromConfig(ConfigurationNumber, Debug, MyKey):
    Output = [] 
    FieldID = []
    DigitizerList = []
    headers = {'Authorization': 'Bearer %s' % MyKey}
    CurlBaseCommand = am.CurlBaseCommandConfig
    FilterByFormula = EqualToFunc(Curly('Configuration number'), DoubleQuotes(ConfigurationNumber)) 

    response = am.requests.get(CurlBaseCommand  + '?filterByFormula=' + FilterByFormula, headers=headers)
    ResponseDict = am.ast.literal_eval(response.text)
    if Debug: return ResponseDict, FilterByFormula
    ListOfFields = ResponseDict["records"][0]['fields'].keys()
    for k , Digitizer in am.DigitizerDict.items():
         if any(Digitizer in fields for fields in ListOfFields):
            DigitizerList.append(Digitizer)
    return DigitizerList

def GetConfigNumberFromConfig(RunNumber, Debug, MyKey):

    headers = {'Authorization': 'Bearer %s' % MyKey}
    CurlBaseCommand = am.CurlBaseCommandConfig
    GlobalConfigIDList, RecordID = ParsingQuery(1, ["Run number"], [RunNumber], "Configuration", False, MyKey)
    GlobalConfigID = GlobalConfigIDList[0][0]

    response = am.requests.get(CurlBaseCommand  + '/' + GlobalConfigID, headers=headers)
    ResponseDict = am.ast.literal_eval(response.text)
    if Debug: return ResponseDict
    ConfigurationNumber = ResponseDict["fields"]['Configuration number']   
    return ConfigurationNumber

def GetFieldID(ConditionAttributeName, ConditionAttributeStatus, Debug, MyKey):
    Output = [] 
    FilterByFormula = EqualToFunc(Curly(ConditionAttributeName), DoubleQuotes(ConditionAttributeStatus))
    headers = {'Authorization': 'Bearer %s' % MyKey, }
    response = am.requests.get(am.CurlBaseCommand  + '?filterByFormula=' + FilterByFormula, headers=headers)
    ResponseDict = am.ast.literal_eval(response.text)
    if Debug: return ResponseDict, FilterByFormula

    for i in ResponseDict["records"]: Output.append(i['id'])   
    return Output

def UpdateAttributeStatus(FieldID, UpdateAttributeName, UpdateAttributeStatus, Debug, MyKey):
    headers = {
        'Authorization': 'Bearer %s' % MyKey, 
        'Content-Type': 'application/json',
    }
    data = '{"fields":{"%s": ["%s"]}}' % (UpdateAttributeName,UpdateAttributeStatus)
    
    # print(data)

    response = am.requests.patch(am.CurlBaseCommand + '/' + FieldID, headers=headers, data=data)
    ResponseDict = am.ast.literal_eval(response.text)
    if Debug: return ResponseDict

def UpdateAttributeStatus2(FieldID, UpdateAttributeName, UpdateAttributeStatus, Debug, MyKey):
    headers = {
        'Authorization': 'Bearer %s' % MyKey, 
        'Content-Type': 'application/json',
    }
    data = '{"fields":{"%s": %d}}' % (UpdateAttributeName,UpdateAttributeStatus)
    response = am.requests.patch(am.CurlBaseCommand + '/' + FieldID, headers=headers, data=data)
    ResponseDict = am.ast.literal_eval(response.text)
    if Debug: return ResponseDict

def GetFieldIDOtherTable(TableName,ConditionAttributeName, ConditionAttributeStatus, Debug, MyKey):     
    if TableName == 'Sensor' :
        CurlBaseCommand = am.CurlBaseCommandSensor
    elif TableName == 'Config':
        CurlBaseCommand = am.CurlBaseCommandConfig
    Output = [] 
    FilterByFormula = EqualToFunc(Curly(ConditionAttributeName), DoubleQuotes(ConditionAttributeStatus))
    headers = {'Authorization': 'Bearer %s' % MyKey, }
    response = am.requests.get(CurlBaseCommand  + '?filterByFormula=' + FilterByFormula, headers=headers)
    ResponseDict = am.ast.literal_eval(response.text)
    if Debug: return ResponseDict, FilterByFormula
    for i in ResponseDict["records"]: Output.append(i['id'])   
    return Output

def NewRunRecord(RunNumber, StartTime, Duration, DigitizerList, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, LabviewRecoVME, LabviewRecoDT5742, LabviewRecoKeySightScope, LabviewRecoSampic, LabviewRecoTekScope, ConfigID, Debug, MyKey):
    #NewRunRecord(RunNumber, DigitizerList, Debug)
    headers = {
        'Authorization': 'Bearer %s' % MyKey, 
        'Content-Type': 'application/json',
    }

    if len(DigitizerList) == 1:
        Digitizer1 = DigitizerList[0]
        data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": ["%s"], "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"],"TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"], "LabviewRecoVME": ["%s"], "LabviewRecoDT5742": ["%s"], "LabviewRecoKeySightScope": ["%s"], "LabviewRecoSampic": ["%s"], "LabviewRecoTekScope": ["%s"], "Configuration": ["%s"]}}' % (RunNumber, StartTime, Duration, Digitizer1, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, LabviewRecoVME, LabviewRecoDT5742, LabviewRecoKeySightScope, LabviewRecoSampic, LabviewRecoTekScope, ConfigID[0])
    elif len(DigitizerList) == 2:
        Digitizer1 = DigitizerList[0]
        Digitizer2 = DigitizerList[1]
        data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": ["%s","%s"], "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"],"TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"], "LabviewRecoVME": ["%s"], "LabviewRecoDT5742": ["%s"], "LabviewRecoKeySightScope": ["%s"], "LabviewRecoSampic": ["%s"], "LabviewRecoTekScope": ["%s"], "Configuration": ["%s"]}}' % (RunNumber, StartTime, Duration, Digitizer1, Digitizer2, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, LabviewRecoVME, LabviewRecoDT5742, LabviewRecoKeySightScope, LabviewRecoSampic, LabviewRecoTekScope, ConfigID[0])
    elif len(DigitizerList) == 3:
        Digitizer1 = DigitizerList[0]
        Digitizer2 = DigitizerList[1]
        Digitizer3 = DigitizerList[2]
        data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": ["%s","%s","%s"], "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"],"TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"], "LabviewRecoVME": ["%s"], "LabviewRecoDT5742": ["%s"], "LabviewRecoKeySightScope": ["%s"], "LabviewRecoSampic": ["%s"], "LabviewRecoTekScope": ["%s"], "Configuration": ["%s"]}}' % (RunNumber, StartTime, Duration, Digitizer1, Digitizer2, Digitizer3, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, LabviewRecoVME, LabviewRecoDT5742, LabviewRecoKeySightScope, LabviewRecoSampic, LabviewRecoTekScope, ConfigID[0])
    elif len(DigitizerList) == 4:
        Digitizer1 = DigitizerList[0]
        Digitizer2 = DigitizerList[1]
        Digitizer3 = DigitizerList[2]
        Digitizer4 = DigitizerList[3]
        data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": ["%s","%s","%s","%s"], "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"],"TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"], "LabviewRecoVME": ["%s"], "LabviewRecoDT5742": ["%s"], "LabviewRecoKeySightScope": ["%s"], "LabviewRecoSampic": ["%s"], "LabviewRecoTekScope": ["%s"], "Configuration": ["%s"]}}' % (RunNumber, StartTime, Duration, Digitizer1, Digitizer2, Digitizer3, Digitizer4, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, LabviewRecoVME, LabviewRecoDT5742, LabviewRecoKeySightScope, LabviewRecoSampic, LabviewRecoTekScope, ConfigID[0])
    elif len(DigitizerList) == 5:
        Digitizer1 = DigitizerList[0]
        Digitizer2 = DigitizerList[1]
        Digitizer3 = DigitizerList[2]
        Digitizer4 = DigitizerList[3]
        Digitizer5 = DigitizerList[4]
        data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": ["%s","%s","%s","%s","%s"], "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"],"TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"], "LabviewRecoVME": ["%s"], "LabviewRecoDT5742": ["%s"], "LabviewRecoKeySightScope": ["%s"], "LabviewRecoSampic": ["%s"], "LabviewRecoTekScope": ["%s"], "Configuration": ["%s"]}}' % (RunNumber, StartTime, Duration, Digitizer1, Digitizer2, Digitizer3, Digitizer4, Digitizer5, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, LabviewRecoVME, LabviewRecoDT5742, LabviewRecoKeySightScope, LabviewRecoSampic, LabviewRecoTekScope, ConfigID[0])

    #Example template of a query response :  {'records': [{'createdTime': '2015-02-12T03:40:42.000Z', 'fields': {'Conversion': ['Complete'], 'Time Resolution 1': 30, 'TimingDAQ': ['Failed'], 'Notes': 'Make test beam great again\n', 'HV 1': ['recJRiQqSHzTNZqal'], 'Run number': 4, 'Tracking': ['Processing'], 'Configuration': ['rectY95k7m19likjW'], 'Sensor': ['recNwdccBdzS7iBa5']}, 'id': 'recNsKOMDvYKrJzXd'}]}
    #data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": ["%s","%s"], "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"],"TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"],"Sensor": ["%s"],"Configuration": ["%s"]}}' % (RunNumber, StartTime, Duration, Digitizer1, Digitizer2, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, SensorID[0], ConfigID[0])
    #data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": %s, "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"],"TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"],"Sensor": ["%s"],"Configuration": ["%s"]}}' % (RunNumber, StartTime, Duration, DigitizerList, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, SensorID[0], ConfigID[0])
    #data = '{"fields":{"Run number": %d, "Digitizer": ["%s","%s"]}}' % (RunNumber, Digitizer1, Digitizer2)
    response = am.requests.post(am.CurlBaseCommand, headers=headers, data=data)
    ResponseDict = am.ast.literal_eval(response.text)
    if Debug: return ResponseDict, data
    


 
def NewRunRecord2(RunNumber, StartTime, Duration, DigitizerList, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQTOFHIR, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, TimingDAQNoTracksTOFHIR, LabviewRecoVME, LabviewRecoDT5742, LabviewRecoKeySightScope, LabviewRecoSampic, LabviewRecoTekScope, BoxTemp, x_stage, y_stage, BoxVoltage, BarCurrent, z_rotation, BoxHum, BoxCurrent, BarVoltage, OverVoltageBTL, VTHBTL, ConfigID, Debug, MyKey):
    headers = {
        'Authorization': 'Bearer %s' % MyKey, 
        'Content-Type': 'application/json',
    }
    data = ""
    if len(DigitizerList) == 1:
        Digitizer1 = DigitizerList[0]
        data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": ["%s"], "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"], "TimingDAQTOFHIR": ["%s"], "TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"], "TimingDAQNoTracksTOFHIR": ["%s"], "LabviewRecoVME": ["%s"], "LabviewRecoDT5742": ["%s"], "LabviewRecoKeySightScope": ["%s"], "LabviewRecoSampic": ["%s"], "LabviewRecoTekScope": ["%s"], "Configuration": ["%s"],"BoxTempOlmo": "%s","x_stageOlmo": "%s","y_stageOlmo": "%s","BoxVoltageOlmo": "%s","BarCurrentOlmo": "%s","z_rotationOlmo": "%s","BoxHumOlmo": "%s","BoxCurrentOlmo": "%s", "BarVoltageOlmo": "%s","OverVoltageBTL": "%s", "VTHBTL": "%s"}}' % (RunNumber, StartTime, Duration, Digitizer1, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQTOFHIR, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, TimingDAQNoTracksTOFHIR, LabviewRecoVME, LabviewRecoDT5742, LabviewRecoKeySightScope, LabviewRecoSampic, LabviewRecoTekScope, ConfigID[0], BoxTemp, x_stage, y_stage, BoxVoltage, BarCurrent, z_rotation, BoxHum, BoxCurrent, BarVoltage, OverVoltageBTL, VTHBTL)
    elif len(DigitizerList) == 2:
        Digitizer1 = DigitizerList[0]
        Digitizer2 = DigitizerList[1]
        data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": ["%s","%s"], "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"], "TimingDAQTOFHIR": ["%s"], "TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"], "TimingDAQNoTracksTOFHIR": ["%s"], "LabviewRecoVME": ["%s"], "LabviewRecoDT5742": ["%s"], "LabviewRecoKeySightScope": ["%s"], "LabviewRecoSampic": ["%s"], "LabviewRecoTekScope": ["%s"], "Configuration": ["%s"],"BoxTempOlmo": "%s","x_stageOlmo": "%s","y_stageOlmo": "%s","BoxVoltageOlmo": "%s","BarCurrentOlmo": "%s","z_rotationOlmo": "%s","BoxHumOlmo": "%s","BoxCurrentOlmo": "%s", "BarVoltageOlmo": "%s","OverVoltageBTL": "%s", "VTHBTL": "%s"}}' % (RunNumber, StartTime, Duration, Digitizer1, Digitizer2, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQTOFHIR, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, TimingDAQNoTracksTOFHIR, LabviewRecoVME, LabviewRecoDT5742, LabviewRecoKeySightScope, LabviewRecoSampic, LabviewRecoTekScope, ConfigID[0], BoxTemp, x_stage, y_stage, BoxVoltage, BarCurrent, z_rotation, BoxHum, BoxCurrent, BarVoltage, OverVoltageBTL, VTHBTL)
    elif len(DigitizerList) == 3:
        Digitizer1 = DigitizerList[0]
        Digitizer2 = DigitizerList[1]
        Digitizer3 = DigitizerList[2]
        data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": ["%s","%s","%s"], "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"], "TimingDAQTOFHIR": ["%s"], "TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"], "TimingDAQNoTracksTOFHIR": ["%s"], "LabviewRecoVME": ["%s"], "LabviewRecoDT5742": ["%s"], "LabviewRecoKeySightScope": ["%s"], "LabviewRecoSampic": ["%s"], "LabviewRecoTekScope": ["%s"], "Configuration": ["%s"],"BoxTempOlmo": "%s","x_stageOlmo": "%s","y_stageOlmo": "%s","BoxVoltageOlmo": "%s","BarCurrentOlmo": "%s","z_rotationOlmo": "%s","BoxHumOlmo": "%s","BoxCurrentOlmo": "%s", "BarVoltageOlmo": "%s","OverVoltageBTL": "%s", "VTHBTL": "%s"}}' % (RunNumber, StartTime, Duration, Digitizer1, Digitizer2, Digitizer3, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQTOFHIR, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, TimingDAQNoTracksTOFHIR, LabviewRecoVME, LabviewRecoDT5742, LabviewRecoKeySightScope, LabviewRecoSampic, LabviewRecoTekScope, ConfigID[0], BoxTemp, x_stage, y_stage, BoxVoltage, BarCurrent, z_rotation, BoxHum, BoxCurrent, BarVoltage, OverVoltageBTL, VTHBTL)
    elif len(DigitizerList) == 4:
        Digitizer1 = DigitizerList[0]
        Digitizer2 = DigitizerList[1]
        Digitizer3 = DigitizerList[2]
        Digitizer4 = DigitizerList[3]
        data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": ["%s","%s","%s","%s"], "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"], "TimingDAQTOFHIR": ["%s"], "TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"], "TimingDAQNoTracksTOFHIR": ["%s"], "LabviewRecoVME": ["%s"], "LabviewRecoDT5742": ["%s"], "LabviewRecoKeySightScope": ["%s"], "LabviewRecoSampic": ["%s"], "LabviewRecoTekScope": ["%s"], "Configuration": ["%s"],"BoxTempOlmo": "%s","x_stageOlmo": "%s","y_stageOlmo": "%s","BoxVoltageOlmo": "%s","BarCurrentOlmo": "%s","z_rotationOlmo": "%s","BoxHumOlmo": "%s","BoxCurrentOlmo": "%s", "BarVoltageOlmo": "%s","OverVoltageBTL": "%s", "VTHBTL": "%s"}}' % (RunNumber, StartTime, Duration, Digitizer1, Digitizer2, Digitizer3, Digitizer4, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQTOFHIR, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, TimingDAQNoTracksTOFHIR, LabviewRecoVME, LabviewRecoDT5742, LabviewRecoKeySightScope, LabviewRecoSampic, LabviewRecoTekScope, ConfigID[0], BoxTemp, x_stage, y_stage, BoxVoltage, BarCurrent, z_rotation, BoxHum, BoxCurrent, BarVoltage, OverVoltageBTL, VTHBTL)
    elif len(DigitizerList) == 5:
        Digitizer1 = DigitizerList[0]
        Digitizer2 = DigitizerList[1]
        Digitizer3 = DigitizerList[2]
        Digitizer4 = DigitizerList[3]
        Digitizer5 = DigitizerList[4]
        data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": ["%s","%s","%s","%s","%s"], "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"], "TimingDAQTOFHIR": ["%s"], "TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"], "TimingDAQNoTracksTOFHIR": ["%s"], "LabviewRecoVME": ["%s"], "LabviewRecoDT5742": ["%s"], "LabviewRecoKeySightScope": ["%s"], "LabviewRecoSampic": ["%s"], "LabviewRecoTekScope": ["%s"], "Configuration": ["%s"],"BoxTempOlmo": "%s","x_stageOlmo": "%s","y_stageOlmo": "%s","BoxVoltageOlmo": "%s","BarCurrentOlmo": "%s","z_rotationOlmo": "%s","BoxHumOlmo": "%s","BoxCurrentOlmo": "%s", "BarVoltageOlmo": "%s","OverVoltageBTL": "%s", "VTHBTL": "%s"}}' % (RunNumber, StartTime, Duration, Digitizer1, Digitizer2, Digitizer3, Digitizer4, Digitizer5, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQTOFHIR, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, TimingDAQNoTracksTOFHIR, LabviewRecoVME, LabviewRecoDT5742, LabviewRecoKeySightScope, LabviewRecoSampic, LabviewRecoTekScope, ConfigID[0], BoxTemp, x_stage, y_stage, BoxVoltage, BarCurrent, z_rotation, BoxHum, BoxCurrent, BarVoltage, OverVoltageBTL, VTHBTL)

    #Example template of a query response :  {'records': [{'createdTime': '2015-02-12T03:40:42.000Z', 'fields': {'Conversion': ['Complete'], 'Time Resolution 1': 30, 'TimingDAQ': ['Failed'], 'Notes': 'Make test beam great again\n', 'HV 1': ['recJRiQqSHzTNZqal'], 'Run number': 4, 'Tracking': ['Processing'], 'Configuration': ['rectY95k7m19likjW'], 'Sensor': ['recNwdccBdzS7iBa5']}, 'id': 'recNsKOMDvYKrJzXd'}]}
    #data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": ["%s","%s"], "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"],"TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"],"Sensor": ["%s"],"Configuration": ["%s"]}}' % (RunNumber, StartTime, Duration, Digitizer1, Digitizer2, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, SensorID[0], ConfigID[0])
    #data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": %s, "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"],"TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"],"Sensor": ["%s"],"Configuration": ["%s"]}}' % (RunNumber, StartTime, Duration, DigitizerList, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, SensorID[0], ConfigID[0])
    #data = '{"fields":{"Run number": %d, "Digitizer": ["%s","%s"]}}' % (RunNumber, Digitizer1, Digitizer2)
    if data != "":
        response = am.requests.post(am.CurlBaseCommand, headers=headers, data=data)
        ResponseDict = am.ast.literal_eval(response.text)
        if Debug: return ResponseDict, data
    else:
        print('Nothing to log in the run table')


def NewRunRecordSimple(run_info,ConfigID,Debug,MyKey):
    header_info = {
        'Authorization': 'Bearer %s' % MyKey, 
        'Content-Type': 'application/json',
    }

    string_run_info = js.dumps({"fields":run_info})

    response = am.requests.post(am.CurlBaseCommand, headers=header_info, data=string_run_info)
    ResponseDict = am.ast.literal_eval(response.text)
    print(string_run_info)
    print(ResponseDict)
    if Debug: return ResponseDict, run_info


def NewRunRecord4(RunNumber, StartTime, Duration, DigitizerList, Tracking, ConversionSampic, ConversionTekScope,ETROC_baseline, ETROC_config,xrdcpRawKeySightScope,xrdcpRawLecroyScope,ConversionKeySightScope,ConversionLecroyScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope,TimingDAQLecroyScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope,TimingDAQNoTracksLecroyScope, TimingDAQNoTracksDT5742, LabviewRecoVME, LabviewRecoDT5742, LabviewRecoKeySightScope, LabviewRecoSampic, LabviewRecoTekScope, BoxTemp, x_stage, y_stage, BoxVoltage, BarCurrent, z_rotation, BoxHum, BoxCurrent, BarVoltage, Temp13ETL, Temp14ETL, Temp15ETL, Temp16ETL, Temp17ETL, Temp18ETL, Temp19ETL, Temp20ETL, LowVoltage1ETL, Current1ETL, LowVoltage2ETL, Current2ETL, LowVoltage3ETL, Current3ETL, ConfigID, Debug, MyKey):
    #NewRunRecord(RunNumber, DigitizerList, Debug)
    headers = {
        'Authorization': 'Bearer %s' % MyKey, 
        'Content-Type': 'application/json',
    }

    # xrdRaw = "N/A"
    # if KeySightScope in DigitizerList: xrdRaw="Not started"

    if len(DigitizerList)==0: return

    #Build digitizer list string first
    digitizerListString = '"Digitizer": ['
    for i, digitizer in enumerate( DigitizerList ):
        if (i == 0):
            digitizerListString = digitizerListString + ( '"%s"' % digitizer )
        else :
            digitizerListString = digitizerListString + ',' + ( '"%s"' % digitizer )
    digitizerListString = digitizerListString + ']'

    data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", %s, "ETROC baseline": "%s", "ETROC config": "%s" ,"xrdcpRawKeySightScope":["%s"],"xrdcpRawLecroyScope":["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "ConversionLecroyScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQLecroyScope": ["%s"], "TimingDAQDT5742": ["%s"],"TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksLecroyScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"], "LabviewRecoVME": ["%s"], "LabviewRecoDT5742": ["%s"], "LabviewRecoKeySightScope": ["%s"], "LabviewRecoSampic": ["%s"], "LabviewRecoTekScope": ["%s"], "Configuration": ["%s"],"BoxTempOlmo": "%s","x_stageOlmo": "%s","y_stageOlmo": "%s","BoxVoltageOlmo": "%s","BarCurrentOlmo": "%s","z_rotationOlmo": "%s","BoxHumOlmo": "%s","BoxCurrentOlmo": "%s", "BarVoltageOlmo": "%s", "Temp13ETL" : "%s", "Temp14ETL" : "%s", "Temp15ETL" : "%s", "Temp16ETL" : "%s", "Temp17ETL" : "%s", "Temp18ETL" : "%s", "Temp19ETL" : "%s", "Temp20ETL" : "%s", "LowVoltage1ETL" : "%s", "LowVoltage2ETL" : "%s", "LowVoltage3ETL" : "%s", "Current1ETL" : "%s", "Current2ETL" : "%s", "Current3ETL" : "%s"}}' % (RunNumber, StartTime, Duration, digitizerListString , ETROC_baseline,ETROC_config, xrdcpRawKeySightScope, xrdcpRawLecroyScope, ConversionSampic, ConversionTekScope, ConversionKeySightScope, ConversionLecroyScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQLecroyScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksLecroyScope, TimingDAQNoTracksDT5742, LabviewRecoVME, LabviewRecoDT5742, LabviewRecoKeySightScope, LabviewRecoSampic, LabviewRecoTekScope, ConfigID[0], BoxTemp, x_stage, y_stage, BoxVoltage, BarCurrent, z_rotation, BoxHum, BoxCurrent, BarVoltage, Temp13ETL, Temp14ETL, Temp15ETL, Temp16ETL, Temp17ETL, Temp18ETL, Temp19ETL, Temp20ETL, LowVoltage1ETL, LowVoltage2ETL, LowVoltage3ETL, Current1ETL, Current2ETL, Current3ETL)

    print(data)

    #Example template of a query response :  {'records': [{'createdTime': '2015-02-12T03:40:42.000Z', 'fields': {'Conversion': ['Complete'], 'Time Resolution 1': 30, 'TimingDAQ': ['Failed'], 'Notes': 'Make test beam great again\n', 'HV 1': ['recJRiQqSHzTNZqal'], 'Run number': 4, 'Tracking': ['Processing'], 'Configuration': ['rectY95k7m19likjW'], 'Sensor': ['recNwdccBdzS7iBa5']}, 'id': 'recNsKOMDvYKrJzXd'}]}

    #data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": ["%s","%s"], "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"],"TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"],"Sensor": ["%s"],"Configuration": ["%s"]}}' % (RunNumber, StartTime, Duration, Digitizer1, Digitizer2, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, SensorID[0], ConfigID[0])
    #data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": %s, "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"],"TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"],"Sensor": ["%s"],"Configuration": ["%s"]}}' % (RunNumber, StartTime, Duration, DigitizerList, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, SensorID[0], ConfigID[0])
    #data = '{"fields":{"Run number": %d, "Digitizer": ["%s","%s"]}}' % (RunNumber, Digitizer1, Digitizer2)
    response = am.requests.post(am.CurlBaseCommand, headers=headers, data=data)
    ResponseDict = am.ast.literal_eval(response.text)
    # print data
    # print ResponseDict
    if Debug: return ResponseDict, data

def NewRunRecord5(RunNumber, MyKey, ConfigID):
    #NewRunRecord(RunNumber, DigitizerList, Debug)
    headers = {
        'Authorization': 'Bearer %s' % MyKey, 
        'Content-Type': 'application/json',
    }
    Digitizer = "KeySightScope"
    
    Tracking = "Not started"
    ConversionKeySightScope = "Not started"
    TimingDAQKeySightScope = "Not started"
    TimingDAQNoTracksKeySightScope =  "Not started"
    Notes = "Without Autopilot"
    data = '{"fields":{"Run number": %d, "Digitizer": ["%s"], "Tracking": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "Configuration": ["%s"], "Notes": "%s"}}' % (RunNumber, Digitizer, Tracking, ConversionKeySightScope, TimingDAQKeySightScope, TimingDAQNoTracksKeySightScope, ConfigID[0], Notes)
    
    #Example template of a query response :  {'records': [{'createdTime': '2015-02-12T03:40:42.000Z', 'fields': {'Conversion': ['Complete'], 'Time Resolution 1': 30, 'TimingDAQ': ['Failed'], 'Notes': 'Make test beam great again\n', 'HV 1': ['recJRiQqSHzTNZqal'], 'Run number': 4, 'Tracking': ['Processing'], 'Configuration': ['rectY95k7m19likjW'], 'Sensor': ['recNwdccBdzS7iBa5']}, 'id': 'recNsKOMDvYKrJzXd'}]}
    #data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": ["%s","%s"], "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"],"TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"],"Sensor": ["%s"],"Configuration": ["%s"]}}' % (RunNumber, StartTime, Duration, Digitizer1, Digitizer2, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, SensorID[0], ConfigID[0])
    #data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": %s, "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"],"TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"],"Sensor": ["%s"],"Configuration": ["%s"]}}' % (RunNumber, StartTime, Duration, DigitizerList, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, SensorID[0], ConfigID[0])
    #data = '{"fields":{"Run number": %d, "Digitizer": ["%s","%s"]}}' % (RunNumber, Digitizer1, Digitizer2)
    response = am.requests.post(am.CurlBaseCommand, headers=headers, data=data)
    ResponseDict = am.ast.literal_eval(response.text)
    return ResponseDict, data


def NewRunRecord3(RunNumber, BoxTemp, x_stage, y_stage, BoxVoltage, BarCurrent, z_rotation, BoxHum, BoxCurrent, BarVoltage, Debug, MyKey):
    #NewRunRecord(RunNumber, DigitizerList, Debug)
    headers = {
        'Authorization': 'Bearer %s' % MyKey, 
        'Content-Type': 'application/json',
    }

    #Example template of a query response :  {'records': [{'createdTime': '2015-02-12T03:40:42.000Z', 'fields': {'Conversion': ['Complete'], 'Time Resolution 1': 30, 'TimingDAQ': ['Failed'], 'Notes': 'Make test beam great again\n', 'HV 1': ['recJRiQqSHzTNZqal'], 'Run number': 4, 'Tracking': ['Processing'], 'Configuration': ['rectY95k7m19likjW'], 'Sensor': ['recNwdccBdzS7iBa5']}, 'id': 'recNsKOMDvYKrJzXd'}]}
    #data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": ["%s","%s"], "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"],"TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"],"Sensor": ["%s"],"Configuration": ["%s"]}}' % (RunNumber, StartTime, Duration, Digitizer1, Digitizer2, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, SensorID[0], ConfigID[0])
    #data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": %s, "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"],"TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"],"Sensor": ["%s"],"Configuration": ["%s"]}}' % (RunNumber, StartTime, Duration, DigitizerList, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, SensorID[0], ConfigID[0])
    data = data = '{"fields":{"Run number": %d,"BoxTemp": "%s","x_stage": "%s","y_stage": "%s","BoxVoltage": "%s","BarCurrent": "%s","z_rotation": "%s","BoxHum": "%s","BoxCurrent": "%s", "BarVoltage": "%s"}}' % (RunNumber, BoxTemp, x_stage, y_stage, BoxVoltage, BarCurrent, z_rotation, BoxHum, BoxCurrent, BarVoltage)
    response = am.requests.post(am.CurlBaseCommand, headers=headers, data=data)
    ResponseDict = am.ast.literal_eval(response.text)
    if Debug: return ResponseDict, data
