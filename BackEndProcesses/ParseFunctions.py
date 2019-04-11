import AllModules as am

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


##################### Main Run Table Operaton functions #########################

def ParsingQuery(NumberOfConditions, ConditionAttributeNames, ConditionAttributeStatus, QueryAttributeName, Debug):
    Output = [] 
    FieldID = []
    FilterByFormula = None
    headers = {'Authorization': 'Bearer %s' % am.MyKey, }
    for i in range (0, NumberOfConditions): 
        if i > 0: FilterByFormula = FilterByFormula + ','
        FilterByFormula = FilterByFormula + EqualToFunc(Curly(ConditionAttributeNames[i]), DoubleQuotes(ConditionAttributeStatus[i])) 
    if NumberOfConditions > 1: FilterByFormula = 'AND(' + FilterByFormula + ')'
    response = am.requests.get(am.CurlBaseCommand  + '?filterByFormula=' + FilterByFormula, headers=headers)
    ResponseDict = am.ast.literal_eval(response.text)
    if Debug: return ResponseDict, FilterByFormula

    for i in ResponseDict["records"]: Output.append(i['fields'][QueryAttributeName])   
    for i in ResponseDict["records"]: FieldID.append(i['id'])   
    return Output, FieldID

def GetDigiFromConfig(ConfigurationNumber, Debug):
    Output = [] 
    FieldID = []
    DigitizerList = []
    headers = {'Authorization': 'Bearer %s' % am.MyKey, }
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

def GetFieldID(ConditionAttributeName, ConditionAttributeStatus, Debug):
    Output = [] 
    FilterByFormula = EqualToFunc(Curly(ConditionAttributeName), DoubleQuotes(ConditionAttributeStatus))
    headers = {'Authorization': 'Bearer %s' % am.MyKey, }
    response = am.requests.get(am.CurlBaseCommand  + '?filterByFormula=' + FilterByFormula, headers=headers)
    ResponseDict = am.ast.literal_eval(response.text)
    if Debug: return ResponseDict, FilterByFormula

    for i in ResponseDict["records"]: Output.append(i['id'])   
    return Output

def UpdateAttributeStatus(FieldID, UpdateAttributeName, UpdateAttributeStatus, Debug):
    headers = {
        'Authorization': 'Bearer %s' % am.MyKey, 
        'Content-Type': 'application/json',
    }
    data = '{"fields":{"%s": ["%s"]}}' % (UpdateAttributeName,UpdateAttributeStatus)
    response = am.requests.patch(am.CurlBaseCommand + '/' + FieldID, headers=headers, data=data)
    ResponseDict = am.ast.literal_eval(response.text)
    if Debug: return ResponseDict

def GetFieldIDOtherTable(TableName,ConditionAttributeName, ConditionAttributeStatus, Debug):     
    if TableName == 'Sensor' :
        CurlBaseCommand = am.CurlBaseCommandSensor
    elif TableName == 'Config':
        CurlBaseCommand = am.CurlBaseCommandConfig
    Output = [] 
    FilterByFormula = EqualToFunc(Curly(ConditionAttributeName), DoubleQuotes(ConditionAttributeStatus))
    headers = {'Authorization': 'Bearer %s' % am.MyKey, }
    response = am.requests.get(CurlBaseCommand  + '?filterByFormula=' + FilterByFormula, headers=headers)
    ResponseDict = am.ast.literal_eval(response.text)
    if Debug: return ResponseDict, FilterByFormula
    for i in ResponseDict["records"]: Output.append(i['id'])   
    return Output

def NewRunRecord(RunNumber, StartTime, Duration, DigitizerList, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, SensorID, ConfigID, Debug):
#NewRunRecord(RunNumber, DigitizerList, Debug)
    headers = {
        'Authorization': 'Bearer %s' % am.MyKey, 
        'Content-Type': 'application/json',
    }
    Digitizer1 = 'KeySightScope'
    Digitizer2 = 'DT5742'
    #Example template of a query response :  {'records': [{'createdTime': '2015-02-12T03:40:42.000Z', 'fields': {'Conversion': ['Complete'], 'Time Resolution 1': 30, 'TimingDAQ': ['Failed'], 'Notes': 'Make test beam great again\n', 'HV 1': ['recJRiQqSHzTNZqal'], 'Run number': 4, 'Tracking': ['Processing'], 'Configuration': ['rectY95k7m19likjW'], 'Sensor': ['recNwdccBdzS7iBa5']}, 'id': 'recNsKOMDvYKrJzXd'}]}
    data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": ["%s","%s"], "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"],"TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"],"Sensor": ["%s"],"Configuration": ["%s"]}}' % (RunNumber, StartTime, Duration, Digitizer1, Digitizer2, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, SensorID[0], ConfigID[0])
    #data = '{"fields":{"Run number": %d,"Start time": "%s", "Duration": "%s", "Digitizer": %s, "Tracking": ["%s"], "ConversionSampic": ["%s"], "ConversionTekScope": ["%s"], "ConversionKeySightScope": ["%s"], "TimingDAQVME": ["%s"], "TimingDAQSampic": ["%s"], "TimingDAQTekScope": ["%s"], "TimingDAQKeySightScope": ["%s"], "TimingDAQDT5742": ["%s"],"TimingDAQNoTracksVME": ["%s"], "TimingDAQNoTracksSampic": ["%s"], "TimingDAQNoTracksTekScope": ["%s"], "TimingDAQNoTracksKeySightScope": ["%s"], "TimingDAQNoTracksDT5742": ["%s"],"Sensor": ["%s"],"Configuration": ["%s"]}}' % (RunNumber, StartTime, Duration, DigitizerList, Tracking, ConversionSampic, ConversionTekScope, ConversionKeySightScope, TimingDAQVME, TimingDAQSampic, TimingDAQTekScope, TimingDAQKeySightScope, TimingDAQDT5742, TimingDAQNoTracksVME, TimingDAQNoTracksSampic, TimingDAQNoTracksTekScope, TimingDAQNoTracksKeySightScope, TimingDAQNoTracksDT5742, SensorID[0], ConfigID[0])
    #data = "{'fields':{'Run number': %d, 'Digitizer': %s}}" % (RunNumber, DigitizerList)
    response = am.requests.post(am.CurlBaseCommand, headers=headers, data=data)
    ResponseDict = am.ast.literal_eval(response.text)
    if Debug: return ResponseDict, data
    


 
